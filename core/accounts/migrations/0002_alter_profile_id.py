# Generated by Django 4.2.17 on 2024-12-27 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]
