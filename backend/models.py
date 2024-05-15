from django.contrib.auth.models import User
from django.db import models




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,default='name')
    mobile_number = models.CharField(max_length=15,unique=True)
    gate_pass_no = models.CharField(max_length=50)
    crew = models.ForeignKey('Crew', on_delete=models.SET_NULL, null=True, related_name='profiles')
    designation = models.ForeignKey('Designation', on_delete=models.SET_NULL, null=True, related_name='profiles')
    RIG_CHOICES = [
        ('Rig', 'Rig'),
        ('Rigless', 'Rigless'),
    ]
    rig_or_rigless = models.CharField(max_length=10, choices=RIG_CHOICES)
    project_name = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

class Crew(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Designation(models.Model):
    name = models.CharField(max_length=50)
    crew = models.ForeignKey(Crew, on_delete=models.CASCADE, related_name='designations')


    def __str__(self):
        return f"{self.name} ({self.crew.name})"
    

