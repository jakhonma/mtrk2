from django.contrib import admin
from helper.models import Fond, Department, Category, Mtv, Language, Region, Format


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['id', 'name']


@admin.register(Fond)
class FondAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_department_name']
    search_fields = ['name']

    def get_department_name(self, obj):
        return obj.department.name if obj.department else "No Department"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['id', 'name']


admin.site.register([Mtv, Language, Region, Format])
