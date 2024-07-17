from datetime import timedelta
import json
from django.utils import timezone
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from datasetApp.models import *
from datasetApp.serializers import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated 
from .models import *
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from django.core.mail import send_mail
from django.db.models import Count
from django.db.models.functions import TruncDay
from rest_framework.exceptions import ValidationError
from django.http import HttpRequest
from .mailUtils import EmailNotifications

# Import your User model and UserRegistrationSerializer

class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            user.generate_verification_code()
            user.is_verified = False
            user.save()

            body = {
                'receiver_details': user.email,
                'user': user,
                'subject': "Verify Account Email"
            }

            EmailNotifications.send_email_notification(html_template="confirm_pass.html" ,emailBody=body )

            return Response({'email': f'{user.email}'})  # Include token
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_verification_email(user):
  subject = 'Email Verification'
  message = f'Your verification code is: {user.verification_code}'
  from_email = 'tensonmtawa@yahoo.com'   
  recipient_list = [user.email]
  send_mail(subject, message, from_email, recipient_list, fail_silently=False)
  
def send_email_view(request):
    subject = "greatings"
    message = "tell me"
    recipient = 'mtawaega@gmail.com'
    send_mail(subject, message, 'tensonmtawa@yahoo.com', [recipient], fail_silently=False)
    print("sent")
    return HttpResponse("sent")

class UserVerificationView(APIView):
  def post(self, request):
    serializer = VerificationSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
      email = 'mtawaega@gmail.com'
      code = "oPZIc4"
      user = CustomUser.objects.get(verification_code=code, email=email)
      if user:
        print("Available")
        user.is_active = True
        user.save()
        return Response({'message': 'success'}, status=status.HTTP_200_OK)
      else:
        return Response({'message': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response({'error': 'Please provide both username and password'}, status=400)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_roles = UserRole.objects.filter(user=user)
            roles_data = []
            for user_role in user_roles:
                roles_data.append(user_role.role.name)

            token, _ = Token.objects.get_or_create(user=user)
            user_data = CustomUserSerializer(user).data  # Adjust serializer as needed
            return Response({**user_data, 'token': token.key, 'roles':roles_data})  # Include token
        else:
            return Response({'error': 'Invalid credentials'}, status=200)
        

class VerifyAccount(APIView):
    def post(self, request):
        token = request.data.get('verification_code')
        if token is None:
            return Response({'message': 'Please provide token' , "status":False}, status=200)
        user = CustomUser.objects.filter(verification_code = token , is_verified = False).first()
        if user is not None:
            user.is_verified = True
            user.save()

            login(request, user)
            user_roles = UserRole.objects.filter(user=user)
            roles_data = []
            for user_role in user_roles:
                roles_data.append(user_role.role.name)

            token, _ = Token.objects.get_or_create(user=user)
            user_data = CustomUserSerializer(user).data 
            return Response({"status":True , "message":"account Activated Successfully" , "userData":user_data} ,status=200) 
        else:
            return Response({'message': 'Invalid token' , "status":False}, status=200)
        

class DatasetShareView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            dataset_id = request.data.get('dataset_id')

            dataset = Dataset.objects.filter(pk=dataset_id).first()
            user_data = CustomUser.objects.filter(pk=user_id).first()


            if RepositoryOwners.objects.filter(
                owner=user_data,
                repository=dataset.repository
            ).first():
                return Response({"error":True , "message":"You have already shared this Dataset with this user"})

            RepositoryOwners.objects.update_or_create(
                owner=user_data,
                repository=dataset.repository
            )
            return Response({'error': False}, status=200)
        except Exception as e:
            print(e)
            return Response({"error":True , "message":"problem ocurred while adding user"})
        


class ModelShareView(APIView):
    def post(self, request):
        try:
            user_id = request.data.get('user_id')
            model_id = request.data.get('model_id')

            model = Model.objects.filter(pk=model_id).first()
            user_data = CustomUser.objects.filter(pk=user_id).first()

            if RepositoryOwners.objects.filter(
                owner=user_data,
                repository=model.repository
            ).first():
                return Response({"error":True , "message":"You have already shared this model with this user"})


            RepositoryOwners.objects.update_or_create(
                owner=user_data,
                repository=model.repository
            )
            return Response({'error': False}, status=200)
        except Exception as e:
            print(e)
            return Response({"error":True , "message":"problem ocurred while adding user"})

class LogoutView(APIView):
    authentication_classes = [SessionAuthentication]  # Only allow authenticated users to logout
    def post(self, request):
        logout(request)  # Logout the user
        return Response({'message': 'Successfully logged out'}, status=200)
    
class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data.get('old_password')
            new_password = serializer.validated_data.get('new_password')
            user = request.user
            if not user.check_password(old_password):
                raise ValidationError({'old_password': ['Incorrect password.']})
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserListView(APIView):
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)

class RoleUserListView(APIView):
    def get(self, request, role_id):
        users = UserRole.objects.filter(role__id = role_id)
        serializer = UserRolesSerializer(users, many=True)
        return Response(serializer.data)
     

class RegionsListView(APIView):
    def get(self, request):
        regions = Regions.objects.all()
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data)
    
class UserRepository(APIView):
    def get(self, request, user_id):
        datasets = Dataset.objects.filter(repository__owner__id = user_id)
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)
    

class RoleListView(APIView):
    def get(self, request):
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

class AddRole(APIView):
    def post(self, request, format=None):
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddRoleUserView(APIView):
    def post(self, request):
        user = CustomUser.objects.get(id=request.data['userId'])
        role = Role.objects.get(id=request.data['roleId'])
        UserRole.objects.create(user=user, role=role)
        return Response({'message': 'Successfully created'}, status=200)
    
class UserDeleteAPIView(APIView):
    def delete(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserDeactivateAPIView(APIView):
    def post(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.is_active = False  # Deactivate the user
        user.save()
        return Response(status=status.HTTP_200_OK)

class UserActivateAPIView(APIView):
    def post(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.is_active = True  # Deactivate the user
        user.save()
        return Response(status=status.HTTP_200_OK)
    
class UserEditAPIView(APIView):
    def patch(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailAPIView(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(pk=user_id)
            serializer = UserDataSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except user.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserProfileAPIView(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = CustomUser.objects.get(pk=user_id)
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class DashboardSummary(APIView):
    def get(self, request):
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)

        dataset_downloads_data = DatasetDownloads.objects \
        .filter(created_at__gte=thirty_days_ago) \
        .annotate(day=TruncDay('created_at')) \
        .values('day') \
        .annotate(download_count=Count('id')) \
        .order_by('day')
        model_downloads_data = ModelDownloads.objects \
        .filter(created_at__gte=thirty_days_ago) \
        .annotate(day=TruncDay('created_at')) \
        .values('day') \
        .annotate(download_count=Count('id')) \
        .order_by('day')
        total_users = CustomUser.objects.count()
        total_repositories = Repository.objects.count()
        roles_summary = UserRole.objects.values('role__name').annotate(user_count=Count('user'))
        datasets_summary = Dataset.objects.values('domain__name').annotate(count=models.Count('id'))
        model_summary = Model.objects.values('domain__name').annotate(count=models.Count('id'))
        data = {
            'total_users': total_users,
            'total_repositories': total_repositories,
            'roles_summary': roles_summary,
            'datasets_summary': datasets_summary,
            'dataset_downloads_data':dataset_downloads_data,
            'model_downloads_data':model_downloads_data,
            'model_summary':model_summary
        }

        return Response(data)

class LandingPageDAta(APIView):
    def get(self, request, format=None):
        today = timezone.now().date()
        thirty_days_ago = today - timedelta(days=30)
        total_downloads = DatasetDownloads.objects.count()
        total_viewers = DatasetViewers.objects.count()
        total_users=CustomUser.objects.count()
        dataset_downloads_data = DatasetDownloads.objects \
        .filter(created_at__gte=thirty_days_ago) \
        .annotate(day=TruncDay('created_at')) \
        .values('day') \
        .annotate(download_count=Count('id')) \
        .order_by('day')
        data = {
            "total_downloads": total_downloads,
            "total_viewers": total_viewers,
            "total_users":total_users,
            "dataset_downloads_data":dataset_downloads_data
        }
        return Response(data)
    

class GetChatroom(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request:HttpRequest, format=None):
        user = request.user

        if user is None:
            return Response(data={"detail":"unauthenticated"} , status=403)

        data_from_body = json.loads(request.body)

        dataset_id = data_from_body["data_set_id"]


        dataset = Dataset.objects.filter(pk = dataset_id).first()
        if dataset is None:
            data = {
                "detail":"data set was not found"
            }

            return Response(data , status=400)
        
        chat_room = ChatRoom.objects.filter(dataset = dataset).first()

        if chat_room is None:
            if chat_room is None:
                chat_room = ChatRoom.objects.create(
                        dataset= dataset
                )


        chat_messages = ChatMessages.objects.filter(chat = chat_room)

        message_list = []

        for message in chat_messages:
            message_list.append(
                {
                    "message":message.message,
                    "sender":message.sender.email,
                    "is_from_sender":message.sender==user,
                    "date_created":message.created_date
                }
            )

        return Response(data=message_list , status=200)
    



class CreateChatroom(APIView):


    permission_classes = [IsAuthenticated]




    def post(self, request:HttpRequest, format=None):
        user = request.user

        if user is None:
            return Response(data={"detail":"unauthenticated"} , status=403)
        

        data_from_body = json.loads(request.body)

        
        dataset_id = data_from_body["data_set_id"]

        message = data_from_body["message"]

        dataset = Dataset.objects.filter(pk = dataset_id).first()
        if dataset is None:
            data = {
                "detail":"data set was not found"
            }

            return Response(data , status=400)
        
        chat_room = ChatRoom.objects.filter(dataset=dataset).first()


        if chat_room is None:
            if chat_room is None:
                chat_room = ChatRoom.objects.create(
                        dataset=dataset
                )


        created_message = ChatMessages.objects.create(chat = chat_room , message=message , sender=user)

        data = {
            "message":created_message.message,
            "sender":created_message.sender.email,
            "is_from_sender":created_message.sender==user,
            "date_created":created_message.created_date
        }


        return Response(data=data , status=200)
    





class GetModelChatroom(APIView):

    permission_classes = [IsAuthenticated]


    def post(self, request:HttpRequest, format=None):
        user = request.user

        if user is None:
            return Response(data={"detail":"unauthenticated"} , status=403)

        data_from_body = json.loads(request.body)

        model_id = data_from_body["model_id"]


        model = Model.objects.filter(pk = model_id).first()
        if model is None:
            data = {
                "detail":"model set was not found"
            }

            return Response(data , status=400)
        
        chat_room = ModelsChatRoom.objects.filter(model = model).first()

        if chat_room is None:
            if chat_room is None:
                chat_room = ModelsChatRoom.objects.create(
                        model= model
                )


        chat_messages = ModelChatMessages.objects.filter(chat = chat_room)

        message_list = []

        for message in chat_messages:
            message_list.append(
                {
                    "message":message.message,
                    "sender":message.sender.email,
                    "is_from_sender":message.sender==user,
                    "date_created":message.created_date
                }
            )

        return Response(data=message_list , status=200)
    



class CreateModelChatroom(APIView):


    permission_classes = [IsAuthenticated]




    def post(self, request:HttpRequest, format=None):
        user = request.user

        if user is None:
            return Response(data={"detail":"unauthenticated"} , status=403)
        

        data_from_body = json.loads(request.body)

        
        model_id = data_from_body["model_id"]

        message = data_from_body["message"]

        model = Model.objects.filter(pk = model_id).first()
        if model is None:
            data = {
                "detail":"data set was not found"
            }

            return Response(data , status=400)
        
        chat_room = ModelsChatRoom.objects.filter(model=model).first()


        if chat_room is None:
            if chat_room is None:
                chat_room = ModelsChatRoom.objects.create(
                        model=model
                )


        created_message = ModelChatMessages.objects.create(chat = chat_room , message=message , sender=user)

        data = {
            "message":created_message.message,
            "sender":created_message.sender.email,
            "is_from_sender":created_message.sender==user,
            "date_created":created_message.created_date
        }


        return Response(data=data , status=200)
    
