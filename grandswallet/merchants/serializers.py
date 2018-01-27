from rest_framework import serializers
from . import models


class MerchantAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MerchantAddress

        fields = (
            'street',
            'outdoor_number',
            'interior_number',
            'outdoor_number',
            'neighborhood',
            'municipality',
            'city',
            'state',
            'country',
            'postal_code',
            'created_date'
        )

        read_only_fields = (
            'created_date',
        )


class SignUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=10, min_length=10, write_only=True
    )

    email_address = serializers.EmailField()

    password = serializers.CharField(
        max_length=255, write_only=True
    )

    confirm_password = serializers.CharField(
        max_length=255, write_only=True
    )

    address = MerchantAddressSerializer(
        write_only=True
    )

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        phone_number = validated_data.pop('phone_number')
        email_address = validated_data.pop('email_address')
        password = validated_data.pop('password')
        address = validated_data.pop('address')

        merchant = super().create(validated_data)
        user = models.MerchantUser.objects.create(
            merchant=merchant,
            username=phone_number
        )
        user.set_password(password)
        user.save()

        merchant.emails.create(
            email_address=email_address
        )

        merchant.phones.create(
            phone_number=phone_number
        )

        merchant.addresses.create(**address)

        return merchant

    class Meta:
        model = models.Merchant

        fields = (
            'first_name',
            'middle_name',
            'last_name_paternal',
            'last_name_maternal',
            'date_of_birth',
            'person_id',
            'phone_number',
            'email_address',
            'password',
            'confirm_password',
            'address',
            'created_date'
        )

        read_only_fields = (
            'created_date',
        )
