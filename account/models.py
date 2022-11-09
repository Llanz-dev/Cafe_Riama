from django.contrib.auth.models import User
from django.db import models


GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female')
)

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, default='Male', blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} - {self.gender}'
    