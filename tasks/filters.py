import django_filters
from django import forms
from django.utils.translation import ugettext_lazy as _

from labels.models import Label
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    author_tasks = django_filters.BooleanFilter(
        field_name='author',
        label=_('Show my tasks only'),
        widget=forms.CheckboxInput,
        method='filter_author')
    labels = django_filters.ModelChoiceFilter(queryset=Label.objects.all())

    class Meta(object):
        model = Task
        fields = ['executor', 'status']

    def filter_author(self, queryset, name, value):
        if value:
            queryset = queryset.filter(author=self.request.user)
        return queryset
