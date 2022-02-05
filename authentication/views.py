from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib import messages
from django.urls import reverse
from authentication.models import User, Profile as ProfileModel
from django.core.mail import EmailMessage
from django.views import View
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from authentication.utils import token_generator
from core.models import ShippingAddress



class Register(View):
    def get(self,request):
        return render(request, "authentication/register.html")

    def post(self,request):
        full_name = request.POST.get('fullname')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            if(len(password1) >= 7):
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already taken')
                    return render(request, "authentication/register.html")
                else:
                    user = User.objects.create_user(email=email, name=full_name)
                    user.set_password(password1)
                    profile = Profile(user=user, full_name=full_name)

                    uid64 = urlsafe_base64_encode(force_bytes(user.pk))  # -- takes the user id ecode or http reqeust
                    domain = get_current_site(request).domain  # - takes the current of the site and it domain eg: ecom.com
                    link = reverse('verify-email', kwargs={'uid64': uid64, 'token': token_generator._make_hash_value(user)})  # - send back the token and id of the user for store
                    activate_url = 'http://'+domain+link   # - the final link contains 
                    email_subject = "Activate Your email account"
                    email_body = 'Hi '+user.name+', Please use this link to verify your account\n'+activate_url # - messsage given to the registered user

                    emailsender = EmailMessage( # -sends information 
                        email_subject, email_body, 'noreply@ecom.com', to=[email]
                    )
                    
                    # emailsender.send(fail_silently=False)
                    user.save()
                    profile.save()
                    messages.success(request, 'Account Successfully Created')
                    return render(request, "authentication/register.html")
            else:
                messages.error(request, 'Password should be more than 7 charaters')
                return render(request, "authentication/register.html")
        else:
            messages.error(request, 'Password do not match')
            return render(request, "authentication/register.html")



class VerifyEmail(View):
    def get(self,request, uid64, token):
        try:
            id = force_text(urlsafe_base64_decode(uid64))
            user = User.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                return redirect('login'+'?messages'+'user already activated')
            if user.is_verify:
                return redirect('login-web')
            user.is_verify = True
            user.save()
            messages.success(request, "Account is successully activated")
        except:
            pass
        return redirect('login-web')



class Login(View):
    def get(self,request):
        return render(request, "authentication/login.html")

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user != None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.info(request, 'User Not Registered')
            return render(request, "authentication/login.html")
        
        

def logout(request):
    auth.logout(request)
    return redirect("/")



class Profile(View):
    def get(self, request):
        profile = ProfileModel.objects.get(user=request.user.id)
        context = {
            'profile': profile,
        }
        return render(request, 'authentication/profile.html', context)
    def post(self, request):
        userId = request.user.id
        full_name = request.POST.get('name')
        number = request.POST.get('number')
        gender = request.POST.get('gender')
        dob = request.POST.get('dob')
        try:
            profile = ProfileModel(user=userId, full_name=full_name, number=number, gender=gender, dob=dob)
            user = User(id=userId, name=full_name)
            messages.success(request, 'Profile Updated Successfully')
            user.save()
            profile.save()
            return render(request, 'authentication/profile.html')
        except:
            messages.success(request, 'Error updating Profile. Check again')
            return render(request, 'authentication/profile.html')
