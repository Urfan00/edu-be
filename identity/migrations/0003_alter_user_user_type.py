# Generated by Django 5.1.1 on 2024-10-26 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0002_remove_user_groups_remove_user_user_permissions_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('parent', 'Parent'), ('teacher', 'Teacher'), ('staff', 'Staff'), ('director', 'Director')], default='student', max_length=20, verbose_name='User Type'),
        ),
    ]
