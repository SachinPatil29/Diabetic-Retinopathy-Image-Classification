from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from knox.auth import AuthToken
from .serializers import UserSerializer, LoginSerializer, PatientSerializer
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework import generics
from django.contrib.auth import authenticate, login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from PIL import Image
import os
import numpy as np
import tensorflow as tf

        
class RegistrationView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            _, token = AuthToken.objects.create(user)
            return Response({
                    'user_info':{
                    'id':user.id,
                    'username':user.username,
                    'email':user.email
                    },
                'token':token
                })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        
        
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return super().post(request, format=None)
        else:
            return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)
        
        
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == 'admin' and password == '12345':
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid username or password'})


        
        
#Retrieving user data from database
from django.http import JsonResponse
from django.contrib.auth.models import User

def user_list(request):
    users = User.objects.all()
    data = []
    for user in users:
        data.append({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'email': user.email,
        })
    return JsonResponse({'data': data})


from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import PatientSerializer
from .models import Patient
from PIL import Image
import numpy as np
import tensorflow as tf
from django.conf import settings
import csv


# Define the CSV file path
csv_filepath = os.path.join(settings.CSV_ROOT, 'DR_ImageDataset.csv')

# Check if the CSV file exists, if not, create it with headers
if not os.path.exists(csv_filepath):
    with open(csv_filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Image', 'Predicted Label'])
    
@api_view(['POST'])

def predict_patient(request):
    serializer = PatientSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()

        # Preprocess the image
        img = Image.open(request.FILES['image'])
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img = np.array(img)
        img = np.expand_dims(img, axis=0)
        img = img / 255.

        # Load the trained model
        # model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model1 (1).h5')
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model3.h5')
        model = tf.keras.models.load_model(model_path)    

        # Make the prediction
        prediction = model.predict(img)
        prediction = prediction.argmax(axis=-1)[0]
        if prediction == 0:
            prediction = "Normal"
        
        elif prediction == 1:
            prediction = "Mild"
            
        elif prediction == 2:
            prediction = "Moderate"
            
        elif prediction == 3:
            prediction = "Severe NonProliferative"
            
        elif prediction == 4:
            prediction = "Proliferative"
            
        else:
            return None

        # Write the prediction to the CSV file
        with open(csv_filepath, 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([request.FILES['image'].name, prediction])
        
        # Update the patient record with the prediction
        patient = Patient.objects.get(id=serializer.data['id'])
        patient.prediction = prediction
        patient.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Retrieving patient data from database

from django.http import JsonResponse
from .models import Patient

def patient_list(request):
    patients = Patient.objects.all()
    data = []
    for patient in patients:
        data.append({
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'age': patient.age,
            'gender': patient.gender,
            'phone_number': patient.phone_number,
            'image': request.build_absolute_uri(patient.image.url),
            'prediction': patient.prediction,
        })
    return JsonResponse({'data': data})

# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
from django.http import JsonResponse
from .models import Patient

def get_patient(request, patient_id):
    # Query the database for the matching patient data
    try:
        patient = Patient.objects.get(id=patient_id)
    except Patient.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'})

    # Return the patient data as JSON
    data = {
        'id': patient.id,
        'fname': patient.fname,
        'lname': patient.lname,
        'age': patient.age,
        'gender': patient.gender,
        'phonenumber': patient.phonenumber,
        'image': patient.image.url,
        'labels': patient.labels.split(',')
    }
    return JsonResponse(data)
