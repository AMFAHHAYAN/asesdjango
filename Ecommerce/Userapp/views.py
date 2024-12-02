from django.shortcuts import render,redirect
from django.views import View
from AdminApp.models import Product
from django.contrib.auth.models import User 
from django.contrib.auth import login,authenticate,logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import random
import uuid
import datetime
from pytz import timezone
from .models import Resetuid
from django.core.mail import send_mail
# Create your views here.

class Login(View):
    def get(self , request):
        return render(request, 'Userpages/login.html')
    def post(self, request):
        Username = request.POST.get('username')
        Password = request.POST.get('pass')

        if User.objects.filter(username = Username).exists():
            user = authenticate(username = Username,password=Password)
            if user != None:
                login(request, user)
                return redirect('dashboarduser')
            else:
                messages.error(request, f'Invalid Credentials')
                return render(request, 'Userpages/login.html')
        else:
            messages.error(request,f'User Not Found please Register')
            return render(request, 'Userpages/login.html')


class Signup(View):
    def get(self , request):
        return render(request, 'Userpages/signup.html')
    def post(self, request):
        Username= request.POST.get('username')
        Email= request.POST.get('email')
        Password= request.POST.get('pass')
        Confirmpas= request.POST.get('confirmpass')
        
        if Password != Confirmpas:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if len(Password) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, "signup.html")

        if not any(char.isupper() for char in Password):
            messages.error(request, "Password must contain at least one uppercase letter.")
            return render(request, "signup.html")

        if not any(char.islower() for char in Password):
            messages.error(request, "Password must contain at least one lowercase letter.")
            return render(request, "signup.html")

        if not any(char.isdigit() for char in Password):
            messages.error(request, "Password must contain at least one number.")
            return render(request, "signup.html")

        specialCharacters = "!@#$%^&*()-_=+[{]}|;:'\",<.>/?"
        if not any(char in specialCharacters for char in Password):
            messages.error(request, "Password must contain at least one special character.")
            return render(request, "signup.html")
        
        if User.objects.filter(email = Email).exists():
            messages.error(request, f'Email Taken')
            return render(request, 'Userpages/signup.html')
        elif User.objects.filter(username = Username).exists():
            messages.error(request, f'Username Taken')
            return render(request, 'Userpages/signup.html')
        else:
            User.objects.create_user(
                username= Username,
                email= Email,
                password= Password
            )
            messages.success(request, f'You have Succesfully Registered please Login')
            return redirect('loginuser')
    
class Forget(View):
    def get(self , request):
        return render(request, 'Userpages/forget.html')
    def post(self, request):
        Email = request.POST.get('email')
        if User.objects.filter(email = Email).exists():
            user = User.objects.get(email = Email)
            exp= datetime.datetime.now() + datetime.timedelta(minutes=2)
            print(exp)
            uuid_data= uuid.uuid1(random.randint (21387,21387089273))

            forget = Resetuid.objects.create(Uuid = uuid_data, user = user,expiry=exp)
            url = f'{settings.SITE_URL}/reset/{forget.Uuid}'
            if Email:
                subject="Password Reset Link"
                message =(
                    "To Reset Password click the link below \n"
                    f"Reset Your Password\n\t{url}"
                )
                try:
                    send_mail(subject,message,settings.EMAIL_HOST_USER,[Email])
                    # print(
                    #     f"\nSubject= {subject}\nmessage ={message}\nHOST= {settings.EMAIL_HOST_USER}\nmail ={Email}"
                    # )
                    messages.success(request, f'Mail sent successfully')
                    return redirect('loginuser')
                except Exception as e:
                    return render(request, 'Userpages/forget.html')
            else:
                return render(request, 'Userpages/forget.html')
        else:
            messages.error(request, f'invalid mail address')
            return render(request, 'Userpages/forget.html')
    
class Reset(View):
    def get(self,request,uuid):
        context ={'uuid':uuid}
        return render(request, 'Userpages/reset.html', context)
    
    def post(self,request,uuid):
        newpass = request.POST.get('newpass')
        confirmpass = request.POST.get('cpass')
        currentime = datetime.datetime.now()

        obj = Resetuid.objects.get(Uuid = uuid)
        user = obj.user
        current_time = currentime.astimezone(timezone('UTC'))

        if current_time < obj.expiry and newpass == confirmpass:
            user.set_password(newpass)
            user.save()
            Resetuid.objects.filter(Uuid = uuid).delete()
            messages.success(request, f'Password Reset Successfully')
            return redirect('loginuser')
        else:
            messages.error(request, f'Link Expired')
            return redirect('loginuser')
    
class Dashboard(View):
    @method_decorator(login_required)
    def get(self, request):
        products = Product.objects.all()
        context = {
           'products':products 
        }
        return render(request, 'Userpages/dashboard.html',context)

class Detail(View):
    @method_decorator(login_required)
    def get(self, request):
        return render (request, 'Userpages/detailproduct.html',)
    
class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')