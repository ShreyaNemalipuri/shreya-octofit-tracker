"""
Views for Team model
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Avg
from .models import Team
from .serializers import TeamSerializer, TeamSummarySerializer


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team model
    - list: get all teams
    - create: create a new team
    - retrieve: get a specific team by id
    - update: update a team
    - destroy: delete a team
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    
    def create(self, request, *args, **kwargs):
        """Create a new team"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """Fetch a specific team by id"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update a team"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get top teams ranked by total_points"""
        teams = Team.objects.all().annotate(
            member_count=Count('members'),
            avg_member_points=Avg('members__total_points')
        ).order_by('-total_points')
        
        summary_data = []
        for rank, team in enumerate(teams, 1):
            avg_points = team.avg_member_points or 0.0
            summary_data.append({
                'team': team,
                'rank': rank,
                'average_member_points': avg_points
            })
        
        serializer = TeamSummarySerializer(summary_data, many=True)
        return Response(serializer.data)