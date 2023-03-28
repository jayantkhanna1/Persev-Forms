from datetime import datetime
from django.db import models

class User(models.Model):
    name=models.CharField(max_length=100)
    password=models.CharField(max_length=300)
    email=models.CharField(max_length=100)
    private_key=models.CharField(max_length=100)

class Surveys(models.Model):
    name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    surveyname=models.CharField(max_length=100)
    surveyid=models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    json=models.TextField()
    img = models.CharField(max_length=1000)

class Accessable(models.Model):
    surveyid = models.CharField(max_length=100)
    emailList = models.CharField(max_length=20000)
    allowedbyall = models.BooleanField(default=True)
    limit_to_one = models.BooleanField(default=False)
    thankyou_or_not = models.BooleanField(default=False)
    thankyou_message = models.CharField(max_length=1000,default="Thankyou for taking the survey we have received your response")
    anonymous_or_not = models.BooleanField(default=True)

class Responses(models.Model):
    surveyid = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    anoynmous = models.BooleanField()
    response = models.TextField()
    time = models.TimeField(default=datetime.now().time())
    date = models.DateField(default=datetime.today())
