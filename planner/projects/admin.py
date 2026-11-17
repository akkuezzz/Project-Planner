from django.contrib import admin

from . import models


# Register your models here.

admin.site.register(models.Project)

admin.site.register(models.AssignedProject)

admin.site.register(models.Task)

