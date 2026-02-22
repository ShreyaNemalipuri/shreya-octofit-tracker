"""
Manual migration to alter team field from CharField to ForeignKey
"""
from django.db import migrations, models
import django.db.models.deletion


def alter_profile_team(apps, schema_editor):
    """
    Manually handle the field change since Djongo doesn't support ALTER COLUMN TYPE
    """
    Pass


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0001_initial'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='team',
        ),
        migrations.AddField(
            model_name='profile',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='members', to='teams.team'),
        ),
    ]
