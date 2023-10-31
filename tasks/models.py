from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField( max_length=50 )
    # As TextInput
    description = models.TextField( blank=True )
    #As TextArea
    created = models.DateTimeField( auto_now_add=True )
    # As DateField
    date_completed = models.DateTimeField( null=True )
    important = models.BooleanField( default=False )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #on_delete = models.CASCADE is for when deleted a user their tasks also deleted
