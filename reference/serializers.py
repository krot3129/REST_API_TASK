from rest_framework import serializers
from .models import Reference, ReferenceVersion, ReferenceElement


class RefBookSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели справочника
    """
    class Meta:
        model = Reference
        fields = ['id', 'code', 'name']


class RefBookVersionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели версии справочника
    """
    class Meta:
        model = ReferenceVersion
        fields = ['version', 'start_date']


class RefBookElementSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели элемента справочника
    """
    class Meta:
        model = ReferenceElement
        fields = ['code', 'value']


class ReferenceSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели справочника со всеми версиями
    """
    versions = RefBookVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Reference
        fields = ['id', 'code', 'name', 'description', 'versions']


class ReferenceVersionSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели версии справочника со всеми элементами
    """
    elements = RefBookElementSerializer(many=True, read_only=True)

    class Meta:
        model = ReferenceVersion
        fields = ['id', 'reference', 'version', 'start_date', 'elements']
