from datasetApp.models import *
import zipfile
from django.core.files.base import ContentFile 
from .utils import *
import tarfile
from django.http import FileResponse
import tempfile

def remove_extension(filename):
    base_name = os.path.basename(filename)
    name, _ = os.path.splitext(base_name)
    return name

def upload_compressed_file(compressed_file, model):
    _, file_extension = os.path.splitext(compressed_file.name)
    if file_extension == '.zip':
        with zipfile.ZipFile(compressed_file, 'r') as zip_ref:
            process_compressed_files(zip_ref, model)
    elif file_extension == '.tar' or file_extension == '.gz':
        with tarfile.open(fileobj=compressed_file, mode='r') as tar_ref:
            process_compressed_files(tar_ref, model)
    else:
        pass

def process_compressed_files(compressed_ref, model):
    parent_folder = ModelFolder.objects.create(name=model.title, parent_folder=None, model=model)
    total_files = 0
    if isinstance(compressed_ref, zipfile.ZipFile):
        for file_name in compressed_ref.namelist():
            if not file_name.endswith('/'):
                total_files += 1
                create_file_from_compressed(compressed_ref, file_name, model, parent_folder)
    elif isinstance(compressed_ref, tarfile.TarFile):
        for file_info in compressed_ref.getmembers():
            if not file_info.isdir():
                total_files += 1
                create_file_from_compressed(compressed_ref, file_info, model, parent_folder)
    model.total_files = total_files
    model.save()



def create_file_from_compressed(compressed_ref, file_info, model, parent_folder):
    if isinstance(file_info, str):
        filename = os.path.basename(file_info)
    elif isinstance(file_info, (zipfile.ZipInfo, tarfile.TarInfo)):
        filename = os.path.basename(file_info.name)

    filename_without_extension, file_extension = os.path.splitext(filename)
    if isinstance(file_info, (zipfile.ZipInfo, tarfile.TarInfo)):
        folders = file_info.name.split('/')
        for folder in folders[:-1]:
            parent_folder = Folder.objects.get_or_create(name=folder, parent_folder=parent_folder, model=model)[0]
    else:
        folders = file_info.split('/')
        for folder in folders[:-1]:
            parent_folder = Folder.objects.get_or_create(name=folder, parent_folder=parent_folder, model=model)[0]

    if parent_folder is None:
        parent_folder = Folder.objects.get_or_create(name=model.title, parent_folder=parent_folder, model=model)[0]

    if isinstance(file_info, str):
        with compressed_ref.open(file_info) as file_obj:
            file_content = file_obj.read()
            file_size = len(file_content)
            model.size+=file_size
    else:
        with compressed_ref.extractfile(file_info) as file_obj:
            file_content = file_obj.read()
            file_size = file_info.size if hasattr(file_info, 'size') else len(file_content)
            model.size+=file_size
    model.save()
    new_file = ModelFile.objects.create(size=file_size, name=filename, folder=parent_folder)
    upload_path = os.path.join(f'{model.id}', filename_without_extension)
    new_file.file.save(upload_path, ContentFile(file_content))
    FileExtension.objects.create(file=new_file, extension=file_extension)
    
    

def download_zip(parent_folder):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    with zipfile.ZipFile(temp_file, 'w') as zip_file:
        add_folder_to_zip(parent_folder, zip_file)
    temp_file.close()
    temp_file = open(temp_file.name, 'rb')
    response = FileResponse(temp_file, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="{parent_folder.name}.zip"'
    return response

def add_folder_to_zip(folder, zip_file, parent_path=''):
    files = File.objects.filter(folder=folder)
    sub_folders = Folder.objects.filter(parent_folder=folder)
    for file in files:
        file_extension = file.fileextension.extension
        file_path = os.path.join(parent_path, f"{file.name}.{file_extension}")
        try:
            zip_file.write(file.file.path, arcname=file_path)
        except:
            pass
    for sub_folder in sub_folders:
        sub_folder_path = os.path.join(parent_path, sub_folder.name)
        add_folder_to_zip(sub_folder, zip_file, parent_path=sub_folder_path)
        
