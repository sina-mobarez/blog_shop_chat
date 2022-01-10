from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserCreationForm, UserChangeForm, PasswordChangeForm
from django.forms import fields

from accounts.models import CustomUser
from .models import *

class CategoryForm(forms.ModelForm):
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput(attrs={'value': 'c'}), label="")

    class Meta:
        model = Category
        fields = ('name',)
        labels = {
			'name': "نام دسته بندی",
		}


class TagForm(forms.ModelForm):
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput(attrs={'value': 't'}), label="")

    class Meta:
        model = Tag
        fields = ('name',)
        labels = {
			'name': "نام تگ",
		}



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'bodytext', 'pic', 'category', 'tag', 'status')
        labels = {
			'title': "عنوان",
            'bodytext': "متن",
			'pic': "عکس",
			'category': "دسته بندی",
			'tag': "تگ",
			'status': "وضعیت",
		}

        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, label='ایمیل', error_messages={'exists': 'This email already exists!'})
    password1 = forms.CharField(
        label="رمز عبور",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="تایید رمز عبور",
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        labels = {
			'username': "نام کاربری",
            'email': "ایمیل",
			'password1': "رمز عبور",
			'password2': "تایید رمز عبور",
		}


    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']


def should_be_empty(value):
    if value:
        raise forms.ValidationError('Field is not empty')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=80, label='نام و نام خانوادگی')
    subject = forms.CharField(max_length=80, label='عنوان')
    message = forms.CharField(widget=forms.Textarea, label='پیام')
    email = forms.EmailField(label='ایمیل')
    forcefield = forms.CharField(
        required=False, widget=forms.HiddenInput, label="Leave empty", validators=[should_be_empty])


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(max_length= 100 , label='رمز عبور قبلی', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(max_length= 100 , label='رمز عبور جدید', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(max_length= 100 , label='تایید رمز عبور جدید', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')


class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label='رمز ورود',
        help_text=(
            '.متاسفانه قادر به نمایش رمز عبور شما نیستیم'
            'ولی برای تغییر ان میتواید از.'
            '<a href="{}">این لینک</a>.'
            'استفاده کنید'
            
        ),
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'is_active', 'email', 'phone')
        labels = {
			'username': "نام کاربری",
			'first_name': "نام",
			'last_name': "نام خانوادگی",
			'is_active': "کاربر فعال",
			'email': "ایمیل",
            'phone': 'شماره مبایل'
		}
