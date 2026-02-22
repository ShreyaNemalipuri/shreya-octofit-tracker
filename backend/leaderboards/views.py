"""
Views for Leaderboard endpoints
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from profiles.models import Profile
from teams.models import Team
from .serializers import StudentLeaderboardSerializer, TeamLeaderboardSerializer


class LeaderboardViewSet(viewsets.ViewSet):
    """
    ViewSet for Leaderboard endpoints
    - students: top students by total_points
    - teams: top teams by total_points
    """
    
    @action(detail=False, methods=['get'], url_path='students')
    def students(self, request):
        """Get top students by total_points"""
        try:
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            limit = 10
        
        # Ensure limit is positive
        if limit < 1:
            limit = 10
        
        # Get top students ordered by total_points descending
        top_students = Profile.objects.order_by('-total_points', 'id')[:limit]
        
        # Build leaderboard with ranks
        leaderboard_data = []
        for rank, student in enumerate(top_students, 1):
            leaderboard_data.append({
                'rank': rank,
                'id': str(student.id),
                'name': student.name,
                'total_points': student.total_points
            })
        
        serializer = StudentLeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='teams')
    def teams(self, request):
        """Get top teams by total_points"""
        try:
            limit = int(request.query_params.get('limit', 10))
        except ValueError:
            limit = 10
        
        # Ensure limit is positive
        if limit < 1:
            limit = 10
        
        # Get top teams ordered by total_points descending
        top_teams = Team.objects.order_by('-total_points', 'id')[:limit]
        
        # Build leaderboard with ranks
        leaderboard_data = []
        for rank, team in enumerate(top_teams, 1):
            leaderboard_data.append({
                'rank': rank,
                'id': str(team.id),
                'name': team.name,
                'total_points': team.total_points
            })
        
        serializer = TeamLeaderboardSerializer(leaderboard_data, many=True)
        return Response(serializer.data)