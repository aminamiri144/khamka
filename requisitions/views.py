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
        status = self.request.GET.get('status', '')
        if status and status != '0':
            object_list = self.model.objects.filter(status=status)
            return object_list
        else:
            query = {f'{option}__icontains': value}
            if value:
                object_list = self.model.objects.filter(**query)
                self.request.session['search'] = self.request.GET.get('q','')
            else:
                object_list = self.model.objects.all()

            return object_list
        
    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        if self.kwargs['option']:
            option = self.kwargs['option']
            return {'option': option}
    
    


class RequestCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Request
    template_name = 'requests/create.html'
    success_url = '/requestions/'
    form_class = RequestsForm
    success_message = "درخواست جدید با موفقیت افزوده شد !"
    # این بخش که کامنت شده برای تغییر داده های فرم بعد از سابمیت به کار میره که فعلا کاریش نداریم 
    # def form_valid(self, form): 
    #     form.instance.customer = Customer.objects.get(pk=self.kwargs['customer'])
    #     return super(RequestCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که 
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(RequestCreateView, self).get_context_data(**kwargs)
        context['form'].fields['customer'].choices.field.queryset = Customer.objects.filter(pk=self.kwargs['customer'])
        context['customer_id'] = self.kwargs['customer']
        return context
    
    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        customer = self.kwargs['customer']
        return {'customer': customer}


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
