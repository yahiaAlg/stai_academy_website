from django.db import models
from instructors.models import Instructor
from datetime import datetime

# Create your models here.
class Listing(models.Model):
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=35)
    description = models.TextField(blank=True)
    prerequisites = models.CharField(max_length=35,blank=True)
    room = models.CharField(max_length=30,blank=True)
    price = models.IntegerField()
    main_img = models.ImageField(upload_to="photos/%Y/%m/%d/")
    photo_1 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_2 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_3 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    photo_4 = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(auto_now_add=True, blank=True)
    start_date = models.DateTimeField(default=datetime.utcnow)

    def __str__(self):
        return f"{self.title}"
