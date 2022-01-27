from gc import get_objects
from django.core.exceptions import PermissionDenied
from django.shortcuts import render




class IsSellerMixin(object):
    permission_denied_message = 'U are not seller, call to admin to give you permission'
    
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_seller:
            raise PermissionDenied(self.permission_denied_message)
        return super().dispatch(request, *args, **kwargs)