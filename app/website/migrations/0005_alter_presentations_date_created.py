# Generated by Django 4.2.6 on 2024-02-14 04:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_alter_profile_bio_alter_profile_profile_pic_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presentations',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
