# Generated by Django 2.2.12 on 2020-05-08 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Monitor', '0003_iperftestresults_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iperftestresults',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
