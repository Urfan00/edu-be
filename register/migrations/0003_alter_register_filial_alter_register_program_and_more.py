# Generated by Django 5.1.1 on 2024-10-26 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_alter_filial_name_alter_program_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='filial',
            field=models.CharField(help_text='Enter the filial (branch) name.', max_length=255, verbose_name='Filial'),
        ),
        migrations.AlterField(
            model_name='register',
            name='program',
            field=models.CharField(help_text='Enter the program name.', max_length=255, verbose_name='Program'),
        ),
        migrations.AlterField(
            model_name='register',
            name='purpose',
            field=models.CharField(help_text='Enter the purpose for registration.', max_length=255, verbose_name='Purpose'),
        ),
        migrations.AlterField(
            model_name='register',
            name='region',
            field=models.CharField(help_text='Enter the region name.', max_length=255, verbose_name='Region'),
        ),
        migrations.AlterField(
            model_name='register',
            name='source_of_information',
            field=models.CharField(help_text='Enter the source of information.', max_length=255, verbose_name='Source of Information'),
        ),
        migrations.AlterField(
            model_name='register',
            name='university',
            field=models.CharField(help_text='Enter the university name.', max_length=255, verbose_name='University'),
        ),
    ]