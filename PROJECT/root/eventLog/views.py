from django.http.response import HttpResponse
from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'home.html',{'name':'fuck off'})

def add(request):
    return render(request,'result.html',{'result':int(request.POST['num1'])+int(request.POST['num2'])})