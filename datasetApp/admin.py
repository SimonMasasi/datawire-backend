from django.contrib import admin
from .models import *

# Register your models here.
class RepositoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'scope', 'created_at', 'updated_at')
    list_filter = ('scope', 'created_at', 'updated_at')
    search_fields = ('name', 'owner__username')
    
admin.site.register(Repository, RepositoryAdmin)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Domain, DomainAdmin)

class DatasetAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'domain', 'repository', 'downloads', 'viewers')
admin.site.register(Dataset, DatasetAdmin)

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'dataset', 'parent_folder', 'created_at')
admin.site.register(Folder, FolderAdmin)

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'folder', 'created_at', 'file')
admin.site.register(File, FileAdmin)

class CollaboratorAdmin(admin.ModelAdmin):
    list_display = ('user', 'repository')
admin.site.register(Collaborator, CollaboratorAdmin)

class DatasetDownloadsAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'user', 'created_at')
admin.site.register(DatasetDownloads, DatasetDownloadsAdmin)

class DatasetViewersAdmin(admin.ModelAdmin):
    list_display = ('dataset', 'user', 'created_at')
admin.site.register(DatasetViewers, DatasetViewersAdmin)

admin.site.register(DatasetVote)
admin.site.register(FileExtension)
admin.site.register(Tag)
admin.site.register(Model)
admin.site.register(ModelFile)
admin.site.register(ModelFolder)
admin.site.register(ModelFileExtension)




@admin.register(ChatRoom)
class UserRoleAdmin(admin.ModelAdmin):
    list_display=['dataset']


@admin.register(ChatMessages)
class UserRoleAdmin(admin.ModelAdmin):
    list_display=['sender' , "chat"]