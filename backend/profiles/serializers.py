"""
Serializers for Profile model
"""
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer for Profile model"""
    id = serializers.SerializerMethodField()
    team_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    team = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'name', 'age', 'grade', 'team', 'team_id', 'total_points', 'created_at', 'updated_at']
        read_only_fields = ['total_points', 'created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        if obj.id:
            return str(obj.id)
        return None
    
    def get_team(self, obj):
        """Return team details"""
        if obj.team:
            return {
                'id': str(obj.team.id),
                'name': obj.team.name,
                'total_points': obj.team.total_points
            }
        return None
    
    def validate_team_id(self, value):
        """Validate that team exists"""
        if value is None:
            return None
        
        from teams.models import Team
        try:
            Team.objects.get(id=value)
        except Team.DoesNotExist:
            raise serializers.ValidationError("Team with this ID does not exist")
        return value
    
    def create(self, validated_data):
        """Create profile with optional team assignment"""
        team_id = validated_data.pop('team_id', None)
        profile = Profile.objects.create(**validated_data)
        
        if team_id:
            from teams.models import Team
            team = Team.objects.get(id=team_id)
            profile.team = team
            profile.save()
        
        return profile
    
    def update(self, instance, validated_data):
        """Update profile with optional team assignment"""
        team_id = validated_data.pop('team_id', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if team_id is not None:
            if team_id is None:
                instance.team = None
            else:
                from teams.models import Team
                team = Team.objects.get(id=team_id)
                instance.team = team
        
        instance.save()
        return instance