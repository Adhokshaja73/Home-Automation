# Generated by Django 4.0.5 on 2022-06-14 05:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_homeboardtopic_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeboardtopic',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
