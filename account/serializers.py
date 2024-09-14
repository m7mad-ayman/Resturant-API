from rest_framework.serializers import Serializer
from django.contrib.auth.models import User

class UserSerializer(Serializer):
    class Meta:
        model = User
        fields = "__all__"