from django.db import models

# class Technician(models.Model):
#     firstname = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     username = models.CharField(max_length=100, unique=True, null=False)
#     email = models.EmailField(max_length=100)
#     password = models.CharField(max_length=100)
    
#     def __str__(self):
#         return self.username
    
   
from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10)
    image = models.ImageField(upload_to='images/')
    # prediction = models.IntegerField(null=True, blank=True)
    prediction = models.CharField(max_length=30,null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
        
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model, load_model
import numpy as np
import pandas as pd
import os
from PIL import Image
import tensorflow as tf
from numpy import asarray
import matplotlib.pyplot as plt
tf.compat.v1.enable_eager_execution()
import time
from tensorflow.keras import Model, layers, models, optimizers
from tensorflow.keras.callbacks import CSVLogger
from tensorflow.keras.constraints import UnitNorm
from django.conf import settings

class RetrainModel():
    global model,model_path
    IMAGE_SIZE = [224, 224]
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_model3.h5')
    model = load_model(model_path)
    train_path = os.path.join(settings.DATASET_ROOT, 'Opencv_augmented_train')
    # test_path = os.path.join(settings.CSV_ROOT, 'Opencv_modified_test')
    # csv_filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DR_ImageDataset.csv')
    # train_path = 'D:\KLETU\3rd Year\6th Sem\MinorProject\MinorProject\Vinayak Augmented'
    
    print(train_path)

    train_ds= tf.keras.utils.image_dataset_from_directory(
              train_path,
              validation_split=0.2,
              subset="training",
              seed=123,
              image_size=(224, 224),
              batch_size=16)
    val_ds = tf.keras.utils.image_dataset_from_directory(
      train_path,
      validation_split=0.2,
      subset="validation",
      seed=123,
      image_size=(224, 224),
      batch_size=16)
   
    def retrain_model():
        print("model start")
        model = load_model(model_path)

        for layer in model.layers[:-1]:
            layer.trainable = False

        new_output = tf.keras.layers.Dense(5, activation='softmax')(model.layers[-2].output)

        model = Model(inputs=model.inputs, outputs=new_output)

        opti = tf.keras.optimizers.Adagrad(
            learning_rate=0.001,
            initial_accumulator_value=0.01,
            epsilon=1e-06,
            name="Adagrad"
        )

        model.compile(
            optimizer=opti, 
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=False), 
            metrics=[
                'accuracy'
            ]
        )
        return model

    model.summary()

    new_model = retrain_model()
    epochs=2
    # time_callback = TimeHistory()

    try:
        history = new_model.fit(
        train_ds,
        validation_data = val_ds,
        epochs = epochs,
        # callbacks = [time_callback]
        )

    except Exception as e:
        print(e)

    # new_model.save('')