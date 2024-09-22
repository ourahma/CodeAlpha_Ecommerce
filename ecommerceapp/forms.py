from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,UserChangeForm,SetPasswordForm
from django import forms
from .models import *



class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model=User
        fields=('new_password1','new_password2')
    
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.fields['new_password1'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['new_password1'].label = ''
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['new_password2'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['new_password2'].label = ''
        self.fields['new_password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'
        
        
        
        
        
        
class UpdateUserForm(UserChangeForm):
    password = None  # Hide password field

    email = forms.EmailField(label="", widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',  
        'placeholder': 'Email Address',
        'disabled':True
    }), required=False)
    
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',  
        'placeholder': 'First Name'
    }), required=False)
    
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control mb-3',  
        'placeholder': 'Last Name'
    }), required=False)
    

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user',None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['username'].initial = user.username
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name
            self.fields['email'].initial = user.email
            
            
        self.fields['username'].widget.attrs.update({
            'class': 'form-control mb-3',  
            'placeholder': 'User Name',
            
        })
        self.fields['first_name'].label = 'First Name'
        self.fields['last_name'].label = 'Last Name'
        self.fields['email'].label = 'Email'
        self.fields['username'].label = 'User Name'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

    
    
    
    
    
    
    
    
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control mb-3'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken. Please choose another one.')
        return username


class UserInfoForm(forms.ModelForm):
    password=None
    
    phone_number=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'Phone'}),required=False)
    city=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'City'}),required=False)
    postal_code=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'Zip Code'}),required=False)
    country=forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control mb-3','placeholder':'Country'}),required=False)
    
    class Meta:
        model = Customer
        fields= ('phone_number','address','city','country','postal_code')
        
        
    def __init__(self, *args, **kwargs):
        user=kwargs.pop('user',None)
        super(UserInfoForm, self).__init__(*args, **kwargs)
        
        if user:
            self.fields['phone_number'].initial = user.customer.phone_number
            self.fields['address'].initial = user.customer.address
            self.fields['city'].initial = user.customer.city
            self.fields['postal_code'].initial = user.customer.postal_code
            self.fields['country'].initial = user.customer.country
        
        self.fields['address'].widget.attrs.update({
            'class': 'form-control mb-3',  
            'placeholder': 'User Name',
            
        })
        
        self.fields['phone_number'].label = 'Phone number'
        self.fields['address'].label = 'Address'
        self.fields['city'].label = 'City'
        self.fields['postal_code'].label = 'Postal code'
        self.fields['country'].label = 'Country'