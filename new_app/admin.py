from email.headerregistry import Group
from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from django.contrib.auth.models import Group
from django.contrib import admin
import nested_admin
from .models import (
    Gdp,
    Product, 
    Detail, 
    Country, 
    Import_export_for_db, 
    X_and_C_for_db, 
    Matrix,
    Gdp
)
admin.site.unregister(Group)

@admin.register(Import_export_for_db, X_and_C_for_db, Matrix, Gdp)
class Admin(ImportExportActionModelAdmin):
    pass

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_filter = ('country_name',)
    search_fields = ('country_name',)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('code_product','product_name', 'skp')
#     search_fields = ('product_name',)

# @admin.register(Detail)
# class DetailAdmin(admin.ModelAdmin):
#     list_filter = ('product_id',)
#     search_fields = ('product_id',)


class DetailInline(nested_admin.NestedStackedInline):
    model = Detail
    search_fields = ('product',)
    list_filter = ('product', 'year')
class ProductAdmin(nested_admin.NestedModelAdmin):
    inlines = [DetailInline,]
    search_fields = ('product_name',)
    list_filter = ('skp',)
    list_display = ('code_product','product_name', 'skp')
admin.site.register(Product, ProductAdmin)