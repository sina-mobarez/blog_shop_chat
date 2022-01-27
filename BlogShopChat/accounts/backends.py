from multiprocessing import AuthenticationError
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.contrib import messages



UserModel = get_user_model()



class UserNotVerified(Exception):
    """The Phone number is not verified yet"""




def user_is_verified(user):
    is_verified = getattr(user, 'is_verified', None)
    return is_verified or is_verified is None





class OtpBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username) | Q(phone__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username | Q(phone__iexact=username))).order_by('id').first()
            
        pwd = None
        if user.password is not None:
            pwd = user.check_password(password)
            if pwd:
                if user_is_verified(user):
                    return user
            else:
                
                try:   
                    if user.authenticate(password):
                        return user
                    else:
                        raise AuthenticationError('your OTP has been expired')
                except AuthenticationError:
                    return None
                
                



class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserModel.objects.get(Q(username__iexact=username) | Q(email__iexact=username) | Q(phone__iexact=username))
        except UserModel.DoesNotExist:
            UserModel().set_password(password)
            return
        except UserModel.MultipleObjectsReturned:
            user = UserModel.objects.filter(Q(username__iexact=username) | Q(email__iexact=username | Q(phone__iexact=username))).order_by('id').first()

        if user.check_password(password) and self.user_can_authenticate(user):
                if user_is_verified(user):
                    return user
                
                else:
                    
                    request.session['phone'] = user.phone
                    request.session.set_expiry(300)
                    messages.error(request, 'you should verify to login')
                    
                    raise UserNotVerified('')
                
                

    
    