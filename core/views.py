from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            
                      
            form.save()
                       
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user.is_active=False     
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=user.password)

            return render(request, 'core/disable.html', {'user': user})

    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})


