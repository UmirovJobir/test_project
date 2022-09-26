from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin

from django.contrib import admin
from .models import Product, Detail, Country


@admin.register(Product, Detail, Country)
class Admin(ImportExportActionModelAdmin):
    pass

