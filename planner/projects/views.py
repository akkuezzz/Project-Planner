from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView #instead of APIview

from .models import Project

from .serializers import ProjectSerializer

from authentication.models import Profile

# Create your views here.  

class ProjectListCreateView(ListCreateAPIView):     #To create LIST AND SERIALIZERS

    queryset = Project.objects.filter(active_status=True)                 #objects.all  but filtered onces

    serializer_class = ProjectSerializer

class ProjectRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Project.objects.filter(active_status=True)                 #objects.all  but filtered onces

    serializer_class = ProjectSerializer        #its only expects PK(Primary KEY)  int/  for now we use uuid

    # put means all update 

    # patch means Parsal update

    #permant delete akaruth active status false akanam delete chyumbo

    def perform_destroy(self, instance):  #instanse 
        
        instance.active_status = False

        instance.save() #manually update chyunnu