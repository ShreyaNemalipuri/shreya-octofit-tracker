"""
Serializers for Activity model
"""
from rest_framework import serializers
from .models import Activity
from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    id = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(write_only=True)
    user = ProfileSerializer(read_only=True)
    activity_type_display = serializers.CharField(
        source='get_activity_type_display',
        read_only=True
    )
    
    class Meta:
        model = Activity
        fields = [
            'id', 'user', 'user_id', 'activity_type', 'activity_type_display',
            'duration_minutes', 'distance_km', 'calories', 'date', 'points',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['points', 'created_at', 'updated_at']
    
    def get_id(self, obj):
        """Convert ObjectId to string"""
        if obj.id:
            return str(obj.id)
        return None
    
    def validate_user_id(self, value):
        """Validate that user exists"""
        try:
            Profile.objects.get(id=value)
        except Profile.DoesNotExist:
            raise serializers.ValidationError("Profile with this ID does not exist")
        return value
    
    def create(self, validated_data):
        """Create activity and update user's total_points"""
        user_id = validated_data.pop('user_id')
        user = Profile.objects.get(id=user_id)
        
        activity = Activity.objects.create(
            user=user,
            **validated_data
        )
        return activity


class ActivitySummarySerializer(serializers.Serializer):
    """Serializer for activity summary statistics"""
    user = ProfileSerializer()
    total_activities = serializers.IntegerField()
    total_duration_minutes = serializers.IntegerField()
    total_distance_km = serializers.FloatField()
    total_points = serializers.IntegerField()
    activities_by_type = serializers.DictField(child=serializers.IntegerField())