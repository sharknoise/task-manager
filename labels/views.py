from django.views import generic

from labels.models import Label


class LabelsListView(generic.ListView):
    model = Label
    template_name = 'labels/labels-list.html'
