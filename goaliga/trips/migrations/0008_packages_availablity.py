# Generated by Django 4.1 on 2022-08-30 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_datebooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='packages',
            name='availablity',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
