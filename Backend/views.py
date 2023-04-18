from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages


def index(request):
    return render(request,'index.html')

# def signup(request):
#     if request.method == "POST":
#         form = Technician(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request, user)
#             messages.success(request, "Registration Successful")
#             return redirect("login")
#         messages.error(request,"Registration unsuccessful, Invalid arguments")
#     return None

# def login(request):
#     return None