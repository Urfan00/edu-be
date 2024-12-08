# Generated by Django 5.1.1 on 2024-11-15 17:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('status', models.CharField(choices=[('present', 'Present'), ('absent', 'Absent'), ('late', 'Late'), ('excused', 'Excused')], help_text='The attendance status of the student for this session. Options include Present, Absent, Late, or Excused.', max_length=10, verbose_name='Status')),
                ('date', models.DateField(help_text='The date of the class or session for which attendance is being recorded.', verbose_name='Date')),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendance Records',
                'constraints': [models.UniqueConstraint(fields=('date', 'user_group'), name='unique_attendance_per_user_group_and_date')],
            },
        ),
    ]
