from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import registry
from .forms import ActiveSignalForm

def index(request):
    latest_signal_list = registry.objects.order_by('first_registered')
    form = ActiveSignalForm()
    context = {'latest_signal_list': latest_signal_list, 'form': form}
    return render(request, 'archiver/index.html', context)

def signalDetail(request, signal_id):
    return HttpResponse("Some details about signal #{}".format(signal_id))

def updateRegistry(request):
    return HttpResponse(request.POST.getlist('choices'))
