from rest_framework.serializers import ModelSerializer, RelatedField

from .models import User


class TokenField(RelatedField):

    def to_representation(self, value):
        return value.token


class UserSerializer(ModelSerializer):

    token = TokenField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'github_id', 'email', 'token')
