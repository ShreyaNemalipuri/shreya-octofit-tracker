"""
Serializers for Profile model
"""
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    id = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'name', 'age', 'grade', 'team', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        if obj.id:
            return str(obj.id)
        return None