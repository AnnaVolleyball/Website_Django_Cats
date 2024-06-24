from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Task
from .serializers import TaskSerializer


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     # user = self.request.user
    #     # return Task.objects.filter(user=user)
    #     return Task.objects.all()
