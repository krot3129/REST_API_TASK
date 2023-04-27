from rest_framework import serializers
from .models import Reference, ReferenceVersion, ReferenceElement


class RefBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reference
        fields = ['id', 'code', 'name']


class RefBookVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceVersion
        fields = ['version', 'start_date']


class RefBookElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReferenceElement
        fields = ['code', 'value']


class ReferenceSerializer(serializers.ModelSerializer):
    versions = RefBookVersionSerializer(many=True, read_only=True)

    class Meta:
        model = Reference
        fields = ['id', 'code', 'name', 'description', 'versions']


class ReferenceVersionSerializer(serializers.ModelSerializer):
    elements = RefBookElementSerializer(many=True, read_only=True)

    class Meta:
        model = ReferenceVersion
        fields = ['id', 'reference', 'version', 'start_date', 'elements']
