from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.views import Token
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class RegisterUser(APIView):
    def post(request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = User.objects.get(username=request.data['username'])
            user.set_password(request.data['password'])
            user.save()
            token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': serializer.data})
        return Response({'status': 403, 'error': serializer.errors, 'message': 'something went wrong'})


class NotesAPI(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        notes_objs = Note.objects.all()
        serializer = NoteSerializer(notes_objs, many=True)
        return Response({'status': 200, 'data': serializer.data})
 
    def post(self, request):
        serializer = NoteSerializer(data = request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'error': serializer.errors, 'message': 'something went wrong'})

        serializer.save()
        return Response({'status': 201 , 'data': serializer.data, 'message': 'Created successfully'})

class NotesAPIByID(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            note_obj = Note.objects.get(id = id)
            serializer = NoteSerializer(note_obj)
            return Response({'status': 200, 'data': serializer.data})
        
        except Exception as e:
            return Response({'status': 403, 'error': e, 'meassage': 'invalid id'})
        
    def patch(self, request, id):
        try:
            note_obj = Note.objects.get(id = id)
            serializer = NoteSerializer(note_obj, data= request.data, partial=True)
            if not serializer.is_valid():
                return Response({'status': 403, 'error': serializer.errors, 'message': 'something went wrong'})
            
            serializer.save()
            return Response({'status': 200, 'data': serializer.data, 'message': 'update successfully'})
        
        except Exception as e:
            return Response({'status': 403, 'error': e, 'meassage': 'invalid id'})
    
    def delete(self, request, id):
        try:
            note_obj = Note.objects.get(id = id)
            note_obj.delete()
            return Response({'status': 200, 'message': 'Delete successfully'})
        
        except Exception as e:
            return Response({'status': 403, 'error': e, 'meassage': 'invalid id'})
