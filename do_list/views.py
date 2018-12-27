from django.http import HttpResponseForbidden
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from .models import Note


class NoteListView(ListView):
    model = Note
    template_name = 'notes-list.html'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset


class NoteCreateView(CreateView):
    model = Note
    fields = ['description', 'due_date']
    template_name = 'create.html'
    success_url = reverse_lazy('note_all')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You have to sign in first.")
        return super().post(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden("You have to sign in first.")
        return super().get(request, *args, **kwargs)


class NoteDeleteView(DeleteView):
    model = Note
    template_name = 'delete.html'
    success_url = reverse_lazy('note_all')
    pk_url_kwarg = 'id'

class NoteUpdateView(UpdateView):
    model = Note
    template_name = 'update.html'
    success_url = reverse_lazy('note_all')
    pk_url_kwarg = 'id'
    fields = ['description', 'due_date']
