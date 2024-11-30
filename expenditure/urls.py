from django.urls import path
from . import views
from django.contrib.auth import views as views_auth


urlpatterns = [
    path("login/", views_auth.LoginView.as_view(template_name="expenditure/login.html"), name="login"),
    path("register/", views.Register.as_view(), name="register"),
    path("logout/", views.Logout.as_view(), name="logout"),

    #path("", views.Home.as_view(), name="home"),
    path("", views.Home.as_view() ,name="home"),
    path("<int:pk>/update/", views.PostUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", views.PostDeleteView.as_view(), name="delete"),
    path("search/", views.PostSearchView.as_view(), name="search"),
    path("create/", views.PostCreateView.as_view(), name="create"),
    
         
]

