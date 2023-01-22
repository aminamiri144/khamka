from distutils.sysconfig import customize_compiler
from requisitions.models import Request, Attachment
from requisitions.forms import RequestsForm, RequestsUpdateForm, AttachmentForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin
from customers.models import Customer
from letters.models import Letter
from django.urls import reverse

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

    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که 
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(RequestUpdateView, self).get_context_data(**kwargs)
        context['form'].fields['customer'].choices.field.queryset = Customer.objects.filter(pk=self.kwargs['pk'])
        context['customer_id'] = self.kwargs['pk']
        return context

    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        customer = self.kwargs['pk']
        return {'customer': customer}

class RequestDetailView(LoginRequiredMixin, DetailView):
    model = Request
    template_name = 'requests/detail.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['letters_list'] = Letter.objects.filter(request=self.object.id)
        context['attachment_list'] = Attachment.objects.filter(request=self.object.id)
        return context



class AttachmentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Attachment
    template_name = 'requests/add-attachment.html'
    #success_url = '/requestions/'
    form_class = AttachmentForm
    success_message = " جدید با موفقیت افزوده شد !"
    # این بخش که کامنت شده برای تغییر داده های فرم بعد از سابمیت به کار میره که فعلا کاریش نداریم 
    # def form_valid(self, form): 
    #     form.instance.customer = Customer.objects.get(pk=self.kwargs['customer'])
    #     return super(RequestCreateView, self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که 
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(AttachmentCreateView, self).get_context_data(**kwargs)
        context['form'].fields['request'].choices.field.queryset = Request.objects.filter(pk=self.kwargs['pk'])
        context['id_request'] = self.kwargs['pk']
        return context
    
    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        return {'request': self.kwargs['pk']}

    def get_success_url(self):
        return reverse('request-detail', kwargs={'pk': self.kwargs['pk'],})


class AttachmentDeleteView(DeleteView, LoginRequiredMixin, SuccessMessageMixin):
    model = Attachment
    success_message = "پیوست مورد نظر با موفقیت حذف شد."
    template_name = 'requests/delete-attachment.html'


    def get_success_url(self):
        self.r_id = Attachment.objects.get(pk=self.kwargs['pk']).request.id
        return reverse('request-detail', kwargs={'pk': self.r_id,})