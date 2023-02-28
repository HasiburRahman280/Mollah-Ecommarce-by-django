from django.shortcuts import render,redirect
from .forms import CreateuserForm,UserProfileForm,ProfilePictureForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from .models import Profile,ProfilePicture
# Create your views here.

def auth_signup(request):
    form = CreateuserForm()
    if request.method == 'POST':
        form = CreateuserForm(data = request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context ={
        'form':form
    }

    return render(request,'signup.html',context)

def auth_login(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect('/')

    context ={
        'form':form
    }
    return render(request,'login.html',context)


def auth_logout(request):
    logout(request)
    return redirect('login')

def user_profile_view(request):
    user_pro = Profile.objects.get(user=request.user)


    context = {
        'user_pro':user_pro,
    }
    return render(request,'AppAcccount/profile_view.html',context)

def user_profile_edit(request):
    user_pro = Profile.objects.get(user=request.user)
    form = UserProfileForm(instance=user_pro)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,instance=user_pro)
        if form.is_valid():
            form.save()
            return redirect('user_profile_view')
        else:
            print('error')

    context = {
        'form':form
    }
    return render(request,'AppAcccount/profile_edit.html',context)

def profile_picture(request):
    profile_pic_form = ProfilePictureForm()
    if request.method == 'POST':
        profile_pic_form = ProfilePictureForm(request.POST,request.FILES)
        if profile_pic_form.is_valid():
            user_profile_obj = profile_pic_form.save(commit=False)
            user_profile_obj.user = request.user
            user_profile_obj.save()
            return redirect('user_profile_view')
        else:
            print('error')

    context ={
        'profile_pic_form':profile_pic_form
    }
    return render(request,'AppAcccount/add_profile_pic.html',context)


def update_Profile_Pic(request):
    update_profile_pic_form = ProfilePictureForm(instance=request.user.pro_pics)
    if request.method == 'POST':
        update_profile_pic_form =  ProfilePictureForm(request.POST,request.FILES, instance=request.user.pro_pics)
        if update_profile_pic_form.is_valid():
            update_profile_pic_form.save()
            return redirect('user_profile_view')
    context ={
        'update_profile_pic_form':update_profile_pic_form,
    }
    return render(request,'AppAcccount/update_profile_pic.html',context)

