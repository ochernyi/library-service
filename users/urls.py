from django.urls import path
from rest_framework.authtoken import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import CreateUserView, ManageUserView

urlpatterns = [
    path("", CreateUserView.as_view(), name="register"),
    path("login/", views.obtain_auth_token, name="token"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user"

# from django.urls import path
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
#
# from users.views import CreateUserView, ManageUserView
#
# urlpatterns = [
#     path("register/", CreateUserView.as_view(), name="create"),
#     path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
#     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
#     path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
#     path("me/", ManageUserView.as_view(), name="manage"),
# ]
#
# app_name = "user"
