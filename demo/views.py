'''
Created on 16.12.2014

@author: sdeiss
'''


from django.shortcuts import render
from django_auth_qr2auth import __version__


def index(request):
    return render(request, 'demo/home.html',
                  {'Q2AVersion': __version__})
