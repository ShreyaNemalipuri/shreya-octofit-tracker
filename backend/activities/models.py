"""
Activity models for activity logging and tracking
"""
from django.db import models
from django.utils import timezone
from profiles.models import Profile


class Activity(models.Model):
    """Activity model for tracking fitness activities"""
    
    ACTIVITY_CHOICES = [
        ('RUN', 'Running'),
        ('WALK', 'Walking'),
        ('CYCLE', 'Cycling'),
        ('SWIM', 'Swimming'),
        ('YOGA', 'Yoga'),
        ('STRENGTH', 'Strength Training'),
        ('OTHER', 'Other'),
    ]
    
    # Points per minute based on activity type
    POINTS_MAP = {
        'RUN': 2.0,          # 2 points per minute
        'WALK': 0.5,         # 0.5 points per minute
        'CYCLE': 1.5,        # 1.5 points per minute
        'SWIM': 2.5,         # 2.5 points per minute
        'YOGA': 1.0,         # 1 point per minute
        'STRENGTH': 2.0,     # 2 points per minute
        'OTHER': 0.75,       # 0.75 points per minute
    }
    
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    duration_minutes = models.IntegerField()
    distance_km = models.FloatField(null=True, blank=True)
    calories = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'activities'
        ordering = ['-date']
    
    def save(self, *args, **kwargs):
        """Calculate points before saving"""
        self.points = self.calculate_points()
        super().save(*args, **kwargs)
        
        # Update user's total points
        self.user.total_points += self.points
        self.user.save()
        
        # Update team's total points if user is in a team
        if self.user.team:
            self.user.team.total_points += self.points
            self.user.team.save()
    
    def calculate_points(self):
        """Calculate points based on activity type and duration"""
        base_points = self.POINTS_MAP.get(self.activity_type, 0.75)
        total_points = int(base_points * self.duration_minutes)
        
        # Bonus points for longer distances
        if self.distance_km and self.distance_km > 0:
            distance_bonus = int(self.distance_km * 5)
            total_points += distance_bonus
        
        return total_points
    
    def __str__(self):
        return f"{self.user.name} - {self.activity_type} on {self.date}"