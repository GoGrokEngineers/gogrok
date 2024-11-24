from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.

class Task(models.Model):  
    title = models.CharField(max_length=200)
    description = RichTextField(blank=True)
    difficulty = models.CharField(max_length=50)  # it can be choice field
    
    

    def __str__(self):
        return f"{self.title} - {self.difficulty}"
    
