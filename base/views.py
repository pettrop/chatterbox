from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import ListView, FormView, CreateView, UpdateView, DeleteView
from base.models import Room, Message
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

@login_required
@permission_required(['base.view_room'])
def search(request):
    q = request.GET.get('q', '')
    rooms = Room.objects.filter(
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    context = {
        'object_list': rooms
    }
    return render(request, 'base/rooms.html', context=context)


class RoomsView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    template_name = 'base/rooms.html'
    # extra_context = {'rooms': Room.objects.all()}
    model = Room
    permission_required = 'base.view_room'


# ALTERNATIVNY ZAPIS PRI POUZITI TemplateView
# class RoomsView(TemplateView):
#     template_name = 'base/rooms.html'
#     extra_context = {'rooms': Room.objects.all()}



def room(request, pk):
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        if request.user.has_perm('base.add_message'):
            Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body_message')
            )
            room.participants.add(request.user)
            room.save()
        return redirect('room', pk=pk)

    messages = room.message_set.all()
    context = {'messages': messages, 'room': room}
    return render(request, template_name='base/room.html', context=context)


class RoomCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = RoomForm
    extra_context = {'title': 'CREATE Room'}
    template_name = 'base/root_form.html'
    success_url = reverse_lazy('rooms')
    permission_required = 'base.add_room'


class RoomUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Room
    template_name = 'base/root_form.html'
    extra_context = {'title': 'UPDATE Room'}
    form_class = RoomForm
    success_url = reverse_lazy('rooms')
    permission_required = 'base.change_room'


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff


class RoomDeleteView(StaffRequiredMixin, PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    template_name = 'base/room_confirm_delete.html'
    model = Room
    extra_context = {'title': 'DELETE Room'}
    success_url = reverse_lazy('rooms')
    permission_required = 'base.delete_room'


def handler403(request, exception=None):
    return render(request, '403.html', status=403)


def handler404(request, exception=None):
    return render(request, '404.html', status=404)