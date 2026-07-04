from django.contrib import admin
from .models import Tasks,SubTask

class TaskAdmin(admin.ModelAdmin):
    list_display = ("title","assigned_to","status")

class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title","task")

admin.site.register(Tasks,TaskAdmin)
admin.site.register(SubTask,SubTaskAdmin)
