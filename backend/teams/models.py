"""
Team models for team creation and management
"""
from django.db import models


class Team(models.Model):
    """Team model for grouping profiles and tracking team metrics"""
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'
        ordering = ['-total_points']
    
    def __str__(self):
        return self.name