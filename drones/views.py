from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from drones.models import DroneCategory,Drone,Pilot,Competition
from drones.serializers import DroneCategorySerializer,DroneSerializer,PilotSerializer,PilotCompetitionSerializer

from rest_framework import filters #filters.FilterSet deprecated
# from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter
from django_filters import rest_framework as dfilters  #using this instead of rest_framework.filters.FilterSet

# permission classes
from rest_framework import permissions
from drones import custompermission

class DroneCategoryList(generics.ListCreateAPIView):
    """
    Return a list of all the drone categories that 
    present within the queryset, with optional filtering.
    ?search=<search-text>
    &ordering=<ordeing keyr>
    &filter=<>
    """
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'
    filter_fields=(
        'name',
        )
    search_fields=(
        '^name',
        )
    ordering_field=(
        'name',
        )

class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'

class DroneList(generics.ListCreateAPIView):
    """
    Return a list of all the drones that 
    present within the queryset, with optional filtering.
    ?search=<search-text>&ordering=<ordering key>&<any of the filtering_fields key below>

    ie 127.0.0.1:8000/drones/?drone-category=1
    """
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'
    filter_fields=(
        'name', #name of the drone
        'drone_category', #id of drone category
        'manufacturing_date', #manufacturing datetime delta of the drone
        'has_it_competed', #bool value 
        )
    search_fields=(
        '^name',
        )
    ordering_field=(
        'name',
        'manufacturing_date',
        )
    
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentUserOwnerOrReadOnly,
        )
    
    #overriding the perform_create method in the 
    #ListCreateAPIView super class
    def perform_create(self,serializer):
        return serializer.save(owner=self.request.user)

class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        custompermission.IsCurrentUserOwnerOrReadOnly,
        )

class PilotList(generics.ListCreateAPIView):
    """
    Return a list of all the pilots that is 
    present within the queryset, with optional filtering.
    ?search=<search-text>
    &ordering=<ordering key>
    &<any of the filtering_fields key below>

    ie 127.0.0.1:8000/drones/?name=
    """
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'
    filter_fields=(
        'name',
        'gender',
        'race_count',
        )
    search_fields=(
        '^name',
        )
    ordering_field=(
        'name',
        'race_count',
        )

class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'

class CompetitionFilter(dfilters.FilterSet):
    from_achievement_date = dfilters.DateTimeFilter(field_name='distance_achievement_date', lookup_expr='gte')
    to_achievement_date = dfilters.DateTimeFilter(field_name='distance_achievement_date', lookup_expr='lte')
    min_distance_in_feet = dfilters.NumberFilter(field_name='distance_in_feet', lookup_expr='gte')
    max_distance_in_feet = dfilters.NumberFilter(field_name='distance_in_feet', lookup_expr='lte')
    drone_name = dfilters.AllValuesFilter(field_name='drone__name')
    pilot_name = dfilters.AllValuesFilter(field_name='pilot__name')
    class Meta:
        model = Competition
        fields = (
            'distance_in_feet',
            'from_achievement_date',
            'to_achievement_date',
            'min_distance_in_feet',
            'max_distance_in_feet',
            # drone__name will be accessed as drone_name
            'drone_name',
            # pilot__name will be accessed as pilot_name
            'pilot_name',
            )

class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'
    filter_backends = (dfilters.DjangoFilterBackend,)
    filter_class = CompetitionFilter
    # ordering_fields = (
    #     'distance_in_feet',
    #     'distance_achievement_date',
    #     )

class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse(DroneCategoryList.name,request=request),
            'drones': reverse(DroneList.name, request=request),
            'pilots': reverse(PilotList.name, request=request),
            'competitions': reverse(CompetitionList.name, request=request)
            })

