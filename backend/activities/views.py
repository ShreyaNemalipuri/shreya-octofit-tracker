"""
Views for Activity model
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from .models import Activity
from .serializers import ActivitySerializer, ActivitySummarySerializer
from profiles.models import Profile


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity model
    - list: get all activities
    - create: create a new activity
    - retrieve: get a specific activity by id
    - update: update an activity
    - destroy: delete an activity
    """
    serializer_class = ActivitySerializer
    
    def get_queryset(self):
        """Filter activities by user if user_id is provided"""
        queryset = Activity.objects.all()
        user_id = self.request.query_params.get('user_id', None)
        
        if user_id is not None:
            queryset = queryset.filter(user_id=user_id)
        
        return queryset
    
    def create(self, request, *args, **kwargs):
        """Create a new activity"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        """Fetch a specific activity by id"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """Update an activity"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'])
    def user_activities(self, request):
        """Fetch activities for a specific user"""
        user_id = request.query_params.get('user_id', None)
        
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        activities = Activity.objects.filter(user_id=user_id)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get activity summary for a user"""
        user_id = request.query_params.get('user_id', None)
        
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        activities = Activity.objects.filter(user_id=user_id)
        
        # Calculate totals
        totals = activities.aggregate(
            total_duration=Sum('duration_minutes'),
            total_distance=Sum('distance_km'),
            total_points=Sum('points'),
            count=Count('id')
        )
        
        # Activities by type
        activities_by_type = {}
        for activity_type, _ in Activity.ACTIVITY_CHOICES:
            count = activities.filter(activity_type=activity_type).count()
            if count > 0:
                activities_by_type[activity_type] = count
        
        summary_data = {
            'user': user,
            'total_activities': totals['count'] or 0,
            'total_duration_minutes': totals['total_duration'] or 0,
            'total_distance_km': totals['total_distance'] or 0.0,
            'total_points': totals['total_points'] or 0,
            'activities_by_type': activities_by_type
        }
        
        serializer = ActivitySummarySerializer(summary_data)
        return Response(serializer.data)