# Generated by Django 5.1.1 on 2024-11-13 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0006_alter_usergroup_unique_together_remove_group_mentor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='average',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Average'),
        ),
        migrations.AlterField(
            model_name='usergroup',
            name='student_full_name',
            field=models.CharField(blank=True, help_text='The full name of the student.', max_length=150, null=True, verbose_name='Student Full Name'),
        ),
    ]