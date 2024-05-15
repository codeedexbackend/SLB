from django.contrib.auth.models import User
from django.db import models




class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100,default='name')
    mobile_number = models.CharField(max_length=15,unique=True)
    gate_pass_no = models.CharField(max_length=50)
    CREW_CHOICES = [
        ('Crew1', 'Crew 1'),
        ('Crew2', 'Crew 2'),
        ('Crew3', 'Crew 3'),
        ('Crew4', 'Crew 4'),
        ('Crew5', 'Crew 5'),
    ]
    crew = models.CharField(max_length=10, choices=CREW_CHOICES)
    DESIGNATION_CHOICES = [
        ('Designation1', 'Designation 1'),
        ('Designation2', 'Designation 2'),
        ('Designation3', 'Designation 3'),
        ('Designation4', 'Designation 4'),
        ('Designation5', 'Designation 5'),
    ]
    designation = models.CharField(max_length=15, choices=DESIGNATION_CHOICES)
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
