from django.urls import path
from . import views
from .views import CategoryListView, TaskCreateView, TaskDeleteView, TaskListView, TaskUpdateView, UserRegistrationView, UserLoginView, CategoryCreateView

urlpatterns = [
    # auth routes
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),

    # task routes
    path('tasks', TaskListView.as_view(), name='task-list'),
    path('task/create', TaskCreateView.as_view(), name='task-create'),
    path('tasks/<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('tasks/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),

    # categories route
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('category/create', CategoryCreateView.as_view(), name='category-create'),
]

