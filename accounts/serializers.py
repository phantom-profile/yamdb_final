from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'bio',
                  'role')
        lookup_field = 'username'
        model = User

    def validate(self, attrs):
        email = attrs.get('email',)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': 'Email is already in use'})
        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ConfirmationCodeEmailSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email',)
        model = User
