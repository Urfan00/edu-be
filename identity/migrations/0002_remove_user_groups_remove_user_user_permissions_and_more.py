# Generated by Django 5.1.1 on 2024-10-01 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('identity', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.AlterField(
            model_name='user',
            name='facebook',
            field=models.URLField(blank=True, help_text='Enter a valid URL for the Facebook profile.', null=True, verbose_name='Facebook Profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, help_text='Enter a valid URL for the GitHub profile.', null=True, verbose_name='GitHub Profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='instagram',
            field=models.URLField(blank=True, help_text='Enter a valid URL for the Instagram profile.', null=True, verbose_name='Instagram Profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='Designates whether this user has all permissions.', verbose_name='Superuser'),
        ),
        migrations.AlterField(
            model_name='user',
            name='linkedin',
            field=models.URLField(blank=True, help_text='Enter a valid URL for the LinkedIn profile.', null=True, verbose_name='LinkedIn Profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='twitter',
            field=models.URLField(blank=True, help_text='Enter a valid URL for the Twitter profile.', null=True, verbose_name='Twitter Profile'),
        ),
        migrations.AlterField(
            model_name='user',
            name='youtube',
            field=models.URLField(blank=True, help_text='Enter a valid URL for the YouTube channel.', null=True, verbose_name='YouTube Channel'),
        ),
    ]