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


class ExchangeSerializer(serializers.ModelSerializer):
    code = serializers.SlugRelatedField(
        slug_field='code', queryset=models.Code.objects.filter(is_active=True)
    )

    pin = serializers.CharField(
        max_length=4, write_only=True
    )

    def create(self, validated_data):
        validated_data.pop('pin')

        return super().create(validated_data)

    class Meta:
        model = models.Exchange

        fields = (
            'pin',
            'code',
            'created_date',
            'authorization',
            'transaction',
            'amount',
            'details'
        )

        read_only_fields = (
            'created_date',
            'authorization',
            'transaction'
        )
