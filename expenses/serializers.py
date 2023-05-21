from rest_framework import serializers
from .models import Expenses,User


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_det = self.Meta.model(**validated_data)

        if password is not None:
            user_det.set_password(password)
        user_det.save()

        return user_det

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = '__all__'
