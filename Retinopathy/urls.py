from django.urls import path
from knox import views as knox_views

from . import views
from . import serializers
from . import models
# from django.urls import path
from .views import (admin_login, get_patient, patient_list, predict_patient,user_list)

urlpatterns = [
    path('register/',views.RegistrationView.as_view(), name='register'),
    path('login/',views.LoginAPI.as_view(), name='Login'),
    path('adminLogin/',admin_login, name='AdminLogin'),
    # path('user/',views.userData),
    path("users/",user_list, name="users"),
    path('patients/', predict_patient),
    path('patientData/', patient_list, name="PatientDetails"),
    # path("retrainModel/", serializers.RetrainModel, name=""),
    path('patients/<int:patient_id>/', get_patient, name='get_patient'),
    path('logout/',knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
]
