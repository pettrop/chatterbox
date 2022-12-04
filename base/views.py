from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, FormView, CreateView
from base.models import Room
from base.forms import RoomForm
from django.urls import reverse_lazy

# Create your views here.


def hello(request):
    s = request.GET.get('s', '')
    return HttpResponse(f"Ahoj {s}!")


# def rooms(request):
#     rooms = Room.objects.all()
#     context = {'rooms': rooms}
#     return render(request, template_name='base/rooms.html', context=context)


class RoomsView(ListView):
    template_name = 'base/rooms.html'
    #extra_context = {'rooms': Room.objects.all()}
    model = Room

# ALTERNATIVNY ZAPIS PRI POUZITI TemplateView
# class RoomsView(TemplateView):
#     template_name = 'base/rooms.html'
#     extra_context = {'rooms': Room.objects.all()}


def room(request, id):
    room = Room.objects.get(id=id)
    messages = room.message_set.all()
    # alternativne vypisanie sprav, ale filer sa pouziva skor pri hladani v pripadoch ked chceme nieco >viac alebo <menej ako
    # messages = Message.objects.filter(room__id=id)
    context = {'messages': messages,
               'room': room}
    return render(request, template_name='base/room.html', context=context)


class RoomCreateView(CreateView):
    form_class = RoomForm
    template_name = 'base/root_form.html'
    success_url = reverse_lazy('rooms')