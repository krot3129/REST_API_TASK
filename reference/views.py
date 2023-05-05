from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Reference, ReferenceVersion, ReferenceElement
from .serializers import RefBookSerializer, RefBookElementSerializer


class RefBookList(APIView):
    """
    Класс представления, возвращающий список справочников в формате JSON, отфильтрованный по указанной дате..

    Methods:
        get(request): Возвращает ответ JSON, содержащий список допустимых справочников.
        В указанную дату, если она предусмотрена. Если дата не указана, возвращает все доступные справочники.
    """

    @swagger_auto_schema(
        operation_summary="Get list of reference books",
        operation_description="Returns a JSON response containing the list of available reference books.",
        responses={200: 'refbooks'},
        manual_parameters=[
            openapi.Parameter(
                name='date',
                in_=openapi.IN_QUERY,
                required=False,
                type=openapi.TYPE_STRING,
                description='Date for filtering the list of reference books in format yyyy-mm-dd.'
            )
        ]
    )
    def get(self, request):
        date = self.request.query_params.get('date', None)
        refbooks = []
        for reference in Reference.objects.all():
            if date is not None:
                versions = ReferenceVersion.objects.filter(
                    reference=reference, start_date__lte=date
                ).order_by('-start_date')
            else:
                versions = ReferenceVersion.objects.filter(reference=reference).order_by('-start_date')
            if versions.exists():
                serializer = RefBookSerializer({'id': reference.id, 'code': reference.code, 'name': reference.name})
                refbooks.append(serializer.data)
        return Response({'refbooks': refbooks})


class RefbookElementsView(generics.RetrieveAPIView):
    """
    Класс для получения элементов конкретного справочника.

    """
    serializer_class = RefBookElementSerializer


    def get_queryset(self):
        """
        :argument:
        id (int): Идентификатор справочника.
        version (str, optional): Версия справочника для проверки.

        :return: elements : list
        Список элементов справочника.
        Raises: Http404:
        В случае отсутствия запрашиваемого справочника или его версии.
        """
        refbook_id = self.kwargs.get('id')
        version = self.request.query_params.get('version')

        refbook = get_object_or_404(Reference, id=refbook_id)

        # Получить текущую версию справочника
        current_version = refbook.get_current_version()

        # Если указана версия, отфильтровать элементы по версии
        if version:
            refbook_version = ReferenceVersion.objects.filter(reference=refbook, version=version).first()
            if refbook_version:
                elements = ReferenceElement.objects.filter(version=refbook_version)
                current_version = refbook_version
            else:
                elements = ReferenceElement.objects.none()
        # В противном случае получить элементы из текущей версии
        else:
            elements = ReferenceElement.objects.filter(version=current_version)

        return elements
    @swagger_auto_schema(
        operation_summary="Get elements of reference book",
        operation_description="Returns a JSON response containing the elements of a reference book.",
        responses={200: 'elements'},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the reference book", type=openapi.TYPE_INTEGER),
            openapi.Parameter('version', openapi.IN_QUERY, description="Version of the reference book",
                              type=openapi.TYPE_STRING),
        ]
    )
    def get(self, request, *args, **kwargs):
        """
        Получение элементов справочника.

        Returns:
        -------
        elements : list
            Список элементов справочника.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        response_data = {"elements": serializer.data}
        return Response(response_data)


class RefbookElementCheckView(APIView):
    """
    Представление для проверки существования данного ссылочного элемента с кодом и значением.
    В конкретной версии справочника.

    """

    @swagger_auto_schema(
        operation_summary="Check reference element",
        operation_description="Returns a JSON response indicating"
                              " whether the specified reference"
                              " element exists in the specified reference book version.",
        responses={200: 'exists'},
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="Идентификатор справочника",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                name="code",
                in_=openapi.IN_QUERY,
                description="Код элемента ссылки для проверки",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="value",
                in_=openapi.IN_QUERY,
                description="Значение элемента ссылки для проверки",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                name="version",
                in_=openapi.IN_QUERY,
                description="Версия справочника для проверки. Если не указано, будет использоваться текущая версия.",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def get(self, request, id):
        """
        GET request parameters:
        id (int): Идентификатор справочника.
        code (str): Код элемента ссылки для проверки.
        value (str): Значение элемента ссылки для проверки.
        version (str, optional): Версия справочника для проверки.
             Если не указано, будет использоваться текущая версия.
        Returns: Объект JSON с одним логическим полем «существует», что указывает
         найден ли элемент в указанной версии справочника."""
        # Извлекаем параметры из запроса
        code = self.request.query_params.get('code')
        value = self.request.query_params.get('value')
        version = self.request.query_params.get('version')

        # Получаем объект справочника по его идентификатору
        refbook = Reference.objects.get(id=id)

        # Если версия не указана, получаем текущую версию справочника
        if version is None:
            current_version = refbook.get_current_version()
            if current_version is None:
                return Response({"message": "No current version found"}, status=404)
            version = current_version.version

        # Получаем версию справочника с указанным номером версии
        refbook_version = ReferenceVersion.objects.filter(reference=refbook, version=version).first()

        # Проверяем, есть ли элемент с указанным кодом и значением в данной версии справочника
        element_exists = ReferenceElement.objects.filter(version=refbook_version, code=code, value=value).exists()

        # Возвращаем результат проверки
        return Response({"exists": element_exists})
