from django.contrib import admin

# Register your models here.

from Myapp.models import *
admin.site.register(DB_project)
admin.site.register(DB_mock)
admin.site.register(DB_api)
admin.site.register(DB_case)