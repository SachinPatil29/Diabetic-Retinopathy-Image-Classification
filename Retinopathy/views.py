from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from .serializers import UserSerializer, LoginSerializer, PatientSerializer
from rest_framework import status
from django.shortcuts import render
from django.http import JsonResponse
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

# # Open the CSV file for writing
# csv_filepath = os.path.join(settings.CSV_ROOT, 'DR_ImageDataset.csv')
# with open(csv_filepath, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerow(['Image', 'Predicted Label'])

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
#=====================================================================================================================================


# import tensorflow as tf
# from tensorflow.keras.preprocessing import image
# import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow.keras.models import Model, load_model
# import numpy as np
# import pandas as pd
# import os
# from PIL import Image
# import tensorflow as tf
# from numpy import asarray
# import matplotlib.pyplot as plt
# tf.compat.v1.enable_eager_execution()
# import time
# from tensorflow.keras import Model, layers, models, optimizers
# from tensorflow.keras.callbacks import CSVLogger
# from tensorflow.keras.constraints import UnitNorm

# class retrainModel():
#     global model,model_path
#     IMAGE_SIZE = [224, 224]
#     model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model3.h5')
#     model = load_model(model_path)
#     train_path = os.path.join(settings.CSV_ROOT, 'Opencv_augmented_train')
#     test_path = os.path.join(settings.CSV_ROOT, 'Opencv_modified_test')
#     # csv_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_ImageDataset.csv')
#     # train_path = 'D:\KLETU\3rd Year\6th Sem\MinorProject\MinorProject\Vinayak Augmented'
    
#     print(train_path)

#     train_ds= tf.keras.utils.image_dataset_from_directory(
#               train_path,
#               validation_split=0.2,
#               subset="training",
#               seed=123,
#               image_size=(224, 224),
#               batch_size=16)
#     val_ds = tf.keras.utils.image_dataset_from_directory(
#       test_path,
#       validation_split=0.2,
#       subset="validation",
#       seed=123,
#       image_size=(224, 224),
#       batch_size=16)
   
#     def retrain_model():
#         print("model start")
#         model = load_model(model_path)

#         for layer in model.layers[:-1]:
#             layer.trainable = False

#         new_output = tf.keras.layers.Dense(5, activation='softmax')(model.layers[-2].output)

#         model = Model(inputs=model.inputs, outputs=new_output)

#         opti = tf.keras.optimizers.Adagrad(
#             learning_rate=0.001,
#             initial_accumulator_value=0.01,
#             epsilon=1e-06,
#             name="Adagrad"
#         )

#         model.compile(
#             optimizer=opti, 
#             loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False), 
#             metrics=[
#                 'accuracy'
#             ]
#         )
#         return model

#     model.summary()

#     new_model = retrain_model()
#     epochs=2
#     # time_callback = TimeHistory()

#     try:
#         history = new_model.fit(
#         train_ds,
#         validation_data = val_ds,
#         epochs = epochs,
#         # callbacks = [time_callback]
#         )

#     except Exception as e:
#         print(e)

#     new_model.save('/workspace/DP/Tensorflow/Saved_models/DR_model4.h5')


########################################################################################################################

# import tensorflow as tf
# import pandas as pd
# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
# import numpy as np
# import matplotlib.pyplot as plt
# from tensorflow.keras.models import Model, load_model
# from tensorflow.keras.preprocessing.image import load_img, img_to_array
# from tensorflow.keras.applications.resnet50 import preprocess_input
# import os
# from PIL import Image
# from numpy import asarray
# import matplotlib.pyplot as plt
# tf.compat.v1.enable_eager_execution()
# import time
# from tensorflow.keras import Model, layers, models, optimizers
# from sklearn.model_selection import train_test_split
# import mysql.connector
# import io
# from tensorflow.keras.constraints import UnitNorm


# def RetrainModel(request):
#     model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model3.h5')
#     model = load_model(model_path)
#     data = pd.read_csv(os.path.join(settings.CSV_ROOT, 'DR_ImageDataset.csv'))
    
#     # image_paths = data['Image'].tolist()
#     # labels = data['Predicted Label'].tolist()
    
#     # Connect to the database
#     cnx = mysql.connector.connect(user='root', password='root',
#                                   host='localhost',
#                                   database='retinopathy')
    
#     # Fetch the images and labels
#     cursor = cnx.cursor()
#     query = "SELECT image, prediction FROM retinopathy_patient"
#     cursor.execute(query)
#     images = []
#     labels = []
#     for (image, label) in cursor:
#         images.append(image)
#         labels.append(label)
    
#     # Preprocess the images
#     width, height = 224, 224
#     num_images = len(images)
#     X = np.zeros((num_images, width, height, 3))
#     for i, image in enumerate(images):
#         image = Image.open(io.BytesIO(image))
#         image = image.resize((width, height))
#         X[i, :, :, :] = np.array(image) / 255.0
    
#     # Split the data into training and validation sets
#     X_train, X_val, y_train, y_val = train_test_split(X, labels, test_size=0.2, random_state=42)
    
#     #compile the model
#     opt = tf.keras.optimizers.Adagrad(
#         learning_rate=0.001,
#         initial_accumulator_value=0.01,
#         epsilon=1e-06,
#         name="Adagrad"
#     )
    
#     model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
    
#     # model.summary()
    
#     # Train the model
#     model.fit(X_train, y_train, epochs=10, batch_size=2, validation_data=(X_val, y_val))

    
#     model.save('')
    
#     # Return a JSON response to indicate that the training was successful
#     return JsonResponse({'status': 'success'})

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


#=============================================================================================================

# import paramiko
# import os
# from django.conf import settings
# from django.http import JsonResponse

# def retrain_model(request):
#     # Set the credentials for the DGX server
#     host = '172.17.0.3'
#     port = 4828
#     username = 'uday@10.2.0.7'
#     password = 'kle@aiml'

#     # Set the path to the Python script on the DGX server
#     remote_script_path = '/workspace/DP/Minor_Project/retinopathy/train.py'

#     # Set the path to the model file and dataset on the local machine
#     local_model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model3.h5')
#     # local_dataset_path = os.path.join(settings.CSV_ROOT, 'DR_ImageDataset.csv')
#     local_dataset_path = 'C:\Users\sachi\OneDrive\Desktop\Vinayak Augmented\Opencv_augmented_train'

#     # Set the paths to the model file and dataset on the DGX server
#     remote_model_path = '/workspace/DP/Minor_Project/model/DR_model3.h5'
#     remote_dataset_path = '/workspace/DP/Minor_Project/dataset/Opencv_augmented_train'

#     # Connect to the DGX server via SSH
#     ssh = paramiko.SSHClient()
#     ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#     ssh.connect(hostname=host, port=port, username=username, password=password)

#     # Upload the model and dataset to the DGX server
#     ftp = ssh.open_sftp()
#     ftp.put(local_model_path, remote_model_path)
#     ftp.put(local_dataset_path, remote_dataset_path)
#     ftp.close()

#     # Run the Python script on the DGX server to retrain the model on the dataset
#     stdin, stdout, stderr = ssh.exec_command(f'python {remote_script_path} --model {remote_model_path} --data {remote_dataset_path}')
#     output = stdout.read().decode('utf-8')
#     errors = stderr.read().decode('utf-8')

#     # Close the SSH connection
#     ssh.close()

#     # Return the output and errors as a JSON response
#     return JsonResponse({'output': output, 'errors': errors})
