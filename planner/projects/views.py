
from django.shortcuts import render

from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .models import Project,Task

from .serializers import Projectserializer

from authentication.models import Profile

from .models import AssignedProject

from .serializers import AssignedProjectserializer

from .serializers import TaskSerializer

from rest_framework.views import APIView

from rest_framework.response import Response

from planner.utils import generate_tasks

from django.db import transaction

from planner.paginations import CustomPagination

from rest_framework_simplejwt.authentication import JWTAuthentication

from authentication.permissions import IsAdmin,IsCoordinator,IsDeveloper

from rest_framework.permissions import IsAuthenticated

# Create your views here.

class ProjectListCreateView(ListCreateAPIView):

    pagination_class = CustomPagination

    queryset = Project.objects.filter(active_status=True)

    serializer_class = Projectserializer

    http_method_names = ['get','post']

    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['POST']:

            permissions = [IsAdmin]

        else:

            permissions = [IsAuthenticated]

            return [permissions() for permission in permissions]
        

class ProjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Project.objects.filter(active_status=True)

    serializer_class = Projectserializer

    http_method_names = ['get','patch','delete']

    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['PATCH','DELETE']:

            permissions = [IsAdmin]

        else:

            permissions = [IsAuthenticated]

            return [permissions() for permission in permissions]
        
    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()

class AssignedProjectListCreateView(ListCreateAPIView):

    pagination_class = CustomPagination
    
    queryset = AssignedProject.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')

    serializer_class = AssignedProjectserializer
    
    http_method_names = ['get','post']

    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['POST']:

            permissions = [IsAdmin]

        else:

            permissions = [IsAuthenticated]

            return [permissions() for permission in permissions]

class AssignedProjectRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = AssignedProject.objects.filter(active_status=True)

    serializer_class = AssignedProjectserializer

    http_method_names = ['get','post','delete']


    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['PATCH','DELETE']:

            permissions = [IsAdmin]

        else:

            permissions = [IsAuthenticated]

            return [permissions() for permission in permissions]

    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()

class TaskListCreateView(ListCreateAPIView):

    pagination_class = CustomPagination
    

    def get_queryset(self):

        uuid = self.request.query_params.get('project')

        # Task.objects.filter(assigned_project__uuid=uuid)

        if uuid:

            assigned_project = AssignedProject.objects.get(uuid=uuid)

            # tasks = assigned_project.task_set.all()   reverse lookup without related_name
            
            tasks = assigned_project.assigned_tasks.filter(active_status=True).select_related('assigned_project','assigned_to')

            return tasks

        return Task.objects.all()


    serializer_class = TaskSerializer

    http_method_names = ['get','post']


    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['POST']:

            permissions = [IsCoordinator]

        else:

            permissions = [IsAuthenticated]

            return [permissions() for permission in permissions]

class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):

    lookup_field = 'uuid'

    queryset = Task.objects.filter(active_status=True).select_related('assigned_project','assigned_to')

    serializer_class = TaskSerializer

    http_method_names = ['get','post','delete']


    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['PATCH','DELETE']:

            permissions = [IsCoordinator]

        else:

            permissions = [IsAuthenticated]

            return [permissions() for permission in permissions]

    def perform_destroy(self, instance):

        instance.active_status = False

        instance.save()

class TaskCreateWithAI(APIView):

    http_method_names = ['post']


    permission_classes = [JWTAuthentication]

    def get_permissions(self):

        permissions = []

        if self.request.method in ['POST']:

            permissions = [IsCoordinator]

            return [permissions() for permission in permissions]

    def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        try:

            assigned_project = AssignedProject.objects.get(uuid=uuid)
    
            result = generate_tasks(assigned_project)

            tasks = [Task(title=task.title,
                      description=task.description,
                      assigned_project=assigned_project,
                      assigned_to_id=task.developer_id,
                      priority=task.priority) for task in result.tasks]

            with transaction.atomic():

                Task.objects.bulk_create(tasks)

                data = {'msg':'Tasks assigned successfully'}

                return Response(data,status=200)

        except Exception as e:

            data = {'msg':'Failed to create tasks'}

            return Response(data,status=400)


# from django.shortcuts import render

# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView #instead of APIview

# from .models import Project

# from .serializers import ProjectSerializer

# from authentication.models import Profile

# from . models import AssignedProject,Task

# from .serializers import AssignedProjectSerializer,TaskSerializer

# from rest_framework.views import APIView

# from rest_framework.response import Response

# from planner.utils import generate_tasks

# from django.db import transaction

# from planner.pageinations import CustomPageination

# from rest_framework_simplejwt.authentication import JWTAuthentication

# # Create your views here.  

# class ProjectListCreateView(ListCreateAPIView):     #To create LIST AND SERIALIZERS


#     pagination_class = CustomPageination

#     queryset = Project.objects.filter(active_status=True)                 #objects.all  but filtered onces

#     serializer_class = ProjectSerializer

# class ProjectRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):

#     # lookup_field = 'uuid'

#     # queryset = Project.objects.filter(active_status=True)                 #objects.all  but filtered onces

#     # serializer_class = ProjectSerializer        #its only expects PK(Primary KEY)  int/  for now we use uuid

#     # put means all update 

#     # patch means Parsal update

#     #permant delete akaruth active status false akanam delete chyumbo

#     permission_classes = [JWSAuthentication]

#     def get_permissions(self):

#         permissions = []

#         if self.request.method in [POST] :

#             permissions = [IsAdmin]

#         else :

#             permissions = [IsAuthenticated]
                       
#         return [permission() for permission in permissions]



#     def perform_destroy(self, instance):  #instanse 
        
#         instance.active_status = False

#         instance.save() #manually update chyunnu



# class AssignedProjectListCreateView(ListCreateAPIView):

#     pagination_class = CustomPageination
#                                                 # one to one                          many to many 
#     queryset = AssignedProject.objects.all().select_related('project','coordinator').prefetch_related('developers')   #code effiecnt akan?
 
#     # n+one query problem ? 

#     serializer_class = AssignedProjectSerializer


# class AssignedProjectRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):

#     lookup_field = 'uuid'

#     queryset = AssignedProject.objects.filter(active_status=True).select_related('project','coordinator').prefetch_related('developers')   #code effiecnt akan?
 
#     # n+one query problem ? 

#     serializer_class = AssignedProjectSerializer


#     # put means all update 

#     # patch means Parsel update

#     # permanent delete agaruth active status false akanam delete chyumbo

#     def perform_destroy(self, instance):  #instanse 
        
#         instance.active_status = False

#         instance.save() #manually update chyunnu

# class TaskListCreateView(ListCreateAPIView):

#     pagination_class = CustomPageination

#     def get_queryset(self):

#         uuid = self.request.query_params.get('project')

#         #taking given data using post method ----- self.request.data
#         # 
#         # Task.objects.filter(assigned_Project__uuid='uuid')

#         # Reverse Pickup-------


#         if uuid:

#             assigned_project = AssignedProject.objects.get(uuid=uuid)

#             # task = assigned_project.task_set.all() #revverse pickup without related name

#         # related name models il use akkiyal ath use akiyal mmath
#             tasks = assigned_project.assigned_task.filter(active_status=True).select_related('assigned_project','assigned_to') #revverse pickup with related name

#             return tasks
        
#         return Task.objects.none()
    
#     serializer_class = TaskSerializer



# class TaskProjectRetriveUpdateDestoryView(RetrieveUpdateDestroyAPIView):

#     lookup_field = 'uuid'

#     queryset = Task.objects.filter(active_status=True).select_related('assigned_project','assigned_to')   

#     serializer_class = TaskSerializer


#     def perform_destroy(self, instance):  
        
#         instance.active_status = False

#         instance.save() #manually update chyunnu


# class TaskcreatewithAi(APIView):

#     def post(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')

#         try :

#             assigned_project = AssignedProject.objects.get(uuid=uuid)

#             result = generate_tasks(assigned_project)

#             # print(result.tasks)

#             tasks = [Task(title = task.title,
#                         description = task.description,
#                         assigned_project=assigned_project,
#                         assigned_to_id = task.developer_id,    #__ id enu anu meaning
#                         priority = task.priority) for task in result.tasks] 


#             with transaction.atomic():

#                 Task.objects.bulk_create(tasks)     #(bulk save akan)

#                 data = {'msg':'Tasks assigned successfully'}

#             # task.save()

#                 return Response(status=200)

#         except Exception as e:

#             print(e)


#             data= {'msg':'Failed to create Tasks'}

#             return Response(data,status=400)



# # ------------------------------------------