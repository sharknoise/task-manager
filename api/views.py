from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import TaskSerializer
from tasks.models import Task
from users.models import UserModel


class APIUsersListView(APIView):
    """
    List of all task manager users.
    """

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [str(user) for user in UserModel.objects.all()]
        return Response(usernames)


class APITasksView(APIView):
    """
    List of all tasks with detailed information.
    """
    def get(self, request):
        tasks = Task.objects.all()
        # 'many' parameter used to serialize more than a single task
        serializer = TaskSerializer(tasks, many=True)
        return Response({'tasks': serializer.data})
