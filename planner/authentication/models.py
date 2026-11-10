from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.


class rolechoices(models.TextChoices):

    ADMIN = 'Admin', 'Admin'

    COORDINATOR = 'Project Coordinator', 'Project Coordinator'

    DEVELOPER = 'Developer','Developer'


class TechChoices(models.TextChoices):

    BACKEND = 'Backend Developer','Backend Developer'

    FRONTEND = 'Frontend Developer','Frontend Developer'

    FULLSTACK = 'Fullstack Developer','Fullstack Developer'

    UI_UX = 'UI/UX Designer','UI/UX Designer'

    TESTER = 'Software Tester','Software Tester'

class Profile(AbstractUser):

    role = models.CharField(max_length=20, choices=rolechoices.choices)

    tech = models.CharField(max_length=30,choices=TechChoices.choices,null=True,blank=True)

    class Meta:

        verbose_name = 'Profile'

        verbose_name_plural = 'Profiles'

    def __str__(self):

        return self.first_name if self.first_name else self.username
