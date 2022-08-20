from rest_framework import serializers
from .models import *


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    firstname = serializers.CharField()
    lastname = serializers.CharField()
    address = serializers.CharField()
    phone = serializers.CharField()
    avatar = serializers.URLField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'firstname', 'lastname', 'address', 'phone','avatar'
                 ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def save(self):
        user = User(
        email=self.validated_data['email'],
        username=self.validated_data['username'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.validationError({'password': 'Password must match'})
        user.set_password(password)
        user.save()
        profile = Profile(
            user=user,
            first_name=self.validated_data['firstname'],
            last_name=self.validated_data['lastname'],
            address=self.validated_data['address'],
            phone=self.validated_data['phone'],
            avatar=self.validated_data['avatar']

        )
        profile.save()


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
                  'id',
                  'name_fr',
                  'name_en',
                  'name_ar'
        ]


class ProductListreqSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'name_ar',
            'name_en',
            'name_fr',
            'photo',
            'stock',

        ]


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            'category',
            'name_ar',
            'name_en',
            'name_fr',
            'description',
            'photo',
            'stock',
        ]


class ProductGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            'owner',
            'product',
            'rating',
            'comment'
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'product',
            'quantity'
        ]


class OrderGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()