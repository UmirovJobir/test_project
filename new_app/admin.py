from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin
from .models import Product, Detail, Country


@admin.register(Detail)
class Admin(ImportExportActionModelAdmin):
    pass



@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_filter = ('country_name',)
    search_fields = ('country_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('product_name',)
