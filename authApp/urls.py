from . import views
from .views import *
from django.urls import path

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('verify-account/', UserVerificationView.as_view()),
    path('send_email_view/', views.send_email_view),
    path('all-users/', UserListView.as_view()),
    path('user-datasets/<int:user_id>/', UserRepository.as_view()),
    path('user-roles/', RoleListView.as_view()),
    path('role-users/<int:role_id>/', RoleUserListView.as_view()),
    path('add-role/', AddRole.as_view()),
    path('add-role-user/', AddRoleUserView.as_view()),
    path('delete_user/<int:user_id>/', UserDeleteAPIView.as_view()),
    path('activate_user/<int:user_id>/', UserActivateAPIView.as_view()),
    path('deactivate_user/<int:user_id>/', UserDeactivateAPIView.as_view()),
    path('edit_user/<int:user_id>/', UserEditAPIView.as_view()),
    path('user_detail/<int:user_id>/', UserDetailAPIView.as_view()),
    path('user-profile/<int:user_id>/', UserProfileAPIView.as_view()),
    path('dashboard/', DashboardSummary.as_view()),
    path('change_password/', ChangePasswordAPIView.as_view()),
    path('landing/', LandingPageDAta.as_view()),
    path('get_chat_messages/', GetChatroom.as_view()),
    path('create_chat_message/', CreateChatroom.as_view()),
    path('get_model_chat_messages/', GetModelChatroom.as_view()),
    path('create_model_chat_message/', CreateModelChatroom.as_view()),
]
