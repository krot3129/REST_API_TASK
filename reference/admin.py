from django.contrib import admin
from .models import Reference, ReferenceVersion, ReferenceElement


class ReferenceVersionInline(admin.TabularInline):
    model = ReferenceVersion
    extra = 1


class ReferenceElementInline(admin.TabularInline):
    model = ReferenceElement
    extra = 1


@admin.register(Reference)
class ReferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'get_current_version')
    search_fields = ('code', 'name')
    inlines = [ReferenceVersionInline]


@admin.register(ReferenceVersion)
class ReferenceVersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'version', 'start_date')
    list_filter = ('reference',)
    search_fields = ('reference__code', 'reference__name')
    inlines = [ReferenceElementInline]


@admin.register(ReferenceElement)
class ReferenceElementAdmin(admin.ModelAdmin):
    list_display = ('id', 'version', 'code', 'value')
    list_filter = ('version__reference', 'version')
    search_fields = ('version__reference__code', 'version__reference__name', 'code', 'value')
