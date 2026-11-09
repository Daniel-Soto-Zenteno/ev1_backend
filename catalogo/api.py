from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Perfume
from .serializers import PerfumeSerializer


class PerfumeViewSet(ModelViewSet):
    """Consulta autenticada; escritura reservada a usuarios administradores."""

    queryset = Perfume.objects.all()
    serializer_class = PerfumeSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']

    def get_permissions(self):
        permissions = [IsAuthenticated()]
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            permissions.append(IsAdminUser())
        return permissions
