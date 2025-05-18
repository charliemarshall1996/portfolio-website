
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView

from crm.models import Client


class ClientListView(ListView):
    model = Client
    template_name = 'crm/generics/list.html'

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)
        context['title'] = 'Clients'
        context['table_headers'] = ['Name', 'Email',
                                    'Phone', 'Created At', 'Updated At']
        return context
