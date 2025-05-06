from django.utils import translation
from rest_framework import viewsets
from django.contrib.auth.models import Group
from a_base.serializers import GroupSerializer
from a_base.permissions import ReadOnlyOrAdmin

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [ReadOnlyOrAdmin]