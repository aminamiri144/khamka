from rest_framework import serializers
from requisitions.models import Request


class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ('number', 'title', 'jd_register_date',
                  'customer_name', 'status_d', 'result_d')
