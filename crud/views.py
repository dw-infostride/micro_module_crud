from django.shortcuts import render, redirect
from django.http import HttpResponse
# from django.contrib.auth.models import User
from crud.models import User, profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from m3s import settings 
import requests
import json
# Create your views here.


# if user is not logged in --> returns true
def not_logged_in(user):
    return not user.is_authenticated


# ________________________________________________________________ start page ________________________________________________________

# user goes through a test before letting the user hit sign_up view
# @user_passes_test(not_logged_in, login_url='/dashboard')



def start_page(request):  # view for start page
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return render(request, 'index.html')
# __________________________________________________________________sign up  ______________________________________________________


# user goes through a test before letting the user hit sign_up view
# @user_passes_test(not_logged_in, login_url='/dashboard')
# if user is logged out , user can sign_up
def sign_up(request):
    
    
    
    if  request.user.is_authenticated:    # inbuilt method to not let user go to private  pages 
        return redirect('/dashboard')
    
    else:

        my_user = User
        if request.method == "POST":
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            password2 = request.POST.get('password2')
            country_code = request.POST.get('country_code')
            phone_number = request.POST.get('phone_number')

            if password != password2:
                # if passwords dont match, user cannot sign up
                # return HttpResponse("Passwords Do Not Match")
                # messages.info(request,"passwords do not match")
                messages.add_message(request, messages.ERROR, 'Passwords Do Not Match', extra_tags='bg-danger text-white')
                return render(request, 'signup.html')

            if User.objects.filter(username=username).exists():
                # username is unique
                # return HttpResponse("User with that username already exists, Please enter a different Username")
                #   messages.info(request,"User with that username already exists, Please enter a different Username")
                messages.add_message(request, messages.ERROR, 'User with that username already exists, Please enter a different Username', extra_tags='bg-danger text-white')
                return render(request, 'signup.html')

            if User.objects.filter(email=email).exists():
                # email is unique
                # return HttpResponse("User witht that email already exists, Please enter a new email")
                # messages.info(request,"User witht that email already exists, Please enter a new email")
                messages.add_message(request, messages.ERROR, 'User with that email already exists, Please enter a different Email', extra_tags='bg-danger text-white')

                return render(request, 'signup.html')
                

            else:
                my_user = User.objects.create_user(first_name=first_name,  # create a user
                                                last_name=last_name,
                                                username=username,
                                                email=email,
                                                password=password,
                                                country_code=country_code,
                                                phone_number=phone_number)
                my_user.save()  # to save a  user in database
                messages.add_message(request, messages.SUCCESS, 'Logged Out Successfuly', extra_tags='bg-success text-white')

                return redirect('/sign-in')

        return render(request, 'signup.html')
    
    

        


# __________________________________________________________________sign in  ______________________________________________________
# @user_passes_test(not_logged_in, login_url='/dashboard')
def sign_in(request):
    
    if  request.user.is_authenticated:
        return redirect('/dashboard')
    
    else:

        if request.method == "POST":
            email = request.POST.get("email")
            password = request.POST.get('password')
            clientKey = request.POST['g-recaptcha-response']
            SecretKey = settings.recaptcha_secret_key
            captchaData = {
                'secret': SecretKey,
                'response': clientKey
                }
            # print(captchaData)
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = captchaData)
            response = json.loads(r.text)
            verify = response['success']
            # print(verify)

            User = authenticate(request, email=email, password=password)

            if User is not None and verify is True:
                login(request, User)
                messages.add_message(request, messages.SUCCESS, 'Logged In Successfuly', extra_tags='bg-success text-white')
                return redirect('dashboard')

            elif verify is False:
                messages.add_message(request, messages.ERROR, 'Recaptcha Failed', extra_tags='bg-danger text-white')
            else:
                messages.add_message(request, messages.ERROR, 'Invalid Credentials', extra_tags='bg-danger text-white') # red colour 
                # messages.error(request,"Invalid Credentials")
                return render(request, 'signin.html')
                # return HttpResponse("Invalid Credentials")


        return render(request, 'signin.html')


# __________________________________________________________________view for dashboard url ________________________________________________


# log in is required to go to dashboard, else will be directed towards sign_in

# @login_required(login_url='sign_in')


@login_required(login_url='sign_in')
def dashboard(request):    
    user = request.user
    profile = user.profile
    return render(request, 'dashboard.html',{'user' : user, 'profile' : user.profile})



# _________________________________________________________________view for logout url_____________________________________________________


def log_out(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logged Out Successfuly', extra_tags='bg-success text-white')
    return redirect('/')

# _________________________________________________________________view to edit profile __________________________________________________


@login_required(login_url='sign_in')
def edit_profile(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        profile_pic = request.FILES.get('my_file')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        country_code = request.POST.get('country_code')
        phone_number = request.POST.get('phone_number')

        if username != user.username and User.objects.filter(username=username).exists():
            # current user 
            # return HttpResponse("User with that username already exists, Please enter a different Username")
            messages.add_message(request, messages.ERROR, 'User with that username already exists, Please enter a different Username', extra_tags='bg-danger text-white')
            return render(request, 'edit_profile.html')

        else:     
            
            
            profile.profile_picture = profile_pic
            profile.save()
                
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.country_code = country_code
            user.phone_number = phone_number
            user.profile_pic = profile_pic
            user.save()
            return redirect('dashboard')

    return render(request, 'edit_profile.html')


# __________________________________________________________ change password _______________________________________________________

def change_password(request):
    if request.user.is_authenticated:
        
        user = request.user              # this gets the user and all its details, no need to get any detail after this 
        if request.method == "POST":
            email = user.email          # gets user email 
            old_password = request.POST.get("old_password")
            new_password = request.POST.get("new_password")
            confirm_new_password = request.POST.get("confirm_new_password")
            
            user = authenticate(request, email=email, password = old_password) # authenticates the user if old password entered is correct or not
            print(user)
            
            
            if user is not None:                          #   i.e. if user exists 
                
                if old_password == new_password:
                    # return HttpResponse("Your New Password And Old Password Cannot Be Same")
                    messages.add_message(request, messages.ERROR, 'Your New Password And Old Password Cannot Be Same', extra_tags='bg-danger text-white')
                    return render(request, 'change_password.html')

                elif new_password != confirm_new_password:
                    # return HttpResponse("Passwords Do Not Match")
                    messages.add_message(request, messages.ERROR, 'Passwords Do Not Match', extra_tags='bg-danger text-white')
                    return render(request, 'change_password.html')

                else:
                    user.set_password(new_password)
                    user.save()
                    messages.add_message(request, messages.SUCCESS, 'Password Changed Successfuly', extra_tags='bg-success text-white')                    
                    return redirect("/dashboard")
            else:
                messages.add_message(request, messages.ERROR, 'Enter Correct Details', extra_tags='bg-danger text-white')
                return render(request, 'change_password.html')
                    

        return render(request, 'change_password.html')
    
    else:
        return redirect('/sign-in')
