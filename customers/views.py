from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from khamka.views import LoginRequiredMixin
from customers.models import Customer
from customers.forms import CustomerForm
# Create your views here.
class CustomerListView(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'customers/list.html'
    

class CustomerCreateView(LoginRequiredMixin, CreateView):
    model = Customer
    template_name = 'customers/create.html'
    success_url = '/customers/'
    form_class = CustomerForm


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/update.html'
    success_url = '/customers/'