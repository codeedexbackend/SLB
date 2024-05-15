from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth import authenticate

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'mobile_number']

    def create(self, validated_data):
        # Create the User object first
        user = User.objects.create_user(username=validated_data['mobile_number'])
        
        # Then, create the Profile object
        profile = Profile.objects.create(user=user, **validated_data)
        return profile

class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'gate_pass_no', 'crew', 'designation', 'rig_or_rigless',
            'project_name', 'company_name', 'profile_photo'
        ]



class LoginSerializer(serializers.Serializer):
    full_name = serializers.CharField()
    mobile_number = serializers.CharField()

    def validate(self, data):
        full_name = data.get('full_name')
        mobile_number = data.get('mobile_number')

        if full_name and mobile_number:
            user = authenticate(full_name=full_name, mobile_number=mobile_number)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError("Invalid full name or mobile number")
        else:
            raise serializers.ValidationError("Both fields are required")
        return data