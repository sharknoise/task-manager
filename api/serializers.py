from rest_framework import serializers

from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    executor = serializers.CharField()
    status = serializers.CharField()

    class Meta(object):
        model = Task
        fields = [
            'id',
            'name',
            'description',
            'created',
            'author',
            'executor',
            'status',
        ]
