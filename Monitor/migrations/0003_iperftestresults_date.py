# Generated by Django 2.2.12 on 2020-05-08 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0002_auto_20200508_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='iperftestresults',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
