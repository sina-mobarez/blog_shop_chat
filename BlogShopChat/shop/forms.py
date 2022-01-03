from django import forms
from django.forms import fields

from blog.models import Category
from .models import Shop, Type


class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'type')
        labels = {
			'name': "نام فروشگاه",
            'type': "نوع فروشگاه",
		}


class TypeForm(forms.ModelForm):
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput(attrs={'value': 't'}), label="")
    class Meta:
        model = Type
        fields = ('name',)
        labels = {
            'name': 'نوع فروشگاه'
        }



class CategoryForm(forms.ModelForm):
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput(attrs={'value': 'c'}), label="")
    class Meta:
        model = Category
        fields = ('name',)
        labels = {
            'name': 'نام دسته بندی'
        }       