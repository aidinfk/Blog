from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Profile
from .helpers import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login



class LoginView(APIView):
    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong!'

        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'Key of username not found!'
                raise Exception('Key of username not found!')

            if data.get('password') is None:
                response['message'] = 'Key of password not found!'
                raise Exception('Key of password not found!')
            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user is None:
                response['message'] = 'Invalid username, user not found!'
                raise Exception('Invalid username, user not found!')

            if not Profile.objects.filter(user = check_user).first().is_verified:
                response['message'] = 'Your profile is not verified!'
                raise Exception('Profile not verified..')

            user_obj = authenticate(username = data.get('username'), password = data.get('password'))

            if user_obj:
                login(request, user_obj)
                response['status'] = 200
                response['message'] = 'Welcome!'

            else:
                response['message'] = 'Invalid password!'
                raise Exception('Invalid password!')


        except Exception as e:
            print(e)

        return Response(response)


LoginView = LoginView.as_view()


class RegisterView(APIView):
    def post(self, request):
        response = {}
        response['status'] = 500
        response['message'] = 'Something went wrong!'

        try:
            data = request.data

            if data.get('username') is None:
                response['message'] = 'Key of username not found!'
                raise Exception('Key of username not found!')

            if data.get('password') is None:
                response['message'] = 'Key of password not found!'
                raise Exception('Key of password not found!')

            check_user = User.objects.filter(username = data.get('username')).first()

            if check_user:
                response['message'] = 'Username create successfully!'
                raise Exception('Username already taken!')


            user_obj = User.objects.create(email = data.get('username'), username = data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            token = generate_random_string(20)
            Profile.objects.create(user = user_obj, token = token)
            send_mail_to_user(token, data.get('useername'))

            response['message'] = 'User created successfully!'
            response['status'] = 200


        except Exception as e:
            print(e)

        return Response(response)


RegisterView = RegisterView.as_view()