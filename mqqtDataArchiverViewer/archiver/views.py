from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import registry
from .forms import ActiveSignalForm, AddNewSignalForm
from django.utils import timezone

def index(request):
    latest_signal_list = registry.objects.order_by('first_registered')
    activeSigForm = ActiveSignalForm()
    addNewSigForm = AddNewSignalForm()
    context = {'latest_signal_list': latest_signal_list,
            'activeSigForm': activeSigForm,
            'addNewSigForm': addNewSigForm,
            }
    return render(request, 'archiver/index.html', context)

def signalDetail(request, signal_id):
    return HttpResponse("This should show a time-series plot of signal #{}".format(signal_id))

def updateRegistry(request):
    newRegistrySettings = [int(i) for i in request.POST.getlist('choices')]
    ts = timezone.now()
    for sig in registry.objects.all():
        if (sig.id in newRegistrySettings) and (not sig.archival_active):
            sig.archival_active = True
            sig.last_altered = ts
            sig.save()
        elif (not sig.id in newRegistrySettings) and sig.archival_active:
            sig.archival_active = False
            sig.last_altered = ts
            sig.save()
    return HttpResponseRedirect('/archiver')

def addNewSignal(request):
    return HttpResponse("Placeholder for addition of a new signal.")
