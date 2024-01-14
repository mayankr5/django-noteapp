from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.throttling import UserRateThrottle

# Create your views here.

class RegisterUser(APIView):
    throttle_classes = [UserRateThrottle]
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

class LoginUser(APIView):
    throttle_classes = [UserRateThrottle]
    def post(self, request):
        user = authenticate(
            username=request.data.get("username"),
            password=request.data.get("password")
            )
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except Token.DoesNotExist:
                token = Token.objects.create(user=user)
            return Response({'token': token.key, 'user': user.username})
        return Response({'status': 401,'message': "unautherised user"})
        
class LogoutUser(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

class NotesAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
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
    throttle_classes = [UserRateThrottle]
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
