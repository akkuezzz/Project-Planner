from rest_framework import serializers

from .models import Profile



class ProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = Profile

        fields = ['username','email','password','role']


        # write_only_fields = ['password']     #(write only)
        
        extra_kwargs = {

            'password': {'write_only':True} 
        }


        read_only_fields = ['email'] 

