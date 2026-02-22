"""
Serializers for Team model
"""
from rest_framework import serializers
from .models import Team
from profiles.serializers import ProfileSerializer


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    id = serializers.SerializerMethodField()
    members = ProfileSerializer(many=True, read_only=True)
    member_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['id', 'name', 'description', 'total_points', 'members', 'member_count', 'created_at', 'updated_at']
        read_only_fields = ['total_points', 'created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        if obj.id:
            return str(obj.id)
        return None
    
    def get_member_count(self, obj):
        """Get count of team members"""
        return obj.members.count()


class TeamSummarySerializer(serializers.Serializer):
    """Serializer for team summary/ranking"""
    team = TeamSerializer()
    rank = serializers.IntegerField()
    average_member_points = serializers.FloatField()