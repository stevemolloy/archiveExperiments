from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
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
    newRegistrySettings = [int(i) for i in request.POST.getlist('choices')]
    for sig in registry.objects.all():
        if sig.id in newRegistrySettings and not sig.archival_active:
            sig.archival_active = True
            sig.save()
        elif not sig.id in newRegistrySettings and sig.archival_active:
            sig.archival_active = False
            sig.save()
    return HttpResponseRedirect('/archiver')
