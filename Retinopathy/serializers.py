from rest_framework import serializers,validators
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Patient


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password')
        
        password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        username = validated_data.get('username')
        email = validated_data.get('email')
        password = validated_data.get('password')       
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username=username,
            email= email, 
            password=password
        )
        user.set_password(password)
        user.save()
        return user
          
class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ('id', 'first_name', 'last_name', 'age', 'gender','phone_number','image', 'prediction')
            
            
            
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
# from django.conf import settings

# class RetrainModel():
#     global model,model_path
#     IMAGE_SIZE = [224, 224]
#     model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model3.h5')
#     model = load_model(model_path)
#     train_path = os.path.join(settings.DATASET_ROOT, 'Opencv_augmented_train')
#     # test_path = os.path.join(settings.CSV_ROOT, 'Opencv_modified_test')
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
#       train_path,
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

#     # new_model.save('')