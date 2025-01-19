from django.shortcuts import render,redirect
from .models import UserProfile,Pet,PetCategory,ContactMessage,ContactMessageAnswer,Adoptation,UserMessage,ReplyUserMessage
from django.contrib.auth.models import User
from .forms import ProfileForm,Userform,UserLoginform,RegisterForm,PetCategoryForm,PetForm,ResetPasswordForm,ContactForm,MessageForm
from django.shortcuts import get_object_or_404
from django .views import View
from django .views.generic import ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .mixins import SuperUserRequiredMixin,CustomLoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils.text import slugify

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
#prevent error related force_text not found
from django.utils.encoding import force_str as force_text




class ListCategory(ListView):

    queryset = PetCategory.objects.all()
    template_name = 'main/home.html'
    context_object_name = 'categories'
    ordering=['-name']
    paginate_by = 6


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        random_pet = Pet.objects.all().order_by('?').first()
        context['random_pet']  = random_pet
        return context

   

class UpdateProfile(CustomLoginRequiredMixin,View):

    def get(self,request):

        user = get_object_or_404(User,pk=self.request.user.pk)
        profile = get_object_or_404(UserProfile,pk=self.request.user.userprofile.pk)

        user_form = Userform(instance=user)
        profile_form = ProfileForm(instance=profile)

        context={'user_form':user_form,'profile_form':profile_form}
        return render(self.request,'main/update_profile.html',context)


    def post(self,request):

        user = get_object_or_404(User,pk=self.request.user.pk)
        profile = get_object_or_404(UserProfile,pk=self.request.user.userprofile.pk)

        user_form = Userform(request.POST,instance=user)
        profile_form = ProfileForm(request.POST,request.FILES,instance=profile)

        password = self.request.POST.get('password')

        if not self.request.user.check_password(password):
            messages.error(self.request,'You entered invalid password')
            
        else:

            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(self.request,'You modified your user data successfully')
                return redirect('home')

            else:
                messages.error(self.request,'Something went wrong')
                
        return redirect('update_profile')
        
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"    



class DeleteUser(UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = User
    template_name = 'main/confirm.html'
    success_message = "%(username)s was deleted successfully"

    def get_success_message(self, cleaned_data):

        return self.success_message % dict(
            cleaned_data,
            username=self.object.username
        )

    def get_success_url(self):
        return  reverse_lazy('home')
    

    def test_func(self):

        object = self.get_object()

        if object.pk == self.request.user.pk or self.request.user.is_superuser:
            return True
        else:
            return False
        

    def handle_no_permission(self):

        return redirect('forbidden')


            

class MyLoginView(SuccessMessageMixin,LoginView):

    template_name = 'main/login.html'
    form_class = UserLoginform
    redirect_authenticated_user = True


    def get_success_message(self, cleaned_data):

        return(f'{self.request.user} has been logged in')
    

    def form_invalid(self,form):

        for key, error in list(form.errors.items()):

                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(self.request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(self.request, error) 

        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):

        return reverse('home')


class MyLogoutview(LogoutView):
  
    def get_success_url(self):

        return reverse_lazy('home')



class MyRegistrationview(SuccessMessageMixin,CreateView):

    template_name = 'main/register.html'
    form_class = RegisterForm
    

    def form_valid(self, form):  
        user = form.save(commit=False)
        user.is_active = False
        user.save()


        current_site = get_current_site(self.request)

        subject = 'Activate Your Account'
        message = render_to_string('account_activation_email.html', {
            'user':user,
            'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token':account_activation_token.make_token(user),
        })
        try:
            user.email_user(subject=subject, message=message)

            messages.success(self.request,'To finish registration please check your mailbox including spam folder and follow instructions')
        except:
            messages.error(self.request,'Mail Server Connection problem, please turn to website admin')

        return super().form_valid(form)
    


     
    def form_invalid(self, form):
        
        for key, error in list(form.errors.items()):

                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(self.request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(self.request, error)
        

        return super().form_invalid(form)
    
    def get_success_url(self):
        return reverse_lazy('login')
    


def account_activation(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        
    except():
        pass

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,'Your registration finished now please login')
        return redirect('login')

    else:
        return render(request, 'activation_invalid.html')



class ChangePassword(CustomLoginRequiredMixin,SuccessMessageMixin,PasswordChangeView):

    template_name = 'main/passwordchange.html'

    def get_success_message(self, cleaned_data):

        return('Your password has been changed successfully')
    
    def get_success_url(self):
        return reverse_lazy('update_profile')
    

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_name']  = 'change_password'
        return context
    
    def form_invalid(self, form):

        for error in list(form.errors.values()):
            messages.error(self.request,error)
            return redirect('change_password')
        
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):

    form_class = ResetPasswordForm
    template_name = 'password_reset.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'

    success_message = "We sent email for you with instructions to change your password." \
                      " if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    
    success_url = reverse_lazy('home')


    def form_invalid(self, form):
        
        for key, error in list(form.errors.items()):

                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(self.request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(self.request, error)
        return redirect('password_reset')

  

class AddPetCategory(SuperUserRequiredMixin,SuccessMessageMixin,CreateView):


    model = PetCategory
    template_name = 'main/forms.html'
    form_class = PetCategoryForm
    success_message = "%(name)s was created successfully"

    def form_valid(self, form):  
            form.instance.donater = self.request.user
            return super().form_valid(form)
     
    def form_invalid(self, form):
        for error in list(form.errors.values()):
            messages.error(self.request,error)
            return super().form_invalid(form)
        
    def get_success_message(self, cleaned_data):
         
         return self.success_message % dict(
            cleaned_data,
            name=self.object.name
        )
    
    
    def get_success_url(self):
        return reverse_lazy('home')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_name']  = 'add_category'
        return context
    

    def handle_no_permission(self):       
        return redirect('forbidden')
        



class UpdateCategory(SuperUserRequiredMixin,SuccessMessageMixin,UpdateView):

    model = PetCategory
    template_name = 'main/forms.html'
    form_class = PetCategoryForm
    success_message = "%(name)s was updated successfully"

    def get_success_message(self, cleaned_data):

        
    
        return self.success_message % dict(
            cleaned_data,
           
        )

    def get_success_url(self):
        return  reverse_lazy('home')
      

    def get_context_data(self, *args, **kwargs):

               
        context = super().get_context_data(*args, **kwargs)       
        context['page_name']  = 'update_category'
        return context
        

    def handle_no_permission(self):

        return redirect('forbidden')

   


class DeleteCategory(SuperUserRequiredMixin,SuccessMessageMixin,DeleteView):

    model = PetCategory
    template_name = 'main/confirm.html'
    success_message = "%(name)s was deleted successfully"

    def get_success_message(self, cleaned_data):

        return self.success_message % dict(
            cleaned_data,
            name=self.object.name
        )

    def get_success_url(self):
        return  reverse_lazy('home')
    

    def handle_no_permission(self):

        return redirect('forbidden')



class ViewCategoryDetail(CustomLoginRequiredMixin,DetailView):

    model = PetCategory
    template_name="main/category_detail.html"

    def get_context_data(self,*args, **kwargs):
        context = super(ViewCategoryDetail,self).get_context_data(*args,**kwargs)

        pet_category = get_object_or_404(PetCategory,slug=self.kwargs['slug'])
        pets = Pet.objects.filter(category=pet_category).order_by('-name')
        

        p = Paginator(pets,6)
        page = self.request.GET.get('page')

        try:
            pets = p.page(page)
        except PageNotAnInteger:
            pets = p.page(1)
        except EmptyPage:
            pets = p.page(p.num_pages)




        context['pet_category'] = pet_category
        context['pets'] = pets


        return context
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ViewPetDetail(CustomLoginRequiredMixin,DetailView):

    model = Pet
    template_name="main/pet_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ViewPetDetail,self).get_context_data(*args,**kwargs)

        pet = get_object_or_404(Pet,slug=self.kwargs['slug'])

        try:
            adoptations = Adoptation.objects.get(pet=pet)
        except:
            adoptations = {}



        context['adoptations'] = adoptations
        context['pet'] = pet

        
        return context
    
    login_url = "/login/"
    redirect_field_name = "redirect_to"

 


class AddPet(CustomLoginRequiredMixin,SuccessMessageMixin,CreateView):


    model = Pet
    template_name = 'main/forms.html'
    form_class = PetForm
    success_message = "%(name)s was created successfully"

    def form_valid(self, form):  
            form.instance.donater = self.request.user
            return super().form_valid(form)
     
    def form_invalid(self, form):
        for error in list(form.errors.values()):
            messages.error(self.request,error)
            return super().form_invalid(form)
        
    def get_success_message(self, cleaned_data):
         
         return self.success_message % dict(
            cleaned_data,
            name=self.object.name
        )
    
    
    def get_success_url(self):
        return reverse_lazy('home')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_name']  = 'add_pet'
        return context
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"





class UpdatePet(UserPassesTestMixin,SuccessMessageMixin,UpdateView):

    model = Pet
    template_name = 'main/forms.html'
    form_class = PetForm

    def get_success_url(self,**kwargs):

        return reverse('category_details',kwargs={'slug':self.object.category.slug})
        

    def form_valid(self, form):
        
        next = self.request.GET.get('next',None)

        data=form.save()
        messages.success(self.request,f'{data.name} has been updated')
        
        if next is not None and next != "/search":
            return HttpResponseRedirect(redirect_to=next)
        
        elif next == "/search":

            page = self.request.session.get('searchpage',"")

            return HttpResponseRedirect(redirect_to=f'/search?petsearch={page}')

        else:
            return HttpResponseRedirect(self.get_success_url())
        
                

    def test_func(self):

        object = self.get_object()

        if object.donater == self.request.user or self.request.user.is_superuser:
            return True
        else:
            return False
        

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_name']  = 'update_pet'
        return context
        

    def handle_no_permission(self):

        return redirect('forbidden')



class DeletePet(UserPassesTestMixin,SuccessMessageMixin,DeleteView):

    model = Pet
    template_name = 'main/confirm.html'
   

    def get_success_url(self,**kwargs):

        return reverse_lazy('category_details',kwargs={'slug':self.object.category.slug})  


    def form_valid(self, form):

        obj = self.get_object()
        super(DeletePet, self).delete(self.request)
        next = self.request.GET.get('next',None)

        messages.success(self.request,f'{obj.name} has been deleted')
        
        if next is not None and next != "/search":
            return HttpResponseRedirect(redirect_to=next)
        
        elif next == "/search":

            page = self.request.session.get('searchpage',"")

            return HttpResponseRedirect(redirect_to=f'/search?petsearch={page}')

            
        else:
            return HttpResponseRedirect(self.get_success_url())
    
       

    def test_func(self):

        object = self.get_object()

        if object.donater == self.request.user or self.request.user.is_superuser:
            return True
        else:
            return False
        

    def handle_no_permission(self):

        return redirect('forbidden')

    login_url = "/login/"
    redirect_field_name = "redirect_to"




class ListUsers(CustomLoginRequiredMixin,ListView):

    queryset = User.objects.all()
    template_name = 'main/user_list.html'
    context_object_name = 'users'
    ordering=['-username']
    paginate_by = 8


    login_url = "/login/"
    redirect_field_name = "redirect_to"




class VievUserDetail(CustomLoginRequiredMixin,DetailView):

    model = User
    template_name="main/user_profile.html"


    def get(self,*args, **kwargs):

        user = get_object_or_404(User,pk=self.kwargs['pk'])

        user_messages = UserMessage.objects.filter(Q(receiver=self.request.user,sender=user)|Q(sender=self.request.user,receiver=user)).order_by('-date')

        p = Paginator(user_messages,6)
        page = self.request.GET.get('page')

        try:
            user_messages = p.page(page)
        except PageNotAnInteger:
            user_messages = p.page(1)
        except EmptyPage:
            user_messages = p.page(p.num_pages)


        if self.request.user.pk != user.pk:
            form = MessageForm()
            context = {'form':form,'user':user,'user_messages':user_messages}
        else:
            context={'user':user,'user_messages':user_messages}

        return render(self.request,'main/user_profile.html',context)
    

    def post(self,*args, **kwargs):

        receiver = get_object_or_404(User,pk=self.kwargs['pk'])
        form = MessageForm(self.request.POST)

        if self.request.user != receiver:
            if form.is_valid():
                data = form.save(commit=False)
                data.sender = self.request.user 
                data.receiver = receiver
                data.save()
                messages.success(self.request,f' You successfully sent message to {receiver}')
            else:
                for error in list(form.errors.values()):
                    messages.error(self.request,error)

        return redirect('user_detail',receiver.pk)



    
    login_url = "/login/"
    redirect_field_name = "redirect_to"





class ListUserPets(CustomLoginRequiredMixin,View):

    def get(self,request,pk):

        user = get_object_or_404(User,pk=pk)
        mypets = Pet.objects.filter(donater=user).order_by('-name')


        p = Paginator(mypets,6)
        page = self.request.GET.get('page')

        try:
            mypets = p.page(page)
        except PageNotAnInteger:
            mypets = p.page(1)
        except EmptyPage:
            mypets = p.page(p.num_pages)



        context={'mypets':mypets,'user':user,}
        return render(self.request,'main/mypets.html',context)
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"





class SearchForPet(CustomLoginRequiredMixin,View):

    def get(self,request):

        search = request.GET.get('petsearch',"")
        request.session['searchpage'] = search

        if search :
            mypets = Pet.objects.filter(Q(name__icontains=search)|Q(description__icontains=search)).order_by('-name')

            if not mypets:

                messages.info(self.request,f'{search} not found')             
            else:
                messages.info(self.request,f' results found for {search}')
        else:
            return redirect(request.META.get('HTTP_REFERER'))
        

        p = Paginator(mypets,6)
        page = self.request.GET.get('page')

        try:
            mypets = p.page(page)
        except PageNotAnInteger:
            mypets = p.page(1)
        except EmptyPage:
            mypets = p.page(p.num_pages)


        context={'mypets':mypets,'search':search}
        return render(self.request,'main/mypets.html',context)
    


class SendContactMessage(SuccessMessageMixin,CreateView):

    model = ContactMessage
    template_name = 'main/forms.html'
    form_class = ContactForm
    success_message = "Your message has been sent to the staff, we will answer soon."


    def form_invalid(self, form):
        for error in list(form.errors.values()):
            messages.error(self.request,error)
            return super().form_invalid(form)
        
    def get_success_message(self, cleaned_data):
         
         return self.success_message
      
    def get_success_url(self):
        return reverse_lazy('home')


    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['page_name']  = 'send_message'
        return context


class ListContactMessage(SuperUserRequiredMixin,ListView):

    queryset = ContactMessage.objects.all()
    template_name = 'main/contact_messages.html'
    context_object_name = 'messages'
    ordering=['-date']
    paginate_by = 8


    def handle_no_permission(self):       
        return redirect('forbidden')
    

class ViewMessageDetail(SuperUserRequiredMixin,DetailView):


    model = ContactMessage
    template_name="main/contact_messages.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ViewMessageDetail,self).get_context_data(*args,**kwargs)

        message = get_object_or_404(ContactMessage,pk=self.kwargs['pk'])

        context['message_detail'] = message
        return context
    

    def handle_no_permission(self):       
        return redirect('forbidden')
    


class SendAnswerMail(SuperUserRequiredMixin,View):


    def get(self,request,pk):

        contact_message = get_object_or_404(ContactMessage,pk=pk)
        context={'contact_message':contact_message}

        return render(self.request,'main/sendmail.html',context)
    

    def post(self,request,pk):

        contact_message = get_object_or_404(ContactMessage,pk=pk)

        address = contact_message.email
        title = contact_message.title

        subject = f'reply to: {title}'
        email_reply = request.POST.get('email-reply')
        email_from  = 'webmaster@localhost'
        cc = 'webmaster@localhost'
        

        email_body = """\
                            <html>
                            <head></head>
                            <body>
                            <hr> 
                            <h3>Hello %s  </h3>                         
                            <p>%s</p>
                            <hr>
                            </body>
                            <footer>
                             <p>Regards: Pet Adoptation platform Team </p>
                            </footer>
                            </html>
                            """ % (contact_message.name,email_reply)

        if email_reply:

            mail = EmailMessage(subject=subject,body=email_body,from_email=email_from,to=[address],cc=[cc])
            mail.content_subtype = "html"

            try:

                mail.send(fail_silently=False)
                messages.success(self.request,f'You sent reply message to {address}')

                contact_message.answered = True
                contact_message.save()
                ContactMessageAnswer.objects.create(person=self.request.user,message=contact_message,title=title,reply=email_reply)


            except Exception:
               messages.error(self.request,f'Error sending email: ... Please try again, or turn to the site admins')      


        return  redirect('home')


    def handle_no_permission(self):       
        return redirect('forbidden')
    


class list_replies(SuperUserRequiredMixin,DetailView):


    model = ContactMessage
    template_name="main/replies.html"

    def get_context_data(self, *args, **kwargs):
        context = super(list_replies,self).get_context_data(*args,**kwargs)

        message = get_object_or_404(ContactMessage,pk=self.kwargs['pk'])
        replies = ContactMessageAnswer.objects.filter(message=message)

      

        context['replies'] = replies
        return context
    

    def handle_no_permission(self):       
        return redirect('forbidden')
    


class SendAdoptationRequest(CustomLoginRequiredMixin,View):


    def post(self,request,pk):


        pet = get_object_or_404(Pet,pk=pk)
        adoptation_request, created = Adoptation.objects.get_or_create(pet=pet)

        if self.request.user in adoptation_request.adopter_list.all():

            adoptation_request.adopter_list.remove(self.request.user)
            messages.success(self.request,f'{self.request.user} removed from adoptation list')
        else:

            adoptation_request.adopter_list.add(self.request.user)
            messages.success(self.request,f'{self.request.user} added to adoptation list')

       
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"
    


class ListMyassignment(CustomLoginRequiredMixin,View):

    def get(self,request):

        myassigments = self.request.user.adopters.all()

        context = {'myassigments':myassigments}
        return render(self.request,'main/assignments.html',context)
    

    login_url = "/login/"
    redirect_field_name = "redirect_to"



class ListAdopters(CustomLoginRequiredMixin,View):

    def get(self,request,slug):

        pet = get_object_or_404(Pet, slug=slug)

        if pet.donater == self.request.user or request.user.is_superuser:

            try:
                adoptation =  Adoptation.objects.get(pet=pet) 
            except:
                adoptation={}

            

            context={'adoptation':adoptation}
            return render(self.request,'main/adopters.html',context)

        return redirect('forbidden')


    login_url = "/login/"
    redirect_field_name = "redirect_to"


class ListAllAdopters(CustomLoginRequiredMixin,View):

    def get(self,request,slug):

        pet = get_object_or_404(Pet, slug=slug)

        if pet.donater == self.request.user or request.user.is_superuser:

            try:
                adoptation =  Adoptation.objects.get(pet=pet) 
                users = adoptation.adopter_list.all().order_by('-username')
            except:
                users = {}
            

            paginator = Paginator(users, 8)  
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
          

            context={'page_obj':page_obj}
            return render(self.request,'main/user_list.html',context)

        return redirect('forbidden')


    login_url = "/login/"
    redirect_field_name = "redirect_to"
              




class SendreplyMessage(CustomLoginRequiredMixin,View):
    
    
    def post(self,request,pk,id):

        usermessage = get_object_or_404(UserMessage,pk=pk)
        receiver = get_object_or_404(User,id=id)

        reply_title = self.request.POST.get('title')
        reply_body = self.request.POST.get('body')

        if reply_title and reply_body:

            ReplyUserMessage.objects.create(reply_message=usermessage,reply_sender=self.request.user,reply_receiver=receiver,reply_title=reply_title,reply_body=reply_body)
            usermessage.replied = True
            usermessage.save()
            messages.success(self.request,f'You sent reply to: {receiver}')
        else:
            messages.error(self.request,'Error you try to send empty message')
          
        return redirect(request.META.get('HTTP_REFERER'))
    


    login_url = "/login/"
    redirect_field_name = "redirect_to"
              




class Forbidden_access(View):

    def get(self,request):
        return render(self.request,'main/forbidden.html')
