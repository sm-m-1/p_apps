# Generated by Django 2.1.4 on 2018-12-14 16:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_future', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useremail',
            name='recipient_name',
        ),
        migrations.AlterField(
            model_name='useremail',
            name='email_subject',
            field=models.CharField(max_length=200),
        ),
    ]
