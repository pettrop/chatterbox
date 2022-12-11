from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
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


class RoomsView(LoginRequiredMixin, ListView):
    template_name = 'base/rooms.html'
    # extra_context = {'rooms': Room.objects.all()}
    model = Room


# ALTERNATIVNY ZAPIS PRI POUZITI TemplateView
# class RoomsView(TemplateView):
#     template_name = 'base/rooms.html'
#     extra_context = {'rooms': Room.objects.all()}


@login_required
@permission_required(['base.view_room', 'base.view_message'])
def room(request, pk):
    room = Room.objects.get(pk=pk)
    messages = room.message_set.all()
    # POST

    if request.user.has_perm('base.add_messages'):
        if request.method == 'POST':

        # ukladani
            Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body_message')
            )
            room.participants.add(request.user)
        return redirect('room', pk=pk)

    # GET
    context = {'messages': messages,
               'room': room
               }
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