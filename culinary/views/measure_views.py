from django.db.models import Q
from rest_framework import viewsets
from culinary.serializers import MeasureSerializer
from culinary.models import Measure
from culinary.permissions import IsStaffOrReadOnly


class MeasureViewSet(viewsets.ModelViewSet):
    queryset = Measure.objects.all().order_by("name")
    serializer_class = MeasureSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        filters = []
        name = self.request.query_params.get("name")
        if name:
            filters.append(Q(name__contains=name))
        return Measure.objects.filter(*filters).order_by("name")
