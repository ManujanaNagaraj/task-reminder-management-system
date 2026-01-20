from rest_framework import generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from django.contrib.auth.models import User
from collections import defaultdict

class CalendarTaskView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        grouped_tasks = defaultdict(list)
        
        for task in tasks:
            serializer = TaskSerializer(task)
            date_str = task.due_date.isoformat()
            grouped_tasks[date_str].append(serializer.data)
            
        return Response(grouped_tasks)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
