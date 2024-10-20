from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import serializers
from tasks.models import Task, Category


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True}
        }
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, attrs):
        if not attrs.get('first_name'):
            raise serializers.ValidationError({"first_name": "First Name is required."})
        if not attrs.get('last_name'):
            raise serializers.ValidationError({"last_name": "Last Name is required."})
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }



class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    email = serializers.CharField(required=False)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not username and not email:
            raise serializers.ValidationError("A username or email is required to login.")

        user = None
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            try:
                user = User.objects.get(email=email)
                user = authenticate(username=user.username, password=password)
            except User.DoesNotExist:
                raise serializers.ValidationError({"message": "No account found with that email."})

        if user is None or not user.is_active:
            raise serializers.ValidationError({"message": "Invalid credentials, please check and try again."})

        attrs['user'] = user
        return attrs
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']
        extra_kwargs = {
            'name': {'required': True}
        }


class TaskSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'is_reoccurring', 'created_at', 'updated_at',
            'user_id', 'completed_at', 'due_date', 'priority_level', 'status', 'category_id'
        ]
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'due_date': {'required': True},
            'category_id': {'required': True},
        }

        def validate_category(self, value):
            request_user = self.context['request'].user
            if value.user != request_user:
                raise serializers.ValidationError("This category does not belong to you.")
            return value
