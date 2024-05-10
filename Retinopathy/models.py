from django.db import models

class Technician(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True, null=False)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    
    def __str__(self):
        return self.username
    
   
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
    
        
