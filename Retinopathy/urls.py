from django.urls import path
from . import views 
from knox import views as knox_views
# from django.urls import path
from .views import predict_patient

urlpatterns = [
    path('register/',views.RegistrationView.as_view(), name='register'),
    path('login/',views.LoginAPI.as_view(), name='Login'),
    # path('user/',views.userData),
    path('patients/', predict_patient),
    path('logout/',knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    
]
