from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import UserSerializer, LoginSerializer, PatientSerializer
from rest_framework import status
# from knox.auth import TokenAuthentication
from django.contrib.auth import authenticate
# from rest_framework.permissions import AllowAny
# from django.shortcuts import redirect
from rest_framework import generics
from django.contrib.auth import authenticate, login
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from .serializers import PatientSerializer
# from . models import Patient
from PIL import Image
import os
import numpy as np
import tensorflow as tf
# Create your views here.
        
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
        
        
# class AdminLoginAPI(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         username = "admin"
#         password = "12345"
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return super().post(request, format=None)
#         else:
#             return Response({'error': 'Invalid username or password.'}, status=status.HTTP_400_BAD_REQUEST)



def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            # Admin user is authenticated
            return JsonResponse({'message': 'Login successful'})
        else:
            return JsonResponse({'message': 'Invalid username or password'}, status=401)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)

        
        
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

@api_view(['POST'])
def predict_patient(request):
    serializer = PatientSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        # Preprocess the image
        img = Image.open(request.FILES['image'])
        img = img.convert('RGB')
        img = img.resize((224, 224))
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.

        # Load the trained model
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model1 (1).h5')
        model = tf.keras.models.load_model(model_path)
        # model = tf.keras.models.load_model('D:\Image_classfication\DR_model1 (1).h5')    

        # Make the prediction
        prediction = model.predict(img_array)
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



# =====================================================================================================================

# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# import tensorflow as tf
# import numpy as np
# import os
# import paramiko

# DGX_HOST = '192.168.0.100'  # replace with your DGX server's IP address
# DGX_PORT = 22
# DGX_USERNAME = 'username'
# DGX_PASSWORD = 'password'

# @csrf_exempt
# def retrain_model(request):
#     if request.method != 'POST':
#         return JsonResponse({'error': 'Only POST requests are allowed.'}, status=405)

#     # Retrieve the uploaded image data
#     image_file = request.FILES['file']
#     # image = tf.image.decode_image(image_file.read())
#     # image = tf.image.resize(image, [224, 224])
#     # image = tf.keras.applications.mobilenet_v2.preprocess_input(image)

#     # Load the pre-existing model
#     # model_path = os.path.join(os.path.dirname(__file__), 'path/to/preexisting_model.h5')
#     model = tf.keras.models.load_model('D:\Image_classfication\DR_model1 (1).h5')

#     # Train the model on the new data using DGX server
#     dgx_client = paramiko.SSHClient()
#     dgx_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     dgx_client.connect(DGX_HOST, port=DGX_PORT, username=DGX_USERNAME, password=DGX_PASSWORD)

#     # Copy the image data to the DGX server
#     stdin, stdout, stderr = dgx_client.exec_command('mkdir -p /tmp/retrain')
#     sftp = dgx_client.open_sftp()
#     sftp.putfo(image_file.file, '/tmp/retrain/image.jpg')
#     sftp.close()

#     # Copy the model code and data to the DGX server
#     sftp = dgx_client.open_sftp()
#     sftp.put('path/to/model_training_script.py', '/tmp/retrain/model_training_script.py')
#     sftp.put('D:\Image_classfication\DR_model1 (1).h5', '/tmp/retrain/preexisting_model.h5')
#     sftp.close()

#     # Run the model training script on the DGX server
#     stdin, stdout, stderr = dgx_client.exec_command('cd /tmp/retrain && python model_training_script.py')

#     # Wait for the script to complete and check for errors
#     exit_status = stdout.channel.recv_exit_status()
#     if exit_status != 0:
#         error_msg = stderr.read().decode('utf-8')
#         return JsonResponse({'error': f'Model training failed: {error_msg}'}, status=500)

    # # Load the updated model from the DGX server
    # updated_model_path = '/tmp/retrain/updated_model.h5'
    # sftp = dgx_client.open_sftp()
    # sftp.get(updated_model_path, 'path/to/updated_model.h5')
    # sftp.close()
    # updated_model = tf.keras.models.load_model('path/to/updated_model.h5')

    # # Save the updated model to disk
    # updated_model.save(updated_model_path)

    # return JsonResponse({'success': 'Model retraining complete.'}, status=200)
