from django.shortcuts import render

def user_profile(request, username):
    print(username)
    return render(request, template_name='users/profile.html')
