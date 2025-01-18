from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  
    path('',ListCategory.as_view(),name="home"),
    path('update_profile/',UpdateProfile.as_view(),name="update_profile"),
    path('login/',MyLoginView.as_view(),name="login"),
    path('user_logout/',MyLogoutview.as_view(),name="user_logout"),
    path('user_signup/',MyRegistrationview.as_view(),name="user_signup"),
    path('change_password/',ChangePassword.as_view(),name='change_password'),
    path('delete_user/<int:pk>/',DeleteUser.as_view(),name="delete_user"),
    path('add_category/',AddPetCategory.as_view(),name='add_category'),
    path('update_category/<slug:slug>/',UpdateCategory.as_view(),name='update_category'),
    path('delete_category/<slug:slug>/',DeleteCategory.as_view(),name="delete_category"),
    path('category_details/<slug:slug>/',ViewCategoryDetail.as_view(),name="category_details"),
    path('pet_detail/<slug:slug>/',ViewPetDetail.as_view(),name="pet_detail"),
    path('add_pet/',AddPet.as_view(),name='add_pet'),
    path('update_pet/<slug:slug>/',UpdatePet.as_view(),name="update_pet"),
    path('delete_pet/<slug:slug>/',DeletePet.as_view(),name='delete_pet'),

    path('list_users/',ListUsers.as_view(),name='list_users'),
    path('user_detail/<int:pk>/',VievUserDetail.as_view(),name='user_detail'),
    path('user_pets/<int:pk>/',ListUserPets.as_view(),name='user_pets'),

    path('search',SearchForPet.as_view(),name="search"),
    path('send_message',SendContactMessage.as_view(),name='send_message'),
    path('list_messages/',ListContactMessage.as_view(),name='list_messages'),
    path('message_detail/<int:pk>/',ViewMessageDetail.as_view(),name='message_detail'),
    path('sendmail/<int:pk>/',SendAnswerMail.as_view(),name='sendmail'),
    path('list_replies/<int:pk>/',list_replies.as_view(),name='list_replies'),
    path('reply_user_message/<int:pk>/<int:id>/',SendreplyMessage.as_view(),name="reply_user_message"),
    path('adoptation_request/<int:pk>/',SendAdoptationRequest.as_view(),name='adoptation_request'),
    path('list_assignment/',ListMyassignment.as_view(),name="list_assignment"),
    path('list_adopters/<slug:slug>/',ListAdopters.as_view(),name='list_adopters'),
    path('list_all_adopters/<slug:slug>/',ListAllAdopters.as_view(),name="list_all_adopters"),
    


    path('password-reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    path('account_activation/<uidb64>/<token>', views.account_activation, name='account_activation'),


    path('forbidden/',Forbidden_access.as_view(),name='forbidden'),


]