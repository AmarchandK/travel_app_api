# Generated by Django 4.1 on 2022-08-30 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendorz', '0006_alter_registrationz_email_alter_registrationz_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registrationz',
            name='email',
            field=models.EmailField(max_length=500, unique=True),
        ),
    ]
