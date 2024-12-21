from django.contrib import admin
from django.db.models import Count
from .models import WORKitUser, Profile




@admin.register(WORKitUser)
class WORKitUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'task_count']

    @admin.display(ordering='task_count')
    def task_count(self, user):
        return user.task_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            task_count = Count('task')
        )
    

admin.site.register(Profile)
