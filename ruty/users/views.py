from django.http import Http404
from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import User, surveyResponse, Group, Message
from .serializers import UserSerializer, SurveyResponseSerializer, GroupDetailSerializer, MessageSerializer

# Create your views here.
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UpdateProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def put(self, request):
        user=request.user
        serializer=UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SurveyResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user=request.user
        serializer=SurveyResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserGroupView(generics.RetrieveAPIView):
    serializer_class = GroupDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        membership = self.request.user.group_memberships.first()
        if membership:
            return membership.group
        raise Http404("Group not found")

class MessageListView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        group_id = self.kwargs['group_id']

        if self.request.user.group_memberships.filter(group__id=group_id).exists():
            return Message.objects.filter(group__id=group_id)
        return Message.objects.none()
         
         
