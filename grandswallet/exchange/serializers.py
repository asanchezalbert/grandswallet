from rest_framework import serializers
from . import models


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Code

        fields = (
            'id',
            'code',
            'amount',
            'reference',
            'phone_number',
            'is_active'
        )

        read_only_fields = (
            'code',
            'is_active'
        )
