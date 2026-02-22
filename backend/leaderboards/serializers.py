"""
Serializers for Leaderboard endpoints
"""
from rest_framework import serializers


class StudentLeaderboardSerializer(serializers.Serializer):
    """Serializer for student leaderboard entry"""
    rank = serializers.IntegerField()
    id = serializers.CharField()
    name = serializers.CharField()
    total_points = serializers.IntegerField()


class TeamLeaderboardSerializer(serializers.Serializer):
    """Serializer for team leaderboard entry"""
    rank = serializers.IntegerField()
    id = serializers.CharField()
    name = serializers.CharField()
    total_points = serializers.IntegerField()