from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import BondFilter
from .models import Bond
from .serializers import BondSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response("Hello World!")


class BondsViewSet(ModelViewSet):
    """
    A simple ViewSet for viewing and editing bonds.
    """

    serializer_class = BondSerializer
    permission_classes = (IsAuthenticated,)
    filterset_class = BondFilter

    def get_queryset(self):
        return Bond.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
