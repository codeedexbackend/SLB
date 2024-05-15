# Generated by Django 3.2.10 on 2024-05-15 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='name', max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]