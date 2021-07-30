from django.views import generic

from statuses.models import Status


class StatusesListView(generic.ListView):
    model = Status
    template_name = 'statuses/statuses-list.html'
