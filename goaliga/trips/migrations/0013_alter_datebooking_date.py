# Generated by Django 4.1 on 2022-09-15 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0012_alter_datebooking_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datebooking',
            name='Date',
            field=models.DateField(blank=True),
        ),
    ]
