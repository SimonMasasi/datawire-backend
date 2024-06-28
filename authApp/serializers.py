from rest_framework import serializers # Assuming CustomUser inherits from AbstractUser
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datasetApp.models import *

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
class RoleSerializer(serializers.ModelSerializer):
  class Meta:
    model = Role
    fields = '__all__'
    
class CustomUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = '__all__'  # Include custom fields
    extra_kwargs = {
        'password': {'write_only': True},
    }
class UserDataSerializer(serializers.ModelSerializer):
  class Meta:
    model = CustomUser
    fields = ("id", "username", "email", "is_active", 'first_name', 'last_name')
      
class VerificationSerializer(serializers.Serializer):
    # verification_code = serializers.CharField(max_length=6)
    class Meta:
        model = CustomUser
        fields = ('verification_code', 'email')
        
# User = get_user_model()
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password')
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['email'],
            verification_code ="",
        )
        return user
    
class UserRolesSerializer(serializers.ModelSerializer):
    user = UserDataSerializer()
    # role = RoleSerializer()
    class Meta:
        model = UserRole
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    repositories = serializers.SerializerMethodField()
    models = serializers.SerializerMethodField()
    datasets = serializers.SerializerMethodField()
    roles = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'age', 'verification_code', 'roles', 'repositories', 'models', 'datasets']

    def get_repositories(self, obj):
        repositories = Repository.objects.filter(owner=obj)
        repository_data = [{'name': repo.name, 'scope': repo.scope} for repo in repositories]
        return repository_data

    def get_models(self, obj):
        models = Model.objects.filter(repository__owner=obj)
        model_data = [{'name': model.title, 'description': model.description} for model in models]
        return model_data

    def get_roles(self, obj):
        roles = UserRole.objects.filter(user=obj)
        role_data = [{'name': role.role.name, 'id': role.role.id} for role in roles]
        return role_data

    def get_datasets(self, obj):
        datasets = Dataset.objects.filter(repository__owner=obj)
        dataset_data = [{'id': dataset.id, 'title': dataset.title, 'description': dataset.description, 'downloads': dataset.downloads, 'viewers': dataset.viewers} for dataset in datasets]
        return dataset_data