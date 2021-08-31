from rest_framework import serializers

from labels.models import Label
from tasks.models import Task


class LabelSerializer(serializers.ModelSerializer):
    """A special serializer we need because Task-Label is m2m."""

    def to_representation(self, value):
        """Represent with value only instead of {key: value}."""
        return value.name

    class Meta(object):
        model = Label
        fields = ['name']


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.CharField()
    executor = serializers.CharField()
    status = serializers.CharField()
    labels = LabelSerializer(many=True)

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
            'labels',
        ]
