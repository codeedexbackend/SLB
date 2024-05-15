from django.db import models

class Designation(models.Model):
    name = models.CharField(max_length=100)

class Training(models.Model):
    name = models.CharField(max_length=100)
    validity = models.DurationField()

class Employee(models.Model):
    name = models.CharField(max_length=100)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE)
    trainings = models.ManyToManyField(Training, through='TrainingAssignment')

class TrainingAssignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    assigned_date = models.DateField(auto_now_add=True)
