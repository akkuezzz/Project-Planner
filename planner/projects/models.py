from django.db import models

import uuid

from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)   #Primary Key

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)  #to implement 'now' from MySQL

    # auto_now_add=  once create time cannot use when update
    
    # auto_now= 
    update_at = models.DateTimeField(auto_now=True)

    class Meta :

        abstract = True  #To let django know about the model

class Project(BaseClass):

    title = models.CharField(max_length=255)

    description = CKEditor5Field()

    documentation = models.FileField(upload_to='project-documents')

    class Meta:

        verbose_name = 'Projects'

        verbose_name_plural = 'Projects'


    def __str__(self):

        return self.title

#its not visible field project
class AssignedProject(BaseClass):   #to assign dev or other users or fields

    project = models.OneToOneField('Project',on_delete=models.PROTECT)   #if assigned project gets deleted, it refuses to be delete

    coordinator = models.ForeignKey('authentication.Profile',on_delete=models.PROTECT,related_name='coordinator')   # related models  (same model use chyunne time issue indavum)

    developers = models.ManyToManyField('authentication.Profile',related_name='developers')

    duration = models.PositiveBigIntegerField()

    start_date = models.DateField()

    tentative_end_date = models.DateField()

    project_completed = models.BooleanField(default=False)

    class Meta:

        verbose_name = 'Assigned Projects'

        verbose_name_plural = 'Assigned Projects'


    def __str__(self):

        return f'{self.project.title}-{self.coordinator.first_name}'


#   Project related assign egane edukam? 

# project = record

# AssignedProject.objects.get(project=project)

# project.assignedProject ----> reverse pickup

# related name --> to name the assignedProject

class PriorityChoice(models.TextChoices):

    LOW = 'Low','Low'

    MEDIUM = 'Medium','Medium'

    HIGH = 'High','High'

class Task(BaseClass):

    title = models.CharField(max_length=255)

    description = models.TextField()

    assigned_project = models.ForeignKey('AssignedProject',on_delete=models.PROTECT,related_name='assigned_task')

    assigned_to = models.ForeignKey('authentication.Profile',on_delete=models.PROTECT)

    priority = models.CharField(max_length=10,choices=PriorityChoice.choices)

    duration = models.TimeField(null=True,blank=True)

    start_date = models.DateField(null=True,blank=True)

    end_date = models.DateField(null=True,blank=True)

    task_completed = models.BooleanField(default=True)

    class Meta:

        verbose_name = 'Task'

        verbose_name_plural = 'Task'

    def __str__(self):

        return f'{self.title}-{self.assigned_to.first_name}'




