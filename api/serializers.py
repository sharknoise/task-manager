from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    created = serializers.DateTimeField()
    author = serializers.CharField()
    executor = serializers.CharField()
    status = serializers.CharField()
