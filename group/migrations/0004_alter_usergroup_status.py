# Generated by Django 5.1.1 on 2024-10-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_remove_group_is_active_group_status_usergroup_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usergroup',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('graduated', 'Graduated'), ('transferred', 'Transferred'), ('dropped_out', 'Dropped Out')], default='active', help_text="Current status of the student's participation. It can be Graduated, Dropped Out, Transferred or Active.", max_length=15, verbose_name='Status'),
        ),
    ]