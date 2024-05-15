from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile,Crew, Designation

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
    crew_name = serializers.SerializerMethodField()
    designation_name = serializers.SerializerMethodField()

    def get_crew_name(self, instance):
        crew = instance.crew
        return crew.name if crew else None

    def get_designation_name(self, instance):
        designation = instance.designation
        return designation.name if designation else None

    class Meta:
        model = Profile
        fields = [
            'gate_pass_no', 'crew', 'crew_name', 'designation', 'designation_name', 'rig_or_rigless',
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
    


class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['id', 'name']

class DesignationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['name'] 


class CrewSerializer(serializers.ModelSerializer):
    designations = DesignationSerializer(many=True, read_only=True)

    class Meta:
        model = Crew
        fields = ['id', 'name', 'designations']

class CrewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ['name']

class DesignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Designation
        fields = ['name']

class CrewDetailSerializer(serializers.ModelSerializer):
    designations = DesignationSerializer(many=True, read_only=True, source='designation_set')

    class Meta:
        model = Crew
        fields = ['name', 'designations']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        designations = data.pop('designations', [])  # Check if 'designations' exists, otherwise set to empty list
        data['designations'] = [designation['name'] for designation in designations]
        return data
    


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'gate_pass_no', 'crew', 'designation', 'rig_or_rigless', 'project_name', 'company_name', 'profile_photo','full_name']

class ProfilePhotoUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_photo']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'