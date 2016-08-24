from rest_framework.response import Response
from rest_framework.views import APIView

from alexandria_server.permissions.authentication import JWTAuthentication

from .helpers import get_user_repos


class PossibleRepositories(APIView):

    authentication_classes = (JWTAuthentication,)

    def get(self, request):

        repos = get_user_repos(request.user)

        data = {'repos': repos}
        return Response({'data': data})