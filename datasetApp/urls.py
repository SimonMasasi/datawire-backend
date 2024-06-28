from . import views
from .views import *
from django.urls import path

urlpatterns = [
    
    path('datasets/<int:id>/delete/', DatasetDeleteView.as_view(), name='dataset_delete'),
    path('dataset-details/<int:id>/', DatasetDetails.as_view(), name='dataset-details'),
    path('dataset/list/', DatasetListView.as_view(), name='dataset-list'),
    path('dataset-downloads/<int:dataset_id>/', views.dataset_downloads_per_day, name='dataset-downloads'),
    path('download-dataset/<int:dataset_id>/', DownloadDatasetsFiles.as_view(), name='download-dataset'),
    path('datasets/downloads/update/<int:id>/', UpdateDatasetsDownloads.as_view(), name='update-datasets-downloads'),
    path('datasets/viewers/update/<int:id>/', UpdateDatasetsViewers.as_view(), name='update-datasets-viewers'),
    path('dataset-repo-upload/', RepositoryAndDatasetCreateView.as_view(), name='dataset-repo-upload'),
    path('delete_dataset/<int:pk>/', DatasetDeleteView.as_view(), name='delete_dataset'),
    path('delete-dataset-file/<int:pk>/', DatasetFileDelete.as_view(), name='delete-dataset'),
    path('domains/', DomainList.as_view()),
    path('folders/<int:parent_folder_id>/<int:dataset_id>/', FolderListAPIView.as_view(), name='folder-list'),
    path('files/<int:folder_id>/', FileListAPIView.as_view(), name='file-list'),
    path('upvote-dataset/', DatasetUpvote.as_view()),
    path('files/<int:file_id>/download/', views.download_file),
    path('files/<int:file_id>/view/', views.view_file),
    
]
