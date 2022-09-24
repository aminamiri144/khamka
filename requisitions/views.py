from distutils.sysconfig import customize_compiler
from requisitions.models import Request
from requisitions.forms import RequestsForm, RequestsUpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin
from customers.models import Customer

class RequestListView(LoginRequiredMixin, ListView):
    paginate_by = 20
    model = Request
    context_object_name = 'requests'
    template_name = 'requests/list.html'

    def get_ordering(self):
        ordering = self.request.GET.get('ordering', '-register_date')
        return ordering

    def get_queryset(self):
        value = self.request.GET.get('q', '')
        option = self.request.GET.get('option', '')
        query = {f'{option}__icontains': value}
        if value:
            object_list = self.model.objects.filter(**query)
        else:
            object_list = self.model.objects.all()
        return object_list
    
    


class RequestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Request
    template_name = 'requests/create.html'
    success_url = '/requestions/'
    form_class = RequestsForm
    success_message = "درخواست جدید با موفقیت افزوده شد !"

    def form_valid(self, form):
        form.instance.customer = Customer.objects.get(pk=self.kwargs['customer'])
        context = {'customer':self.kwargs['customer']}
        return super(RequestCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super(RequestCreateView, self).get_context_data(**kwargs)
        context['customer_id'] = self.kwargs['customer']
        return context
    
    def get_initial(self):
      customer = self.kwargs['customer']
      return {
        'customer': customer,
      }


class RequestUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Request
    form_class = RequestsUpdateForm
    template_name = 'requests/update.html'
    success_url = '/requestions/'
    context_object_name = 'requests'
    success_message = "درخواست مورد نظر با موفقیت ویرایش شد!"


class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'requests/detail.html'
