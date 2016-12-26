from django.shortcuts import render

from models import Entity


def index(request):
    context = {
        'entities': Entity.objects.all()
    }
    return render(request, 'sentiment/index.html', context)
