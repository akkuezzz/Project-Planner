from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView #instead of APIview

from .models import Project

from .serializers import ProjectSerializer

from authentication.models import Profile

from . models import AssignedProject,Task

from .serializers import AssignedProjectSerializer,TaskSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

from planner.utils import generate_tasks

from django.db import transaction

from planner.pageinations import CustomPageination

# Create your views here.  

class ProjectListCreateView(ListCreateAPIView):     #To create LIST AND SERIALIZERS

    pagination_class = CustomPageination

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



class AssignedProjectListCreateView(ListCreateAPIView):

    pagination_class = CustomPageination
                                                # one to one                          many to many 
    queryset = AssignedProject.objects.all().select_related('project','coordinator').prefetch_related('developers')   #code effiecnt akan?
 
    # n+one query problem ? 

    serializer_class = AssignedProjectSerializer


class AssignedProjectRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = AssignedProject.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')   #code effiecnt akan?
 
    # n+one query problem ? 

    serializer_class = AssignedProjectSerializer


    # put means all update 

    # patch means Parsel update

    # permanent delete agaruth active status false akanam delete chyumbo

    def perform_destroy(self, instance):  #instanse 
        
        instance.active_status = False

        instance.save() #manually update chyunnu

class TaskListCreateView(ListCreateAPIView):

    pagination_class = CustomPageination

    def get_queryset(self):

        uuid = self.request.query_params.get('project')

        #taking given data using post method ----- self.request.data
        # 
        # Task.objects.filter(assigned_Project__uuid='uuid')

        # Reverse Pickup-------


        if uuid:

            assigned_project = AssignedProject.objects.get(uuid=uuid)

            # task = assigned_project.task_set.all() #revverse pickup without related name

        # related name models il use akkiyal ath use akiyal mmath
            tasks = assigned_project.assigned_task.filter(active_status=True).select_related('assigned_project','assigned_to') #revverse pickup with related name

            return tasks
        
        return Task.objects.none()
    
    serializer_class = TaskSerializer



class TaskProjectRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Task.objects.filter(active_status=True).select_related('assigned_project','assigned_to')   

    serializer_class = TaskSerializer


    def perform_destroy(self, instance):  
        
        instance.active_status = False

        instance.save() #manually update chyunnu


class TaskcreatewithAi(APIView):

    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        try :

            assigned_project = AssignedProject.objects.get(uuid=uuid)

            result = generate_tasks(assigned_project)

            # print(result.tasks)

            tasks = [Task(title = task.title,
                        description = task.description,
                        assigned_project=assigned_project,
                        assigned_to_id = task.developer_id,    #__ id enu anu meaning
                        priority = task.priority) for task in result.tasks] 


            with transaction.atomic():

                Task.objects.bulk_create(tasks)     #(bulk save akan)

                data = {'msg':'Tasks assigned successfully'}

            # task.save()

                return Response(status=200)

        except Exception as e:

            print(e)


            data= {'msg':'Failed to create Tasks'}

            return Response(data,status=400)


