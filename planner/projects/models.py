from django.db import models

import uuid

from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.

class BaseClass(models.Model):

    uuid = models.UUIDField(unique=True,default=uuid.uuid4)   #Primary Key

    active_status = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)  #to impliment 'now' from MySQL

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

    tentative_end_date = models.Dat


#   Project reladed assign egane edukam? 

# project = record

# AssignedProject.objects.get(project=project)

# project.assignedProject ----> reverse pickup

# related name --> to name the assiggnedProject