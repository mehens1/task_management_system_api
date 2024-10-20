from django.http import Http404, HttpResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from task_management.serializers import UserRegistrationSerializer
from task_management.serializers import UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import serializers
from .models import Task, Category
from task_management.serializers import TaskSerializer, CategorySerializer


def home(request):
    return HttpResponse("Welcome to the Task Management System API! This is Samson Meheni's ALX Capstone Project, you can login to continue!")

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response({
                'status': True,
                'status_code': status.HTTP_201_CREATED,
                'message': 'Registration Successful!',
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': False,
            'status_code': status.HTTP_400_BAD_REQUEST,
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(ObtainAuthToken):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            return Response({
                'status': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'error': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserRegistrationSerializer(user).data

        return Response({
                'status': True,
                'status_code': status.HTTP_202_ACCEPTED,
                'accessToken': token.key,
                'user': user_data
        }, status=status.HTTP_202_ACCEPTED)
    
    
class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                'status': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'No category found!',
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)
        serialized_data = self.get_serializer(queryset, many=True).data
        return Response({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Categories fetched successfully.',
                'data': serialized_data
        }, status=status.HTTP_200_OK)


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status': True,
            'status_code': status.HTTP_201_CREATED,
            'message': 'Category created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

class CategoryDeleteView(generics.DestroyAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Http404:
            return Response({
                'status': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Category not found or you do not have permission to delete it.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(category)
        return Response({
                'status': True,
                'status_code': status.HTTP_202_ACCEPTED,
                'message': 'Category deleted successfully.'
            }, status=status.HTTP_202_ACCEPTED)


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset.exists():
            return Response({
                'status': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'No tasks found!',
                'data': []
            }, status=status.HTTP_404_NOT_FOUND)
        
        serialized_data = self.get_serializer(queryset, many=True).data
        
        return Response({
                'status': True,
                'status_code': status.HTTP_200_OK,
                'message': 'Tasks fetched successfully.',
                'data': serialized_data
        }, status=status.HTTP_200_OK)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            'status': True,
            'status_code': status.HTTP_201_CREATED,
            'message': 'Task created successfully.',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    


class TaskUpdateView(generics.UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class TaskDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        try:
            task = self.get_object()
        except Http404:
            return Response({
                'status': False,
                'status_code': status.HTTP_404_NOT_FOUND,
                'message': 'Task not found or you do not have permission to delete it.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        self.perform_destroy(task)
        return Response({
                'status': True,
                'status_code': status.HTTP_202_ACCEPTED,
                'message': 'Task deleted successfully.'
            }, status=status.HTTP_202_ACCEPTED)