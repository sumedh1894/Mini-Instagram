from django.db import models
from django.contrib.auth.models import User

#Data fields model that is to be stored in the sqlite3 database
class Post(models.Model):
    
    image_field= models.FileField(null=True, blank=True)
    
    pub_date = models.DateTimeField( )
    
    # models.cascade deletes all the data associated with the deleted object 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    caption= models.CharField(max_length=250)
    

