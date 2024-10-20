from django.urls import path
from .views import CategoryListView, TaskCreateView, TaskDeleteView, TaskListView, TaskUpdateView, UserRegistrationView, UserLoginView, CategoryCreateView, CategoryDeleteView, CategoryUpdateView

urlpatterns = [

    # auth routes
    path('register', UserRegistrationView.as_view(), name='register'),
    path('login', UserLoginView.as_view(), name='login'),

    # task routes
    path('tasks', TaskListView.as_view(), name='task-list'),
    path('task/create', TaskCreateView.as_view(), name='task-create'),
    path('task/<int:pk>/update', TaskUpdateView.as_view(), name='task-update'),
    path('task/<int:pk>/delete', TaskDeleteView.as_view(), name='task-delete'),

    # categories route
    path('categories', CategoryListView.as_view(), name='category-list'),
    path('category/create', CategoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/delete', CategoryDeleteView.as_view(), name='category-delete'),
    path('category/<int:pk>/update', CategoryUpdateView.as_view(), name='category-update'),
]

