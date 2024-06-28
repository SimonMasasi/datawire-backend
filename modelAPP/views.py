from rest_framework.response import Response
from datasetApp.models import *
from datasetApp.serializers import *
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

def model_downloads_per_day(request, model_id):
    downloads_per_day = ModelDownloads.objects.filter(model_id=model_id)\
                                                .annotate(date=TruncDate('created_at'))\
                                                .values('date')\
                                                .annotate(download_count=Count('id'))\
                                                .order_by('date')
    data = [{'date': item['date'].strftime('%m-%d'), 'download_count': item['download_count']} for item in downloads_per_day]
    print(data)
    return JsonResponse(data, safe=False)

class DownloadModelsFiles(APIView):
    permission_classes = [AllowAny]

    def get(self, request, model_id):
        parent_folder = ModelFolder.objects.get(model__id=model_id, parent_folder=None)
        response = download_zip(parent_folder)
        model = Model.objects.get(pk=model_id)
        model.downloads += 1
        model.save()
        user = request.user
        download = ModelDownloads.objects.create(model=model, user=user if user.is_authenticated else None)
        download.save()
        return response

class ModelDeleteView(APIView):
    def delete(self, request, pk):
        try:
            model = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
        model.delete()
        return Response({'message': 'Model deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class ModelFileDelete(APIView):
    def delete(self, request, pk):
        try:
            model = ModelFile.objects.get(pk=pk)
        except ModelFile.DoesNotExist:
            return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
        model.delete()
        return Response({'message': 'Model deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    
class DomainList(APIView):
    def get(self, request):
        domains = Domain.objects.all()
        serializer = DomainSerializer(domains, many=True)
        return Response(serializer.data)
    
class ModelUpvote(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        model=Model.objects.get(id=request.data['model'])
        modelUpvote=ModelVote.objects.get_or_create(user=request.user, model=model)[0]
        # modelUpvote.save()
        modelUpvote.isUpvoted = not modelUpvote.isUpvoted
        modelUpvote.save()
        return Response({'message':"Successfully"})  
    
class RepositoryAndModelCreateView(APIView):
    permission_classes = [IsAuthenticated]  # Enforce authentication

    def post(self, request):
        data = request.data
        user = request.user
        repository = Repository.objects.create(
            scope=data['scope'],
            owner=request.user,
            name=data['repo_name']
        )
        domain = Domain.objects.filter(name=data['domain']).first()
        model = Model.objects.create(
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
        model.tags.set(tags)
        model.save()
        zipped_files = request.FILES.getlist('files')
        for compressed_file in zipped_files:
            upload_compressed_file(compressed_file, model)
        return JsonResponse({'status': 'success'})


class UpdateModelsDownloads(APIView):
    def get(self, request, id):
        model = Model.objects.get(id=id)
        model.downloads += 1
        model.save()
        return Response({'message':'downloads updated'})
        
class UpdateModelsViewers(APIView):
    permission_classes = [AllowAny]     # Enforce authentication
    def get(self, request, id):
        if id:
            model = Model.objects.get(id=id)
            model.viewers += 1
            model.save()
            try:
                ModelViewers.objects.create(user=request.user, model=model)
            except:
                ModelViewers.objects.create(model=model)
            return Response({'message':'downloads updated'})
        
class ModelDeleteView(APIView):
    def delete(self, request, pk):
        try:
            model = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return Response({'error': 'Model not found'}, status=status.HTTP_404_NOT_FOUND)
        model.delete()
        return Response({'message': 'Model deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class ModelListView(APIView):
    permission_classes = [AllowAny]
    class CustomPagination(PageNumberPagination):
        page_size = 15
        page_size_query_param = 'page_size'
        max_page_size = 100
    def get(self, request):
        query = request.query_params.get('query', None)
        categories = request.query_params.getlist('categories')
        is_my_model = (request.query_params.get('my_model'))
        print(is_my_model)
        if is_my_model == 'true':
            models = Model.objects.filter(repository__owner__id=request.user.id)
        elif query and is_my_model=='false':
            models = Model.objects.filter(repository__scope="Public").filter(
                Q(title__icontains=query) |
                Q(domain__name__icontains=query) |
                Q(repository__owner__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).annotate(votes_count=Count('votes')).distinct().order_by('-votes_count')
        else:
            models = Model.objects.annotate(votes_count=Count('model_votes')).filter(repository__scope="Public").order_by('-votes_count')
        if categories and categories != ['']:
            print("Yes")
            categories_list = categories[0].split(',')
            models = models.filter(domain__name__in=categories_list)
        total_count = models.count()
        paginator = self.CustomPagination()
        print(models)
        paginated_data = paginator.paginate_queryset(models, request)
        serializer = ModelSerializer(paginated_data, many=True)
        response_data = {
            'count': total_count,
            'results': serializer.data
        }
        return paginator.get_paginated_response(response_data)
    
class ModelDetails(APIView):
    def get(self, request, id):
        model = Model.objects.get(id=id)
        model_files = ModelFile.objects.filter(folder__model=model)[:6]  # Retrieve related files

        # Serialize model and files together
        serializer = ModelSerializer(model)
        files_serializer = ModelFileSerializer(model_files, many=True)

        data = {
            'model': serializer.data,
            'files': files_serializer.data
        }
        return Response(data)

class ModelFolderPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class ModelFolderListAPIView(generics.ListAPIView):
    serializer_class = ModelFolderSerializer
    pagination_class = ModelFolderPagination
    def get_queryset(self):
        parent_folder_id = self.kwargs.get('parent_folder_id')
        if parent_folder_id > 0:
            return ModelFolder.objects.filter(parent_folder__id=parent_folder_id)
        else:
            model_id=self.kwargs.get('model_id')
            return ModelFolder.objects.filter(model__id=model_id, parent_folder=None)

class ModelFilePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class ModelFileListAPIView(generics.ListAPIView):
    serializer_class = ModelFileSerializer
    pagination_class = ModelFilePagination

    def get_queryset(self):
        folder_id = self.kwargs.get('folder_id')
        return ModelFile.objects.filter(folder__id=folder_id)

def download_file(request, file_id):
    file_obj = get_object_or_404(ModelFile, pk=file_id)
    try:
        file_extension = ModelFileExtension.objects.get(file=file_obj).extension
        print(file_extension+"Exists")
    except ModelFileExtension.DoesNotExist:
        file_extension = ""
        print("Not exists")
    file_path = os.path.join(settings.MEDIA_ROOT, file_obj.file.name)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.file.name}"'
        return response


def view_file(request, file_id):
    file_obj = get_object_or_404(ModelFile, pk=file_id)
    file_path = os.path.join(settings.MEDIA_ROOT, file_obj.file.name)
    mime = magic.Magic(mime=True)
    content_type = mime.from_file(file_path)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read(), content_type=content_type)
        return response
