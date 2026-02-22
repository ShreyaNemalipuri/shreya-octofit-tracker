"""
Views for Profile model
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Profile model
    - list: get all profiles
    - create: create a new profile
    - retrieve: get a specific profile by id
    - update: update a profile
    - destroy: delete a profile
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        """Create a new profile"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Update a profile"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        """Fetch a specific profile by id"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_name(self, request):
        """Fetch profiles by name"""
        name = request.query_params.get('name', None)
        if name:
            profiles = Profile.objects.filter(name__icontains=name)
            serializer = self.get_serializer(profiles, many=True)
            return Response(serializer.data)
        return Response({'error': 'name parameter is required'}, status=status.HTTP_400_BAD_REQUEST)