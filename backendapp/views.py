from django.core.exceptions import ObjectDoesNotExist
# https://api-promovers.herokuapp.com/
# usertwo@users.com token: aa25ca8f13c18c5ef66607558c4554ee3ec8813f

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.views import APIView 

from .models import User, Request, RegUser, Mover
from .serializers import UserSerializer, RequestSerializer, RegUserSerializer, MoverSerializer

from django.conf import settings
from django.core.mail import send_mail
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['email'] = user.email
        token['username'] = user.username

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        acc_type = request.data['acc_type']
        data = {}
        if instance := serializer.create(validated_data=request.data):
            # token = Token.objects.get(user=instance).key
            # The email section
            subject = 'Welcome to ProMovers'
            if acc_type == "mover":
                message = f"Hi {instance.username}, thank you for registering in as a mover on ProMovers. Where we will connect you to potential clients."
            else:
                message = f"Hi {instance.username}, thank you for registering in as a user on ProMovers."
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [instance.email, ]
            send_mail(subject, message, email_from, recipient_list)

            # data['token'] = token
            data['user_id'] = instance.id
            data['response'] = "User registration, successful"

            return Response(data, status=200)
        else:
            data['response'] = "User registration, failed"
            return Response(data, status=400)


@api_view(['PUT'])
def api_update_user_profile(request):
    if user_id := request.data['user']:
        if user := RegUser.get_user_user_by_id(user_id):
            serializer = RegUserSerializer(user, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = {"message": "Update was successful"}
                return Response(data, status=200)
        else:
            data = {"message": "User doesn't exist"}
            return Response(data, status=404)
    else:
        data = {"message": "Invalid user"}
        return Response(data, status=400)


@api_view(['PUT'])
def api_update_mover_profile(request):
    if user_id := request.data['user']:
        if mover := Mover.get_mover_user_by_id(user_id):
            serializer = MoverSerializer(mover, request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                data = {"message": "Update was successful"}
                return Response(data, status=200)
        else:
            data = {"message": "Mover doesn't exist"}
            return Response(data, status=404)
    else:
        data = {"message": "Invalid user"}
        return Response(data, status=400)



@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def api_get_all_users(request):
    users = RegUser.objects.all()
    serializer = RegUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def api_get_all_movers(request):
    movers = Mover.objects.all()
    serializer = MoverSerializer(movers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def api_get_specific_user(request, username):
    try:
        users = RegUser.objects.get(user__username=username)
        serializer = RegUserSerializer(users, many=False)
        return Response(serializer.data, status=200)
    except ObjectDoesNotExist:
        return Response({"response": "404"}, status=404)


@api_view(['GET'])
# @permission_classes((IsAuthenticated,))
def api_get_specific_mover(request, username):
    try:
        users = Mover.objects.get(user__username=username)
        serializer = RegUserSerializer(users, many=False)
        return Response(serializer.data, status=200)
    except ObjectDoesNotExist:
        return Response({"response": "404"}, status=404)


class new_move_request(APIView):
    def post(self,request,*args,**kwargs):
        draft_request_data = request.data.copy()
        id_mover = draft_request_data["id_mover"]
        id_user = draft_request_data["id_user"]
        mover = Mover.objects.get(id=id_mover)
        user = RegUser.objects.get(id=id_user)
        draft_request_data["user"] = user.id
        draft_request_data["mover"] = mover.id
        kwargs["data"] = draft_request_data
        serializer = RequestSerializer(data=draft_request_data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        serializer.save()
        return Response(serializer.data)




class api_get_all_users_requests(APIView):
    def get(self,request,username,*args,**kwargs):
        users = Request.objects.filter(user__full_name=username).all()
        serializer = RequestSerializer(users,many=True)
        return Response(serializer.data)

class api_get_all_movers_requests(APIView):
    def get(self,request,username,*args,**kwargs):
        users = Request.objects.filter(mover__user__username=username).all()
        serializer = RequestSerializer(users,many=True)
        return Response(serializer.data)

class api_get_all_requests(APIView):
    def get(self,request,*args,**kwargs):
        users = Request.objects.all()
        serializer = RequestSerializer(users,many=True)
        return Response(serializer.data)

