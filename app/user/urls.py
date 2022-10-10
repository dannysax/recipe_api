from django.urls import path
from user import views


app_name = "user"

urlpatterns = [
    path("create/", views.CreateUserApiView.as_view(), name="create"),
    path("token/", views.AuthTokenView.as_view(), name="token"),
    path("me/", views.UserDetailsView.as_view(), name="me")
]