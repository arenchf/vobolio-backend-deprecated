from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import ObtainTokenPairWithColorView, CustomUserCreate, UserRoleView, UserView, RoleView, ChangePassword

urlpatterns = [
    path('token/obtain/', ObtainTokenPairWithColorView.as_view(),
         name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('token/create/', CustomUserCreate.as_view(), name="create_user"),
    path('users/<int:user_id>/', UserView.as_view(), name="user"),
    path('users/<int:user_id>/roles/', UserRoleView.as_view(), name="user_roles"),
    path('users/<int:user_id>/password/',
         ChangePassword.as_view(), name="change_password"),
    path('roles/', RoleView.as_view(), name="roles")
]
