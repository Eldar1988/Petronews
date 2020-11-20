from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login_success', views.login_success_view, name='login_success'),

    path('user_name_update/<int:pk>', views.UserNameUpdate.as_view(), name='update_user_name'),
    path('user_change_avatar/<int:pk>', views.UserChangeAvatar.as_view(), name='change_avatar'),
    path('user_change_bg/<int:pk>', views.UserChangeBg.as_view(), name='change_bg'),

    path('add_publication/<int:pk>', views.AddPublication.as_view(), name='add_publication'),
    path('edit_publication/<int:pk>', views.EditPublication.as_view(), name='edit_publication'),
    path('delete_publications/<int:pk>', views.DeletePublication.as_view(), name='delete_publication'),
    path('delete_question/<int:pk>', views.DeleteQuestion.as_view(), name='delete_question'),
]
