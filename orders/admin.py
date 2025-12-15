from django.contrib import admin
from .models import DesignPackage, DesignOrder, Deliverable

admin.site.register(DesignPackage)
admin.site.register(DesignOrder)
admin.site.register(Deliverable)
