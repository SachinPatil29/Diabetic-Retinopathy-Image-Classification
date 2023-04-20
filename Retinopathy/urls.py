from django.urls import path
from . import views 
from knox import views as knox_views
# from django.urls import path
from .views import predict_patient
from .views import user_list, patient_list, admin_login

urlpatterns = [
    path('register/',views.RegistrationView.as_view(), name='register'),
    path('login/',views.LoginAPI.as_view(), name='Login'),
    path('adminLogin/',admin_login, name='AdminLogin'),
    # path('user/',views.userData),
    path("users/",user_list, name="users"),
    path('patients/', predict_patient),
    path('patientDetails/', patient_list, name="PatientDetails"),
    path('logout/',knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    
]
