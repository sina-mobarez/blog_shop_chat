from django import forms
from .models import Picture, Product, Shop, Type, Category





class ShopForm(forms.ModelForm):
    class Meta:
        model = Shop
        fields = ('name', 'type', 'description')
        labels = {
			'name': "نام فروشگاه",
            'type': "نوع فروشگاه",
            'description': "توضیحات فروشگاه"
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
        
    



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'category', 'description', 'quantity')  
        labels = {
            'name': 'نام محصول',
            'price': 'قیمت ',
            'category': 'دسته بندی ',
            'description': 'توضیحات',
            'quantity': 'تعداد موجودی'
        } 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'col': 30, 'row': 10}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),

        } 




class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ('name', 'image', 'default')
        labels = {
            'name': '',
            'image': '',
            'default': ''
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'اسم عکس '}),
        } 