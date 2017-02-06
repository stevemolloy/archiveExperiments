from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import registry

def index(request):
    latest_signal_list = registry.objects.order_by('first_registered')
    context = {'latest_signal_list': latest_signal_list,}
    return render(request, 'archiver/index.html', context)

def signalDetail(request, signal_id):
    return HttpResponse("Some details about signal #{}".format(signal_id))
