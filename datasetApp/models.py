from django.db import models  # Assuming user authentication
from authApp.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
import os

class Repository(models.Model):
    scope_choices = (
          ('Private', 'Private'),
          ('Public', 'Public')
      )
    name = models.CharField(max_length=50)
    scope = models.CharField(choices=scope_choices, max_length=15, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
      return self.name
    
class RepositoryOwners(models.Model):
    repository  = models.ForeignKey(Repository , on_delete=models.CASCADE , related_name="owner_repository")
    owner = models.ForeignKey(CustomUser, on_delete = models.CASCADE , related_name="repository_owner")




class Domain(models.Model):
  """Represents a domain of data (e.g., image recognition, NLP)."""
  name = models.CharField(max_length=255, unique=True)
  
  def __str__(self):
    return self.name
  
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
      
class Dataset(models.Model):
  """Represents a dataset within the repository in a ."""
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
  repository=models.ForeignKey(Repository, on_delete=models.CASCADE, blank=True, null=True)
  downloads=models.IntegerField(default=0)
  viewers=models.IntegerField(default=0)
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateField(auto_now_add=True)
  tags = models.ManyToManyField(Tag)
  total_files=models.IntegerField(default=14)
  size=models.PositiveIntegerField(default=0)

  def __str__(self):
    return f"{self.title} ({self.domain})"

class DatasetVote(models.Model):
    """Represents a vote for a dataset."""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    upvoted_at = models.DateTimeField(auto_now_add=True)
    isUpvoted = models.BooleanField(default=True)

    class Meta:
        unique_together = ['dataset', 'user'] 
        
class Folder(models.Model):
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Collaborator(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    repository=models.ForeignKey(Repository, on_delete=models.CASCADE)    
    
class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='datasets/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    size=models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name 

class FileExtension(models.Model):
    file = models.OneToOneField(File, on_delete=models.CASCADE)
    extension = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.file} - {self.extension}"
      
class DatasetDownloads(models.Model):
  dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class DatasetViewers(models.Model):
  dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
class Model(models.Model):
  """Represents a pre-trained model in the repository."""
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  downloads=models.IntegerField(default=0)
  viewers=models.IntegerField(default=0)
  dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
  repository=models.ForeignKey(Repository, on_delete=models.CASCADE, blank=True, null=True)
  architecture = models.CharField(max_length=255, blank=True)  # Model architecture (e.g., ResNet-50)
  framework = models.CharField(max_length=255, blank=True)  # Framework used (e.g., TensorFlow, PyTorch)
  performance_metrics = models.JSONField(blank=True, null=True)  # Stores metrics on benchmark datasets
  file = models.FileField(upload_to='models/', blank=True, null=True)
  created_at = models.DateField(default=timezone.now)
  updated_at = models.DateField(default=timezone.now)
  domain = models.ForeignKey(Domain, on_delete=models.CASCADE, null=True)
  tags = models.ManyToManyField(Tag)
  total_files=models.IntegerField(default=14)
  size=models.PositiveIntegerField(default=0)

  def __str__(self):
    return f"{self.title} ({self.architecture})"
  
class ModelVote(models.Model):
    """Represents a vote for a dataset."""
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name='model_votes')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    upvoted_at = models.DateTimeField(auto_now_add=True)
    isUpvoted = models.BooleanField(default=True)

    class Meta:
        unique_together = ['model', 'user'] 
        
class ModelFolder(models.Model):
    model = models.ForeignKey(Model, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name    
          
class ModelFile(models.Model):
    folder = models.ForeignKey(ModelFolder, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='models/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    size=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name 

class ModelFileExtension(models.Model):
    file = models.OneToOneField(ModelFile, on_delete=models.CASCADE)
    extension = models.CharField(max_length=10)
    def __str__(self):
        return f"{self.file} - {self.extension}"
  
class DatasetAccess(models.Model):
  """Controls user access to specific datasets."""
  dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  access_level = models.CharField(max_length=255)  # Define access levels (e.g., read, edit)

  class Meta:
    unique_together = ('dataset', 'user')
    
class ModelDownloads(models.Model):
  model = models.ForeignKey(Model, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class ModelViewers(models.Model):
  model = models.ForeignKey(Model, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
class ModelAccess(models.Model):
  """Controls user access to specific models."""
  model = models.ForeignKey(Model, on_delete=models.CASCADE)
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  access_level = models.CharField(max_length=255)  # Define access levels (e.g., download, use)

  class Meta:
    unique_together = ('model', 'user')

class DatasetFeedback(models.Model):
  """Stores user feedback on datasets or models."""
  content = models.TextField()
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)

class DatasetRating(models.Model):
  """Stores user ratings for datasets."""
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
  rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Excellent'), (5, 'Outstanding')])
  created_at = models.DateTimeField(auto_now_add=True)

  class Meta:
    unique_together = ('user', 'dataset')

class ModelRating(models.Model):
  """Stores user ratings for models."""
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  model = models.ForeignKey(Model, on_delete=models.CASCADE)
  rating = models.IntegerField(choices=[(1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Excellent'), (5, 'Outstanding')])
  created_at = models.DateTimeField(auto_now_add=True)
  class Meta:
    unique_together = ('user', 'model')

class UserUpload(models.Model):
  """Represents user-uploaded datasets or models."""
  user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
  upload_type = models.CharField(max_length=255, choices=[('dataset', 'Dataset'), ('model', 'Model')])
  file = models.FileField(upload_to='uploads/')  # Store uploaded file
  description = models.TextField(blank=True)
  submitted_at = models.DateTimeField(auto_now_add=True)
  # Add fields for approval status, review process (if applicable)

  def __str__(self):
    return f"{self.user.username} - {self.upload_type} Upload ({self.id})"
  



class ChatRoom(models.Model):
    dataset = models.ForeignKey(Dataset , on_delete=models.CASCADE , related_name="receiver")
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.dataset}'
    

class ChatMessages(models.Model):
    message = models.CharField(default='' , max_length=9000)
    sender = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name="sender")
    chat = models.ForeignKey(ChatRoom , on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.chat} - {self.sender}'
    


class ModelsChatRoom(models.Model):
    model = models.ForeignKey(Model , on_delete=models.CASCADE , related_name="model")
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.model}'
    

class ModelChatMessages(models.Model):
    message = models.CharField(default='' , max_length=9000)
    sender = models.ForeignKey(CustomUser , on_delete=models.CASCADE , related_name="sender_model")
    chat = models.ForeignKey(ModelsChatRoom , on_delete=models.CASCADE)
    created_date = models.DateField(auto_now=True)

    def __str__(self):
        return f'{self.chat} - {self.sender}'