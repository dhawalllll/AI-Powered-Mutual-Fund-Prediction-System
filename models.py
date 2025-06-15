from django.db import models

# Create your models here.
from django.db import models

# Create your models here.

class newuser(models.Model):
    Username=models.CharField(max_length=80)
    fname=models.CharField(max_length=89)
    lname=models.CharField(max_length=88)
    email=models.EmailField(max_length=90)
    pass1=models.CharField(max_length=90)
    pass2=models.CharField(max_length=90)


class student(models.Model):
    Username=models.CharField(max_length=80, null=True)
    fname=models.CharField(max_length=89,null=True)
    lname=models.CharField(max_length=88,null=True)
    email=models.EmailField(max_length=90,null=True)
    pass1=models.CharField(max_length=90,null=True)
    pass2=models.CharField(max_length=90,null=True)



class Contact(models.Model):
    names = models.CharField(max_length=30)
    email = models.EmailField(max_length=50, null='True')
    phone = models.CharField(max_length=10, null='True')
    desc = models.TextField(null='True')
    var = models.TextField(null='True')
    var2 = models.TextField(null='True')