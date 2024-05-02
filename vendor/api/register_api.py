from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from vendor.serializers import UserSerializer

class RegisterUser(APIView):
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response ({'status':403,'errors':serializer.errors,'message':'Something Went Wrong'})
        
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj = Token.objects.get_or_create(user=user)
        return Response({'status':200,'payload':serializer.data,'token':str(token_obj),'message':'Your data is saved'})