from rest_framework import mixins, generics
from culinary.serializers import FridgeSerializer
from culinary.models import Fridge
from culinary.permissions import IsOwnerOrStaff


class FridgeList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    serializer_class = FridgeSerializer
    permission_classes = [IsOwnerOrStaff]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if not user.is_staff:
            return Fridge.objects.filter(user_id=user.id)

        return Fridge.objects.all()


class FridgeDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Fridge.objects.all()
    serializer_class = FridgeSerializer
    permission_classes = [IsOwnerOrStaff]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class FridgeEdit(
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView
):
    queryset = Fridge.objects.all()
    serializer_class = FridgeSerializer
    permission_classes = [IsOwnerOrStaff]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
