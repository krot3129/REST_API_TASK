from django.contrib import admin
from reference.models import Reference, ReferenceVersion, ReferenceElement


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferenceVersion)
class ReferenceVersionAdmin(admin.ModelAdmin):
    pass


@admin.register(ReferenceElement)
class ReferenceElementAdmin(admin.ModelAdmin):
    pass
