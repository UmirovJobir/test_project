from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin
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

@admin.register(Import_export_for_db, X_and_C_for_db, Matrix, Gdp)
class Admin(ImportExportActionModelAdmin):
    pass

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_filter = ('country_name',)
    search_fields = ('country_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('code_product','product_name', 'skp')
    search_fields = ('product_name',)


    