from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers

from pos_users.models import *


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password',)


class GeneralUserSerializer(serializers.ModelSerializer):
    """

    """

    password = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password',)


class UserSerializer(serializers.ModelSerializer):
    """
    business user signup
    """
    company_name = serializers.CharField(max_length=50, required=False)
    organization_id = serializers.IntegerField(required=False)
    user = GeneralUserSerializer()
    phone_number = serializers.CharField(max_length=50, required=True)

    def __init__(self, *args, **kwargs):
        super(UserSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        if not data.get('company_name'):
            raise serializers.ValidationError(
                {"company_name": "Please enter your company name."})
        return data

    def create(self, validated_data):
        user = User.objects.create(
            password=make_password(validated_data['user'].pop('password')),
            **validated_data.pop('user'))
        organization = Organization.objects.create(
            company_name=validated_data.pop('company_name'),
            is_2factor_auth_required=True)

        user.create_oauth_application()
        return OrganizationUser.objects.create(**validated_data, user=user,
                                               organization=organization)

    class Meta:
        model = OrganizationUser
        fields = ('user', 'company_name', 'organization_id', 'phone_number',
                  'is_business_owner',)


class ChangePasswordSerializer(serializers.Serializer):
    """
	Serializer for password change endpoint.
	"""
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password')
