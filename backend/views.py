from django.conf import settings
from twilio.rest import Client
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OTP
from .serializers import OTPSerializer,VerifyOTPSerializer
import random

class SendOTP(APIView):
    def post(self, request):
        serializer = OTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
            OTP.objects.create(mobile_number=mobile_number, otp=otp)
            
            try:
                # Send OTP to the mobile number using Twilio
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    body=f'Your OTP is: {otp}',
                    from_=settings.TWILIO_PHONE_NUMBER,
                    to=mobile_number
                )
            except Exception as e:
                # Handle Twilio API exceptions
                return Response({"message": f"Failed to send OTP: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            return Response({"message": "OTP sent successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            mobile_number = serializer.validated_data['mobile_number']
            otp = serializer.validated_data['otp']
            # Verify OTP
            try:
                otp_obj = OTP.objects.get(mobile_number=mobile_number, otp=otp)
                # OTP verified, you can log the user in here
                otp_obj.delete()  # Remove the OTP from database after verification
                return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
            except OTP.DoesNotExist:
                return Response({"message": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)