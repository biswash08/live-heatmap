from rest_framework import serializers


class AuthHealthSerializer(serializers.Serializer):
    status = serializers.CharField()
    service = serializers.CharField()
