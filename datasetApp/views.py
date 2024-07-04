from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status  
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
import os
from django.http import HttpResponse, JsonResponse
from django.db.models import Count
from django.db.models.functions import TruncDate
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
import magic
from django.shortcuts import get_object_or_404
from django.conf import settings
from .utils import *

def dataset_downloads_per_day(request, dataset_id):
    downloads_per_day = DatasetDownloads.objects.filter(dataset_id=dataset_id)\
                                                .annotate(date=TruncDate('created_at'))\
                                                .values('date')\
                                                .annotate(download_count=Count('id'))\
                                                .order_by('date')
    data = [{'date': item['date'].strftime('%m-%d'), 'download_count': item['download_count']} for item in downloads_per_day]
    print(data)
    return JsonResponse(data, safe=False)

class DownloadDatasetsFiles(APIView):
    permission_classes = [AllowAny]

    def get(self, request, dataset_id):
        parent_folder = Folder.objects.get(dataset__id=dataset_id, parent_folder=None)
        response = download_zip(parent_folder)
        dataset = Dataset.objects.get(pk=dataset_id)
        dataset.downloads += 1
        dataset.save()
        user = request.user
        download = DatasetDownloads.objects.create(dataset=dataset, user=user if user.is_authenticated else None)
        download.save()
        return response

class DatasetDeleteView(APIView):
    def delete(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        dataset.delete()
        return Response({'message': 'Dataset deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class DatasetFileDelete(APIView):
    def delete(self, request, pk):
        try:
            dataset = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        dataset.delete()
        return Response({'message': 'Dataset deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class DomainList(APIView):
    def get(self, request):
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return Response(serializer.data)
    
class DatasetUpvote(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        dataset=Dataset.objects.get(id=request.data['dataset'])
        datasetUpvote=DatasetVote.objects.get_or_create(user=request.user, dataset=dataset)[0]
        # datasetUpvote.save()
        datasetUpvote.isUpvoted = not datasetUpvote.isUpvoted
        datasetUpvote.save()
        return Response({'message':"Successfully"})  
    
class RepositoryAndDatasetCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Enforce authentication

    def post(self, request):
        data = request.data
        user = request.user
        repository = Repository.objects.create(
            scope=data['scope'],
            name=data['repo_name']
        )

        RepositoryOwners.objects.create(
            owner=request.user,
            repository= repository
        )

        domain = Domain.objects.filter(name=data['domain']).first()
        dataset = Dataset.objects.create(
            title=data['title'],
            description=data['description'],
            domain=domain,
            repository=repository,
        )
        tags_data = data.pop('tags', [])
        tags = []
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            tags.append(tag)
        dataset.tags.set(tags)
        dataset.save()
        zipped_files = request.FILES.getlist('files')
        for compressed_file in zipped_files:
            upload_compressed_file(compressed_file, dataset)
        return JsonResponse({'status': 'success'})


class UpdateDatasetsDownloads(APIView):
    def get(self, request, id):
        dataset = Dataset.objects.get(id=id)
        dataset.downloads += 1
        dataset.save()
        return Response({'message':'downloads updated'})
        
class UpdateDatasetsViewers(APIView):
    permission_classes = [AllowAny]     # Enforce authentication
    def get(self, request, id):
        if id:
            dataset = Dataset.objects.get(id=id)
            dataset.viewers += 1
            dataset.save()
            try:
                DatasetViewers.objects.create(user=request.user, dataset=dataset)
            except:
                DatasetViewers.objects.create(dataset=dataset)
            return Response({'message':'downloads updated'})
        
class DatasetDeleteView(APIView):
    def delete(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
        dataset.delete()
        return Response({'message': 'Dataset deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class DatasetListView(APIView):
    permission_classes = [AllowAny]
    class CustomPagination(PageNumberPagination):
        page_size = 15  # Number of items per page
        page_size_query_param = 'page_size'
        max_page_size = 100
    def get(self, request):
        query = request.query_params.get('query', None)
        categories = request.query_params.getlist('categories')
        is_my_dataset = (request.query_params.get('my_dataset'))
        print(is_my_dataset)
        if is_my_dataset == 'true':
            datasets = Dataset.objects.filter(repository__owner_repository__owner__id=request.user.id)
        elif query and is_my_dataset=='false':
            datasets = Dataset.objects.filter(repository__scope="Public").filter(
                Q(title__icontains=query) |
                Q(domain__name__icontains=query) |
                Q(repository__owner_repository__owner__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).annotate(votes_count=Count('votes')).distinct().order_by('-votes_count')
        else:
            datasets = Dataset.objects.annotate(votes_count=Count('votes')).filter(repository__scope="Public").order_by('-votes_count')
        if categories and categories != ['']:
            print("Yes")
            categories_list = categories[0].split(',')
            datasets = datasets.filter(domain__name__in=categories_list)
        total_count = datasets.count()
        paginator = self.CustomPagination()
        print(datasets)
        paginated_data = paginator.paginate_queryset(datasets, request)
        serializer = DatasetSerializer(paginated_data, many=True)
        response_data = {
            'count': total_count,
            'results': serializer.data
        }
        return paginator.get_paginated_response(response_data)
    
class DatasetDetails(APIView):
    def get(self, request, id):
        dataset = Dataset.objects.get(id=id)
        dataset_files = File.objects.filter(folder__dataset=dataset)[:6]  # Retrieve related files

        # Serialize dataset and files together
        serializer = DatasetSerializer(dataset)
        files_serializer = FileSerializer(dataset_files, many=True)

        data = {
            'dataset': serializer.data,
            'files': files_serializer.data
        }
        return Response(data)

class FolderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class FolderListAPIView(generics.ListAPIView):
    serializer_class = FolderSerializer
    pagination_class = FolderPagination
    def get_queryset(self):
        parent_folder_id = self.kwargs.get('parent_folder_id')
        if parent_folder_id > 0:
            return Folder.objects.filter(parent_folder__id=parent_folder_id)
        else:
            dataset_id=self.kwargs.get('dataset_id')
            return Folder.objects.filter(dataset__id=dataset_id, parent_folder=None)

class FilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class FileListAPIView(generics.ListAPIView):
    serializer_class = FileSerializer
    pagination_class = FilePagination

    def get_queryset(self):
        folder_id = self.kwargs.get('folder_id')
        return File.objects.filter(folder__id=folder_id)

def download_file(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    try:
        file_extension = FileExtension.objects.get(file=file_obj).extension
        print(file_extension+"Exists")
    except FileExtension.DoesNotExist:
        file_extension = ""
        print("Not exists")
    file_path = os.path.join(settings.MEDIA_ROOT, file_obj.file.name)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        return response


def view_file(request, file_id):
    file_obj = get_object_or_404(File, pk=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_obj.file.name)
    mime = magic.Magic(mime=True)
    content_type = mime.from_file(file_path)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        return response
