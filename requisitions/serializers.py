from rest_framework import serializers
from requisitions.models import Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('number', 'title', 'register_date',
                  'customer', 'description', 'status', 'result')
