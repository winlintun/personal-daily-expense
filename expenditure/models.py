from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User



class Post(models.Model):

    STATUE_CHOICE = (
        (0, "Darft"),
        (1, "Publish")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    location = models.CharField(max_length=255, blank=True)
    money = models.DecimalField(max_digits=7, decimal_places=2, help_text="NTD dollar")
    create_date = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUE_CHOICE, default=0)
    
    

    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-create_date']
    