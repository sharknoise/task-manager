from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TaskSerializer
from tasks.models import Task
from users.models import UserModel


class APIUsersListView(APIView):
    """List of all task manager users."""

    def get(self, request, format=None):
        """Return full names of all users without using a Serializer class."""
        usernames = [str(user) for user in UserModel.objects.all()]
        return Response(usernames)


class APITasksView(ListAPIView):
    """List of all tasks with detailed information."""

    queryset = Task.objects.all()
    serializer_class = TaskSerializer
