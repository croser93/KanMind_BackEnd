from rest_framework import serializers
from django.contrib.auth.models import User

class RegistrationSerializer(serializers.ModelSerializer):

    repeated_password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'repeated_password']
        extra_kwargs = {
        'password': {'write_only': True},
        'email': {'required': True}
    }
        
    def save(self):
        pw = self.validated_data['password']
        repeated_password = self.validated_data['repeated_password']
        email = self.validated_data['email']
        all_email = User.objects.values_list('email', flat=True)

        if pw != repeated_password:
            raise serializers.ValidationError({'error': 'password dont match'})
        
        if email in all_email:
            raise serializers.ValidationError({'error': 'email is used'})
        
        account = User(email = self.validated_data['email'], username=self.validated_data['username'])
        account.set_password(pw)
        account.save()
        return account