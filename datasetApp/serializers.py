from rest_framework import serializers
from .models import *
from authApp.serializers import CustomUserSerializer 
from modelAPP.models import *
from rest_framework import serializers
from .models import Repository, Dataset, Folder, File

class RepositorySerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField("get_my_owner")
    my_id = serializers.SerializerMethodField("my_id_get")
    class Meta:
        model = Repository
        fields = ['id', 'name', 'scope', 'created_at', 'updated_at' ,"my_id" , "owner"]

    def get_my_owner(self , obj):
        owner_model = RepositoryOwners.objects.last().owner
        serializer_class = CustomUserSerializer(owner_model).data
        
        return serializer_class
    
    def my_id_get(self,obj):
        return "heloo"
        

class FileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = ['extension']

class FileSerializer(serializers.ModelSerializer):
    file_extension = serializers.SerializerMethodField()
    size_with_unit = serializers.SerializerMethodField()

    def get_file_extension(self, obj):
        try:
            return obj.fileextension.extension
        except FileExtension.DoesNotExist:
            return None

    class Meta:
        model = File
        fields = ['id', 'folder', 'name', 'file', 'size_with_unit', 'size', 'created_at', 'file_extension']
    def get_size_with_unit(self, obj):
        size = obj.size
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024**2:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024**3:
            return f"{round(size / 1024**2, 2)} MB"
        else:
            return f"{round(size / 1024**3, 2)} GB"

class ModelFileExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileExtension
        fields = ['extension']

class ModelFileSerializer(serializers.ModelSerializer):
    file_extension = serializers.SerializerMethodField()
    size_with_unit = serializers.SerializerMethodField()

    def get_file_extension(self, obj):
        try:
            return obj.modelfileextension.extension
        except FileExtension.DoesNotExist:
            return None

    class Meta:
        model = File
        fields = ['id', 'name', 'file', 'size_with_unit', 'created_at', 'file_extension']
    def get_size_with_unit(self, obj):
        size = obj.size
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024**2:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024**3:
            return f"{round(size / 1024**2, 2)} MB"
        else:
            return f"{round(size / 1024**3, 2)} GB"
        
class FolderSerializer(serializers.ModelSerializer):
    files = FileSerializer(many=True, required=False)

    class Meta:
        model = Folder
        fields = ['id', 'dataset', 'name', 'parent_folder', 'created_at', 'files']

    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        folder = Folder.objects.create(**validated_data)
        for file_data in files_data:
            File.objects.create(folder=folder, **file_data)
        return folder

class ModelFolderSerializer(serializers.ModelSerializer):
    files = ModelFileSerializer(many=True, required=False)
    class Meta:
        model = ModelFolder
        fields = ['id', 'model', 'name', 'parent_folder', 'created_at', 'files']
    def create(self, validated_data):
        files_data = validated_data.pop('files', [])
        folder = ModelFolder.objects.create(**validated_data)
        for file_data in files_data:
            ModelFile.objects.create(folder=folder, **file_data)
        return folder
    
class DomainSerializer(serializers.ModelSerializer):
  class Meta:
    model = Domain
    fields = '__all__'
 
class ModelSerializer(serializers.ModelSerializer):
    domain = DomainSerializer()
    votes_count = serializers.SerializerMethodField()
    folders = FolderSerializer(many=True, required=False)
    repository = RepositorySerializer(read_only=True)
    class Meta:
        model = Model
        fields = '__all__'
    def get_votes_count(self, obj):
        return obj.model_votes.filter(isUpvoted=True).count()-obj.model_votes.filter(isUpvoted=False).count()
    


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']
        
class DatasetSerializer(serializers.ModelSerializer):
    domain = DomainSerializer()
    votes_count = serializers.SerializerMethodField()
    folders = FolderSerializer(many=True, required=False)
    size_with_unit = serializers.SerializerMethodField()
    repository = RepositorySerializer(read_only=True)
      # Optional field for repository association
    class Meta:
        model = Dataset
        fields = ['id', 'title', 'description', 'domain','total_files', 'repository', 'size_with_unit', 'downloads', 'viewers', 'created_at', 'folders', 'votes','votes_count']
    def create(self, validated_data):
        folders_data = validated_data.pop('folders', [])
        dataset = Dataset.objects.create(**validated_data)
        for folder_data in folders_data:
            files_data = folder_data.pop('files', [])
            folder = Folder.objects.create(dataset=dataset, **folder_data)
            for file_data in files_data:
                File.objects.create(folder=folder, **file_data)
        return dataset
    def get_votes_count(self, obj):
        return obj.votes.filter(isUpvoted=True).count()-obj.votes.filter(isUpvoted=False).count()
    def get_size_with_unit(self, obj):
        size = obj.size
        if size < 1024:
            return f"{size} bytes"
        elif size < 1024**2:
            return f"{round(size / 1024, 2)} KB"
        elif size < 1024**3:
            return f"{round(size / 1024**2, 2)} MB"
        else:
            return f"{round(size / 1024**3, 2)} GB"
        


class DatasetVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetVote
        fields = ['dataset', 'user', 'upvoted_at']
        read_only_fields = ['user', 'upvoted_at']

class ModelVoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelVote
        fields = ['model', 'user', 'upvoted_at', 'isUpvoted']
        read_only_fields = ['user', 'upvoted_at']
             
class DatasetFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatasetFeedback
        fields = ['id', 'content', 'user', 'dataset', 'created_at']
        read_only_fields = ['id', 'created_at']
        
# class FolderSerializer(serializers.ModelSerializer):
#   repository = RepositorySerializer()
#   parent = serializers.CharField(read_only=True)  # Use CharField for parent representation

#   class Meta:
#     model = Folder
#     fields = '__all__'

#   def to_representation(self, instance):
#       representation = super().to_representation(instance)
#       representation['parent'] = FolderSerializer(instance.parent).data if instance.parent else None  # Check for null parent
#       return representation

class CollaboratorSerializer(serializers.ModelSerializer):
  user = CustomUserSerializer()
  repository = RepositorySerializer()
  class Meta:
    model = Collaborator
    fields = '__all__'

# class DatasetSerializer(serializers.ModelSerializer):
#   domain = DomainSerializer()
#   repository = RepositorySerializer(read_only=True)  # Optional field for repository association

#   class Meta:
#     model = Dataset
#     fields = '__all__'


    


class DatasetAccessSerializer(serializers.ModelSerializer):
  dataset = DatasetSerializer()
  user = CustomUserSerializer()

  class Meta:
    model = DatasetAccess
    fields = '__all__'


class UserUploadSerializer(serializers.ModelSerializer):
  user = CustomUserSerializer()

  class Meta:
    model = UserUpload
    fields = '__all__'

# class ModelVersionSerializer(serializers.ModelSerializer):
#   model = ModelSerializer()

#   class Meta:
#     model = ModelVersion
#     fields = '__all__'

# class DatasetTagSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = DatasetTag
#     fields = '__all__'

# class ModelTagSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = ModelTag
#     fields = '__all__'

# class DatasetDataTagSerializer(serializers.ModelSerializer):
#   dataset = DatasetSerializer()
#   tag = DatasetTagSerializer()

#   class Meta:
#     model = DatasetDatasetTag
#     fields = '__all__'

# class ModelModelTagSerializer(serializers.ModelSerializer):
#   model = ModelSerializer()
#   tag = ModelTagSerializer()

#   class Meta:
#     model = ModelModelTag
#     fields = '__all__'

class DatasetRatingSerializer(serializers.ModelSerializer):
  user = CustomUserSerializer()
  dataset = DatasetSerializer()

  class Meta:
    model = DatasetRating
    fields = '__all__'
