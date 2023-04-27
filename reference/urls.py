from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from .views import RefBookList, RefbookElementsView, RefbookElementCheckView

app_name = 'reference'

api_info = openapi.Info(
    title="My API",
    default_version='v1',
    description="My API description",
)

schema_view = get_schema_view(
    api_info,
    public=True,
    permission_classes=([permissions.AllowAny, ]),
)


urlpatterns = [
    path('refbooks/', RefBookList.as_view(), name='refbook-list'),
    path('refbooks/<int:id>/elements/', RefbookElementsView.as_view(), name='refbook_elements_list'),
    path('refbooks/<int:id>/check_element/', RefbookElementCheckView.as_view(), name='check_refbook_element'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
