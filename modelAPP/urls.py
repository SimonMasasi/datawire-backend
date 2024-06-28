from . import views
from .views import *
from django.urls import path

urlpatterns = [
    path('models/<int:id>/delete/', ModelDeleteView.as_view(), name='model_delete'),
    path('model-details/<int:id>/', ModelDetails.as_view(), name='model-details'),
    path('list/', ModelListView.as_view(), name='model-list'),
    path('model-downloads/<int:model_id>/', views.model_downloads_per_day, name='model-downloads'),
    path('download-model/<int:model_id>/', DownloadModelsFiles.as_view(), name='download-model'),
    path('models/downloads/update/<int:id>/', UpdateModelsDownloads.as_view(), name='update-models-downloads'),
    path('viewers/update/<int:id>/', UpdateModelsViewers.as_view(), name='update-models-viewers'),
    path('model-repo-upload/', RepositoryAndModelCreateView.as_view(), name='model-repo-upload'),
    path('delete_model/<int:pk>/', ModelDeleteView.as_view(), name='delete_model'),
    path('delete-model-file/<int:pk>/', ModelFileDelete.as_view(), name='delete-model'),
    path('domains/', DomainList.as_view()),
    path('upvote-model/', ModelUpvote.as_view()),
    path('folders/<int:parent_folder_id>/<int:model_id>/', ModelFolderListAPIView.as_view(), name='folder-list'),
    path('files/<int:folder_id>/', ModelFileListAPIView.as_view(), name='file-list'),
    path('files/<int:file_id>/download/', views.download_file),
    path('files/<int:file_id>/view/', views.view_file),
]
