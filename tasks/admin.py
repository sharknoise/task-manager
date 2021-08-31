from django.contrib import admin

from tasks.models import Task, TaskLabels


class LabelInline(admin.TabularInline):
    """
    A class that adds a widget for TaskLabels.

    Django admin doesn't show a widget for m2m by default.
    """

    model = TaskLabels
    extra = 1  # only a form for 1 label initially


class TaskAdmin(admin.ModelAdmin):
    inlines = (LabelInline,)


admin.site.register(Task, TaskAdmin)
