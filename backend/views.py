from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import UserRegistrationSerializer, UserProfileUpdateSerializer
from django.contrib.auth import get_user_model
from .models import Profile,Crew, Designation
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.contrib.auth import login
from .serializers import LoginSerializer,CrewSerializer, DesignationSerializer,CrewCreateSerializer\
    ,DesignationCreateSerializer,CrewDetailSerializer,UserProfileSerializer
from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from django.contrib.auth import authenticate





User = get_user_model()

class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    authentication_classes = []
    permission_classes = []
    

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            response_data = {
                "message": "User Login success",
                "status": True
            }
            return Response(response_data, status=HTTP_200_OK)
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
    
class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'user_id'


#for accept - reject req from user

class ProfileUpdateRequest(APIView):
    def post(self, request, user_id):
        action = request.data.get('action')  
        
        try:
            profile = Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)

        if action == 'accept':
            profile.save() 
            return Response({'message': 'Profile update request accepted'}, status=status.HTTP_200_OK)
        elif action == 'reject':
            profile.delete()
            return Response({'message': 'Profile update request rejected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        

#for admin login

class SuperuserLogin(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if user is not None and user.is_superuser:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None and authenticated_user.is_superuser:
                return Response({'message': 'Superuser login successful', 'user': user.username}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials or user is not a superuser'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid credentials or user is not a superuser'}, status=status.HTTP_401_UNAUTHORIZED)