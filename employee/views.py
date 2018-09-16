from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from employee.forms import UserForm
from django.shortcuts import render, redirect
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from ems.decorators import admin_hr_required, admin_only
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render_to_response



# Create your views here.
@login_required(login_url="/login/")
def employee_list(request):
    print(request.role)
    context = {}
    context['users'] = User.objects.all()
    context['title'] = 'Employees'
    return render(request, 'employee/index.html', context)

@login_required(login_url="/login/")
def employee_details(request, id=None):
    context ={}
    context['user'] = get_object_or_404(User, id=id)
    return render(request, 'employee/details.html', context)

@login_required(login_url="/login/")
@admin_only
def employee_add(request):
    context = {}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        context['user_form'] = user_form
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/add.html', context)
    else:
        user_form = UserForm()
        return render(request, 'employee/add.html', context)




@login_required(login_url="/login/")
def employee_edit(request, id=None):
    user=get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form =  UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            return render(request, 'employee/edit.html', {"user_form": user_form})
    else:
        user_form = UserForm(instance=user)
        return render(request, 'employee/edit.html', {"user_form":user_form})



@login_required(login_url="/login/")
def employee_delete(request, id=None):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('employee_list'))
    else:
        context = {}
        context['user'] = user
        return render(request, 'employee/delete.html', context)





def login_view(request):
    if request.method == 'POST':
        print("tisi")
        context = {}
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if request.GET.get('next', None):
                return  HttpResponseRedirect(request.GET['next'])
            print(login(request, user))
            return HttpResponseRedirect(reverse('employee_list'))
        else:
            context = {}
            print('no post')
            context["error"] = "Please provide valid credentials"
            return render(request, "auth/login.html", context)

    else:
        return render(request, "auth/login.html")


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)  # built in form of django
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            print("successful")
            return redirect("/success")
        else:
            form = UserCreationForm()
            args = {'form': form}
            return render(request, "login.html", args)

    return render(request, "login.html", {})

@login_required(login_url="/login/")
def logout_view(request):
    print("logging out")
    logout(request)
    print(logout(request))
    return HttpResponseRedirect(reverse('login'))


def csrf_failure(request,
                 reason=""):  # build a method to logout whenever we encounter a csrf_failure(check settings for further details)
    logout_view(request)

@login_required(login_url="/login/")
def success(request):
    # code to make sure it can't directly go to success page
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if login(request, user):
        return HttpResponseRedirect(reverse('login'))
    # actual code to make sure that main page is displayed
    context = {}
    context['user'] = request.user
    return render(request, "auth/success.html", {})



class ProfileUpdate(UpdateView):
    fields = ['designation', 'salary']
    template_name = 'auth/profile_update.html'
    success_url = reverse_lazy('my_profile')

    def get_object(self):
        return self.request.user.profile

class MyProfile(DetailView):
    template_name = 'auth/profile.html'

    def get_object(self):
        return self.request.user.profile


