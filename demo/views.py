'''
Created on 16.12.2014

@author: sdeiss
'''


from django.shortcuts import render


def index(request):
    return render(request, 'demo/home.html')
