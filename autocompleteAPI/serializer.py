from authentication.models import User
from rest_framework import serializers


class UsernameSerializer(serializers.ModelSerializer):
    text = serializers.CharField(source='username')

    class Meta:
        model = User
        fields = ('id','text')
