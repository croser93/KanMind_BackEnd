from rest_framework import serializers
from django.contrib.auth.models import User
from django.core.validators import RegexValidator 
from django.contrib.auth import authenticate

class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    fullname = serializers.CharField(
        validators=[RegexValidator(r'^[a-zA-ZäöüÄÖÜß\s]+$', 'Only letters and spaces allowed.')]
    )
    class Meta:
        model = User
        fields = ['fullname', 'email', 'password', 'repeated_password']
        extra_kwargs = {
        'password': {'write_only': True},
        'email': {'required': True}
    }

    def validate_fullname(self, value):
        if len(value.split()) < 2:
            raise serializers.ValidationError({'error': 'Enter your Firstname and Lastname'})
        return value
        
    def save(self):
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email = self.validated_data['email']
        all_email = User.objects.values_list('email', flat=True)
        full_name = self.validated_data['fullname']
        name_parts = full_name.split()
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])

        if pw != repeated_password:
            raise serializers.ValidationError({'error': 'password dont match'})
        
        if email in all_email:
            raise serializers.ValidationError({'error': 'email is used'})
        
        account = User(
            email=email,
            username=first_name + '-' + last_name,
            first_name=first_name,
            last_name=last_name
        )
        account.set_password(pw)
        account.save()
        return account

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user_mail = User.objects.filter(email=data['email']).first()
        if user_mail and user_mail.check_password(data['password']):
            return {'user': user_mail}
        raise serializers.ValidationError({'error': 'Wrong credentials'})
