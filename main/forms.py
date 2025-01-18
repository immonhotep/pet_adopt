from django import forms
from .models import UserProfile,Pet,PetCategory,ContactMessage,UserMessage,ReplyUserMessage
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm,PasswordResetForm

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from tinymce.widgets import TinyMCE



class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile
        fields = ('phone','bio','image')


 

    phone = forms.CharField(label="",required="True",widget=forms.TextInput(attrs={

        'placeholder':'Enter your phone number',
        'class':'form-control  bg-light my-1'
    }))


class Userform(forms.ModelForm):

    class Meta:

        model = User
        fields = ('username','first_name','last_name','email')


    username = forms.CharField(label="",widget=forms.TextInput(attrs={

        'placeholder':'Enter your Username',
        'class':'form-control  bg-light my-1'
    }))

    first_name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'placeholder':'Enter your first name',
        'class':'form-control  bg-light my-1'
    }))

    last_name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'placeholder':'Enter your last name',
        'class':'form-control  bg-light my-1'
    }))

    email = forms.CharField(label="",widget=forms.EmailInput(attrs={

        'placeholder':'Enter your email address',
        'class':'form-control bg-light my-1'
        
    }))



class UserLoginform(AuthenticationForm):

    def __init__(self,*args,**kwargs):
        super(UserLoginform,self).__init__(*args,**kwargs)

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder':'Enter username',
        'class':'form-control bg-light my-1'
        } ))


    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control bg-light my-1',
        'input':'data-mdb-input-init'

        }))
    
    captcha= ReCaptchaField(widget=ReCaptchaV2Checkbox(
       
    ))
    
class RegisterForm(UserCreationForm):


    email = forms.CharField(widget=forms.EmailInput(attrs={

        'placeholder':'Enter email',
        'class':'form-control bg-light my-1'

    }))

    username = forms.CharField(widget=forms.TextInput(attrs={

        'placeholder':'Enter Username',
        'class':'form-control bg-light my-1'

    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder':'Enter Password',
        'class':'form-control bg-light my-1'

    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder':'Repeat password ',
        'class':'form-control bg-light my-1'

    }))


    captcha= ReCaptchaField(widget=ReCaptchaV2Checkbox(
       
    ))

    usable_password = None

    class Meta:

        model = User

        fields=('username','email','password1','password2')




class ChangePasswordForm(PasswordChangeForm):

    old_password = forms.CharField(label="",widget=forms.PasswordInput(attrs={

        'placeholder':'Enter your current password',
        'class':'form-control bg-light my-1'

    }))

    new_password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={

        'placeholder':'Enter your new password',
        'class':'form-control bg-light my-1'

    }))

    new_password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={

        'placeholder':'Repeat your new password',
        'class':'form-control bg-light my-1'

    }))


class PetCategoryForm(forms.ModelForm):

    class Meta:

        model = PetCategory
        fields = ('name','description','image')


    name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'placeholder':'Enter Pet Category name',
        'class':'form-control  bg-light my-1'
    }))


   



class PetForm(forms.ModelForm):

    class Meta:

        model = Pet
        fields = ('name','description','image','category')


    name = forms.CharField(label="",widget=forms.TextInput(attrs={

        'placeholder':'Enter pet name',
        'class':'form-control  bg-light my-1'
    }))



    category = forms.ModelChoiceField(queryset=PetCategory.objects.all(),widget=forms.Select(attrs={

        'class':'form-select form-control fw-bolder'
    }))




class ResetPasswordForm(PasswordResetForm):

    def __init__(self,*args,**kwargs):
        super(ResetPasswordForm,self).__init__(*args,**kwargs)


    email = forms.CharField(label="",widget=forms.EmailInput(attrs={

        'placeholder':'Enter your email address',
        'class':'form-control my-3'

    }))

    captcha= ReCaptchaField(label="",widget=ReCaptchaV2Checkbox(
       
    ))
        


class ContactForm(forms.ModelForm):

    class Meta:

        model = ContactMessage
        fields = ('name','email','phone','title','message')

    name = forms.CharField(label="",required=True,max_length=200,widget=forms.TextInput(attrs={

        'placeholder':'Enter your name',
        'class':'form-control  bg-light my-1'

    }))


    email = forms.CharField(label="",required=True,max_length=100,widget=forms.EmailInput(attrs={

        'placeholder':'Enter your email address',
        'class':'form-control  bg-light my-1'

    }))

    phone = forms.CharField(label="",required=True,max_length=20,widget=forms.TextInput(attrs={

        'placeholder':'Enter your phone number',
        'class':'form-control  bg-light my-1'

    }))

    title = forms.CharField(label="",required=True,max_length=200,widget=forms.TextInput(attrs={

        'placeholder':'Enter title',
        'class':'form-control  bg-light my-1'

    }))


    message = forms.CharField(label="",required=True,max_length=3000,widget=forms.Textarea(attrs={

        'placeholder':'Enter message',
        'class':'form-control  bg-light my-1'

    }))



class MessageForm(forms.ModelForm):

    class Meta:

        model = UserMessage
        fields = ('title','body')


    title = forms.CharField(required="True",label="",widget=forms.TextInput(attrs={

        'placeholder' : 'Enter your message title',
        'class' : 'form-control form-control-sm bg-light my-1'

    }))






