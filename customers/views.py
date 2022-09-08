from unicodedata import name
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin
from customers.models import Customer
from customers.forms import CustomerForm



# Create your views here.
class CustomerListView(LoginRequiredMixin, ListView):
    paginate_by = 10
    model = Customer
    context_object_name = 'customers'
    template_name = 'customers/list.html'



    def get_queryset(self):
        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
        query = {f'{option}__icontains': value}
        if value:
            object_list = self.model.objects.filter(**query)
        else:
            object_list = self.model.objects.all()
        return object_list
    

class CustomerCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Customer
    template_name = 'customers/create.html'
    success_url = '/customers/'
    form_class = CustomerForm
    success_message = "درخواست دهنده جدید با موفقیت افزوده شد !"



class CustomerUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'customers/update.html'
    success_url = '/customers/'
    success_message = "درخواست دهنده مورد نظر با موفقیت ویرایش شد."
