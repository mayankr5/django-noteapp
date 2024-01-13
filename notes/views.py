from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUser(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response({'status': 403, 'error': serializer.errors, 'message': 'something went wrong'})

# class LoginUser(APIView):
#     def post(self, request):
#         serializers = UserSerializer(data=request.data)
        

class NotesAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        notes_objs = Note.objects.filter(owner=user)
        serializer = NoteSerializer(notes_objs, many=True)
        return Response({'status': 200, 'data': serializer.data})
 
    def post(self, request):
        note = request.data
        note['owner'] = request.user.id
        serializer = NoteSerializer(data = note)
        if not serializer.is_valid():
            return Response({'status': 403, 'error': serializer.errors, 'message': 'something went wrong'})

        serializer.save()
        return Response({'status': 201 , 'data': serializer.data, 'message': 'Created successfully'})

class NotesAPIByID(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            note_obj = Note.objects.filter(id = id, owner = request.user)
            serializer = NoteSerializer(note_obj)
            return Response({'status': 200, 'data': serializer.data})
        
        except Exception as e:
            return Response({'status': 403, 'error': e, 'meassage': 'invalid id'})
        
    def patch(self, request, id):
        try:
            note_obj = Note.objects.filter(id = id, owner = request.user)
            serializer = NoteSerializer(note_obj, data = request.data, partial=True)
            if not serializer.is_valid():
                return Response({'status': 403, 'error': serializer.errors, 'message': 'something went wrong'})
            
            serializer.save()
            return Response({'status': 200, 'data': serializer.data, 'message': 'update successfully'})
        
        except Exception as e:
            return Response({'status': 403, 'error': e, 'meassage': 'invalid id'})
    
    def delete(self, request, id):
        try:
            note_obj = Note.objects.filter(id = id , owner = request.user)
            note_obj.delete()
            return Response({'status': 200, 'message': 'Delete successfully'})
        
        except Exception as e:
            return Response({'status': 403, 'error': e, 'meassage': 'invalid id'})
