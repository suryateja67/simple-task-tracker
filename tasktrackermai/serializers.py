from rest_framework import serializers
from .models import CustomUser,Task,TaskAssignment,Team,TeamMember


class customuserserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        Fields=['userid','email','role','password']
    def validate(self,data):
        if data['username']:
            if CustomUser.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username is taken')
        if data('email'):
            if CustomUser.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email has been taken')
        return data
    def create_user(self,validated_data):
        user=CustomUser.objects.create(email=validated_data['email'],username=validated_data['username'],role=validated_data['role'])
        user.set_password(validated_data['password'])
        user.save()
        return validated_data
    
class teamserializer(serializers.ModelSerializer):
    team_leader=customuserserializer()
    team_members=serializers.SerializerMethodField()
    class Meta:
        model=Team
        fields='__all__'
    def get_team_members(self,obj):
        team_members=TeamMember.objects.filter(team=obj.id)
        res=[]
        for mem in team_members:
            res.append(customuserserializer(mem.user).data)
        return res
class taskserializer(serializers.ModelSerializer):
    team=teamserializer()
    TaskAssignment=serializers.SerializerMethodField()
    class meta:
        model=Team
        fields='__all__'
    def get_TaskAssignment(self,obj):
        task_members=TaskAssignment.objects.filter(task=obj)
        mems=[]
        for mem in task_members:
            mems.append(customuserserializer(mem.user).data)
        return mems
            
















