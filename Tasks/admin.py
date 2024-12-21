from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from django.urls import reverse
from urllib.parse import urlencode
from . import models



#Task Admin
@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["name", "employer_name", "amount"]
    list_per_page = 15

    def employer_name(self, task):
        url = (
            reverse("admin:users_workituser_changelist")
            + '?'
            + urlencode({
                "id": str(task.employer.id)
            })
        )
        return format_html("<a href='{}'>{}</a>", url, task.employer)




# Location Admin
@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["place", "task_count"]
    list_per_page = 15


    @admin.display(ordering="task_count")
    def task_count(self, location):
        return location.task_count
    

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            task_count = Count('task')
        )
    




@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "task_count"]
    list_per_page = 15

    @admin.display(ordering="task_count")
    def task_count(self, category):
        return category.task_count


    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            task_count = Count('task')
        )