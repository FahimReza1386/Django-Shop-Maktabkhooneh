# Generated by Django 4.2.17 on 2025-01-23 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Gender',
            field=models.IntegerField(choices=[(1, 'male'), (2, 'female'), (3, 'other')], default=3),
        ),
    ]
