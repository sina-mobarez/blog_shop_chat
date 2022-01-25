from ast import Not
from django.db.models import Q
from http.client import responses
from pickle import TRUE
from random import randint
from django.contrib.auth import authenticate, login, views as auth_views
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import generic
from django.urls import reverse_lazy
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from accounts.models import CustomUser
from webservice.serializers import UserModelLoginSerializer, UserModelSerializer
from rest_framework_simplejwt import views
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.db import IntegrityError
from .forms import LoginForm, CustomUserCreationForm
import json
from django.contrib.auth.hashers import check_password
from rest_framework import status
from webservice.serializers import UserModelSerializer
from django.contrib.auth import login
from .backends import UserModel, UserNotVerified
from datetime import timedelta
import redis
from .serializers import GetCodeVerifyPhoneNumber, VerifyPhoneNumber
import pyotp


from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic.edit import CreateView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login, get_user_model
from .utils import send_sms

from django.contrib import messages
from .forms import CustomUserCreationForm, VerifyForm



from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema





# class RefreshToken(BlacklistMixin, Token):
#     token_type = 'refresh'
#     lifetime = api_settings.REFRESH_TOKEN_LIFETIME
#     no_copy_claims = (
#         api_settings.TOKEN_TYPE_CLAIM,
#         'exp',

#         # Both of these claims are included even though they may be the same.
#         # It seems possible that a third party token might have a custom or
#         # namespaced JTI claim as well as a default "jti" claim.  In that case,
#         # we wouldn't want to copy either one.
#         api_settings.JTI_CLAIM,
#         'jti',
#     )

#     @property
#     def access_token(self):
#         """
#         Returns an access token created from this refresh token.  Copies all
#         claims present in this refresh token to the new access token except
#         those claims listed in the `no_copy_claims` attribute.
#         """
#         access = AccessToken()

#         # Use instantiation time of refresh token as relative timestamp for
#         # access token "exp" claim.  This ensures that both a refresh and
#         # access token expire relative to the same time if they are created as
#         # a pair.
#         access.set_exp(from_time=self.current_time)

#         no_copy = self.no_copy_claims
#         for claim, value in self.payload.items():
#             if claim in no_copy:
#                 continue
#             access[claim] = value

#         return access


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.username
        # ...

        return token


class LoginView(auth_views.LoginView):


    form_class = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    
    def get(self, request, *args, **kwargs):
        #if any session there is, remove phone key
        if 'phone' in self.request.session.keys():
            del self.request.session['phone']
        return super().get(self, request, *args, **kwargs)

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        try :
            login(self.request, form.get_user())
        except UserNotVerified:
            """ exception will handeled by middleware"""
            pass
        else:
            return HttpResponseRedirect(self.get_success_url())





class VerifyMixin:
    @property
    def get_user(self):
        try:
            user = UserModel.objects.get(phone=self.request.session['phone'])
            return user
        except UserModel.DoesNotExist:
            return 
        except KeyError:
            return

    @property
    def set_token(self):
        token = randint(10000, 99999)
        return str(token)
    
    def set_token_to_db(self, phone, token):
        r = redis.Redis()
        r.setex(str(f"otp{phone}"),timedelta(minutes=5),value=str(token))
        return True
       
    def get_token_from_db(self, phone):
        r = redis.Redis()
        print('>>>>>>>>', r.exists(str(f"otp{phone}")))
        if r.exists(str(f"otp{phone}")) == 1:
            otp_code = r.get(str(f"otp{phone}"))
            print('1212121221>>>>>>>>>>',eval(otp_code))
            return eval(otp_code)
        else:
            return None


class VerifyView(VerifyMixin, FormView):
    form_class = VerifyForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/verify.html'

    def get(self, request, *args, **kwargs):
        if self.get_user:
            return super().get(self, request, *args, **kwargs)
        else :
            return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        
        phone_number = self.request.session['phone']
        op =  self.get_token_from_db(phone_number)
        print('otp from db : ',type(op))
        otp_code = str(request.POST.get('otp_code'))
        print('.................',type(otp_code))
        if  str(self.get_token_from_db(phone_number)) == otp_code:
            user = self.get_user
            user.is_verified = True
            user.save()
            print('whaaaaaaaaaaaaaaaaaaaaaaaaaaat')
            messages.success(self.request,'شماره مبایل شما تایید شد')
            return super().post(self, request, *args, **kwargs)
        else :
            messages.warning(self.request,'کد تایید اشتباه است ')
            return self.form_invalid(self.form_class)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['phone']=self.request.session['phone']
        return context

class ResendVerifyView(VerifyMixin, View):
    
    def get(self, request, *args, **kwargs):
        if self.get_user:
            user = self.get_user
            phone = user.phone
            token = self.set_token
            print('==========', type(phone), '======', token)
            self.set_token_to_db(phone=phone, token=token)
            # send_sms(receptor=phone, token=token)
        return HttpResponseRedirect(reverse_lazy('verify'))




class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


# @api_view(["POST",])
# @permission_classes([AllowAny])
# def Register_Users(request):
#     try:
#         data = {}
#         serializer = UserModelSerializer(data=request.data)
#         if serializer.is_valid():
#             account = serializer.save()
#             account.is_active = True
#             account.save()
#             data["message"] = "user registered successfully"
#             data["email"] = account.email
#             data["username"] = account.username

#         else:
#             data = serializer.errors


#         return Response(data)
#     except IntegrityError as e:
#         account=CustomUser.objects.get(username='')
#         account.delete()
#         raise ValidationError({"400": f'{str(e)}'})

#     except KeyError as e:
#         print(e)
#         raise ValidationError({"400": f'Field {str(e)} missing'})

class RegisterUser(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserModelSerializer

    @swagger_auto_schema(request_body=UserModelSerializer,
                         responses={400: "you have provided invalid parameters",
                                    200: UserModelSerializer})
    def post(self, request, *args, **kwargs):
        
        try:
            data = {}
            serializer = UserModelSerializer(data=request.data)
            if serializer.is_valid():
                account = serializer.save()
                account.is_active = True
                account.save()
                time_otp = pyotp.TOTP(account.key, interval=300)
                time_otp = time_otp.now()
                
                data["message"] = "user registered successfully, and otp is sent to your number"
                data["email"] = account.email
                data["username"] = account.username

            else:
                data = serializer.errors
                return Response(
                    {
                        'message': data,
                        
                    },
                    status= status.HTTP_400_BAD_REQUEST
                )

            # send_sms(receptor=account.phone, token=time_otp)
            return Response(data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            account=CustomUser.objects.get(username='')
            account.delete()
            raise ValidationError({"400": f'{str(e)}'})

        except KeyError as e:
            print(e)
            raise ValidationError({"400": f'Field {str(e)} missing'})



# @api_view(["POST"])
# @permission_classes([AllowAny])
# def login_user(request):

#         data = {}
#         reqBody = json.loads(request.body)
#         username = reqBody['username']
#         password = reqBody['password']
#         try:

#             Account = CustomUser.objects.get(username=username)
#         except BaseException as e:
#             raise ValidationError({"400": f'{str(e)}'})

#         token = MyTokenObtainPairSerializer.get_token(Account)
#         token = str(token)
#         if check_password(password, Account.password):
#             raise ValidationError({"message": "Incorrect Login credentials"})

#         if Account:
#             if Account.is_active:
#                 login(request, Account)
#                 data["message"] = "user logged in"
#                 data["email"] = Account.email

#                 Res = {"data": data, "token": token}

#                 return Response(Res)

#             else:
#                 raise ValidationError({"400": f'Account not active'})

#         else:
#             raise ValidationError({"400": f'Account doesnt exist'})


class LoginUser(APIView):
    @swagger_auto_schema(request_body=UserModelLoginSerializer,
                         responses={400: "account doesn't exist",
                                    200: UserModelSerializer})
    
    def post(self, request,*args, **kwargs):
        data = {}
        print('==============',request.data)
        serializer = UserModelLoginSerializer(data=request.data)


        
        username = request.data['username']
        password = request.data['password']
        try:

            Account = CustomUser.objects.get(Q(username__iexact=username) | Q(email__iexact=username) | Q(phone__iexact=username))
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})

        token = AccessToken.for_user(Account)
        print("--------------",token)
        if not check_password(password, Account.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        if Account:
            if Account.is_active:
                login(request, Account, backend='accounts.backends.OtpBackend')
                data["message"] = "user logged in"
                data["email"] = Account.email

                Res = {"data": data, "token": str(token)}

                return Response(Res, status=200)

            else:
                raise ValidationError({"400": f'Account not active'})

        else:
            raise ValidationError({"400": f'Account doesnt exist'})
        
        

class VerifyPhoneNumber(APIView):
    @swagger_auto_schema(request_body=VerifyPhoneNumber,
                         responses={400: "The provided code did not match or has expired",
                                    201: "Phone number verified successfully"})
    
    def post(self, request,*args, **kwargs): 
        phone = request.data['phone']
        otp_code = request.data['otp_code']
        try:

            Account = CustomUser.objects.get(phone=phone)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})


        if Account:
            if not Account.is_verified:
                if Account.authenticate(otp_code):
                    Account.is_verified=True
                    Account.save()
                    return Response(dict(detail = "Phone number verified successfully"),status=201)
                else:
                    return Response(dict(detail='The provided code did not match or has expired'),status=400)
            else:
                return Response(dict(detail='PhoneNumber verified before'),status=400)

        else:
            raise ValidationError({"400": f'Account with this phone number doesnt exist'})
        
        

class GetCodeForVerify(APIView):
    @swagger_auto_schema(request_body=GetCodeVerifyPhoneNumber,
                         responses={400: "Account Verified before or doesn't exist",
                                    200: "Verification Code sent to your Number"})
    
    def post(self, request,*args, **kwargs): 
        phone = request.data['phone']
        try:

            Account = CustomUser.objects.get(phone=phone)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})


        if Account:
            if not Account.is_verified:
                time_otp = pyotp.TOTP(Account.key, interval=300)
                time_otp = time_otp.now()
                # send_sms(receptor=phone, token=time_otp)
                print('=========== otp : ', time_otp)
                return Response(dict(detail = "Verification Code sent to your Number"),status=200)
            else:
                return Response(dict(detail='PhoneNumber verified before'),status=400)

        else:
            raise ValidationError({"400": f'Account with this phone number doesnt exist'})
