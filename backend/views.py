from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserProfileUpdateSerializer
from django.contrib.auth import get_user_model
from .models import Profile,Crew, Designation
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import login
from .serializers import LoginSerializer,CrewSerializer, DesignationSerializer,CrewCreateSerializer,DesignationCreateSerializer,CrewDetailSerializer
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404

User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response({"status": True, "message": "Login success"}, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    

class CrewListAPIView(generics.ListAPIView):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

class CrewCreateAPIView(generics.CreateAPIView):
    queryset = Crew.objects.all()
    serializer_class = CrewCreateSerializer

class DesignationCreateAPIView(generics.CreateAPIView):
    queryset = Designation.objects.all()
    serializer_class = DesignationCreateSerializer

    def perform_create(self, serializer):
        crew_id = self.kwargs['crew_id']
        try:
            crew = Crew.objects.get(id=crew_id)
        except Crew.DoesNotExist:
            raise NotFound('Crew not found')
        serializer.save(crew=crew)

class DesignationListByCrewAPIView(generics.ListAPIView):
    serializer_class = DesignationSerializer

    def get_queryset(self):
        crew_id = self.kwargs['crew_id']
        return Designation.objects.filter(crew_id=crew_id)

class UserProfileUpdateAPIView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileUpdateSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        try:
            profile = Profile.objects.get(user__id=user_id)
        except Profile.DoesNotExist:
            raise NotFound('Profile not found')
        return profile
    

class CrewDetailAPIView(generics.RetrieveAPIView):
    queryset = Crew.objects.all()
    serializer_class = CrewDetailSerializer
    lookup_field = 'id'

    def retrieve(self, request, *args, **kwargs):
        crew = self.get_object()
        designations = crew.designations.all()  # Adjust this line if the related_name is different
        serializer = self.get_serializer(crew)
        designation_serializer = DesignationSerializer(designations, many=True)
        data = serializer.data
        data['designations'] = designation_serializer.data
        return Response(data)
    
class CrewDetailByNameAPIView(generics.GenericAPIView):
    serializer_class = CrewDetailSerializer

    def get(self, request, name, *args, **kwargs):
        crew = get_object_or_404(Crew, name=name)
        serializer = self.get_serializer(crew)
        return Response(serializer.data, status=status.HTTP_200_OK)