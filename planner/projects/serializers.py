from rest_framework import serializers

from .models import Project

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:

        model = Project

        fields = '__all__'
        # read chyunne time active status indavanam  write chyumbo venda

        read_only_fields = ['active_status']

