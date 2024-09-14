from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny 
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import *


@api_view(["POST"])
@permission_classes([AllowAny])
def registerView(request):
    if request.method == "POST":
        try:
            serial = UserSerializer(data=request.data)
            if serial.is_valid():
                if not User.objects.filter(username = request.data['username']).exists():
                    user=User(username = request.data["username"],email = request.data["email"])
                    if request.data['password'] == request.data['confirm']:
                        user.password = make_password(request.data["password"])
                        if 'role' in request.data:
                            print(request.data["role"])
                            if request.data["role"] == "admin":
                                user.is_superuser =True
                                user.is_staff = True
                            elif request.data["role"] == "staff":
                                user.is_staff =True
                        else:
                            pass
                        user.save()
                        token=Token.objects.get_or_create(user=user)

                        return Response({"username":user.username,"token":str(token[0])}, status=status.HTTP_201_CREATED)
                    else:
                        return Response({"message":"password did't match"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    
                else:
                    return Response({"message":"username already exist"}, status=status.HTTP_403_FORBIDDEN)
            else :
                return Response(serial.errors, status=status.HTTP_403_FORBIDDEN)
        except Exception as error:
            return Response({"error":str(error)}, status=status.HTTP_403_FORBIDDEN)
        
