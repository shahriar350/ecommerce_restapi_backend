from rest_framework import serializers

from admin_app.models import Category, ShopCategory
from auth_app.models import SellerRequest, Users


class SellerRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerRequest
        fields = "__all__"

    def validate_contact(self, value):
        if not SellerRequest.objects.filter(contact=value).count() == 0:
            raise serializers.ValidationError("Phone number is already taken.")
        elif not Users.objects.filter(phone_number=value).count() == 0:
            raise serializers.ValidationError("Phone number is already taken.")
        elif not value.isdecimal():
            raise serializers.ValidationError("Phone number must be in number format")
        elif len(value) != 11:
            raise serializers.ValidationError("Phone number must be 11 digit")
        return value


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['id', 'name', 'password', 'phone_number', 'seller']

    def create(self, validated_data):
        print(validated_data)
        user = Users.objects.create_user(
            name=validated_data['name'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number'],
        )
        return user

    def validate_phone_number(self, data):
        if Users.objects.filter(phone_number=data).count() > 0:
            raise serializers.ValidationError("Phone number is already taken.")
        else:
            return data


class SingleUserSerializer(serializers.Serializer):
    phone_number = serializers.CharField(min_length=11, max_length=11)
    password = serializers.CharField()
