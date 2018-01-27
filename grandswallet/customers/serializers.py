from rest_framework import serializers
from . import models


class CustomerAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerAddress

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


class CustomerSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
        max_length=10, min_length=10, write_only=True
    )

    email_address = serializers.EmailField(
        write_only=True
    )

    password = serializers.CharField(
        max_length=255, write_only=True
    )

    confirm_password = serializers.CharField(
        max_length=255, write_only=True
    )

    address = CustomerAddressSerializer(
        write_only=True
    )

    is_active = serializers.ReadOnlyField(
        source='user.is_active'
    )

    is_verified = serializers.ReadOnlyField(
        source='user.is_verified'
    )

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        phone_number = validated_data.pop('phone_number')
        email_address = validated_data.pop('email_address')
        password = validated_data.pop('password')
        address = validated_data.pop('address')

        customer = super().create(validated_data)

        customer.emails.create(
            email_address=email_address
        )

        customer.phones.create(
            phone_number=phone_number
        )

        customer.addresses.create(**address)

        user = models.CustomerUser.objects.create(
            customer=customer,
            username=phone_number
        )
        user.set_password(password)
        user.save()

        return customer

    class Meta:
        model = models.Customer

        fields = (
            'id',
            'first_name',
            'middle_name',
            'last_name_paternal',
            'last_name_maternal',
            'date_of_birth',
            'elector_id',
            'person_id',
            'phone_number',
            'email_address',
            'password',
            'confirm_password',
            'address',
            'created_date',
            'is_active',
            'is_verified'
        )

        read_only_fields = (
            'created_date',
        )

        extra_kwargs = {
            'elector_id': {'write_only': True},
            'person_id': {'write_only': True}
        }


class VerificationSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=12, min_length=12
    )


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerDocument

        fields = (
            'id',
            'document_file',
            'created_date'
        )

        read_only_fields = (
            'created_date',
        )


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomerAccount

        fields = (
            'id',
            'name',
            'created_date',
            'balances'
        )
