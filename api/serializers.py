from rest_framework import serializers
from .models import *

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'address', 'phone','avatar']


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2','profile']
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
            first_name=self.validated_data['profile']['first_name'],
            last_name=self.validated_data['profile']['last_name'],
            address=self.validated_data['profile']['address'],
            phone=self.validated_data['profile']['phone'],
            avatar=self.validated_data['profile']['avatar']

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