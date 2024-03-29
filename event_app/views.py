# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Event
from .forms import EventForm
from django.http import JsonResponse

def event_calendar(request):
    events = Event.objects.all()
    return render(request, 'event_app/event_calendar.html', {'events': events})

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_app:event_calendar')
    else:
        form = EventForm()
    return render(request, 'event_app/add_event.html', {'form': form})

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_app/event_detail.html', {'event': event})

def api_events(request):
    events = Event.objects.all()
    event_list = []
    for event in events:
        event_list.append({
            'id' : event.event_id,
            'title': event.event_title,
            'start': event.event_init_date.isoformat(),
            'end': event.event_last_date.isoformat(),
            'url': event.get_absolute_url(),
            'place': event.event_place,
            'comments': event.comments,
        })

    return JsonResponse(event_list, safe=False)

def edit_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_app:event_detail', event_id=event_id)
    else:
        form = EventForm(instance=event)

    return render(request, 'event_app/edit_event.html', {'form': form, 'event': event})

def delete_event(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    if request.method == 'POST':
        event.delete()
        return redirect('event_app:event_calendar')

    return render(request, 'event_app/delete_event.html', {'event': event})