from django.shortcuts import render
from letters.models import Letter, Organ
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin
from letters.forms import LetterForm, OrganForm
from requisitions.models import Request


class LetterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Letter
    template_name = 'letters/create.html'
    success_url = '/letters/'
    form_class = LetterForm
    success_message = 'نامه جدید با موفقیت افزوده شد !'



    def get_context_data(self, **kwargs):
        """در اینجا فیلد کاستومر یا درخواست دهنده را طوری تنظیم میکنیم که 
        فقط درخواست دهنده ای که میخواهیم براش درخواست ثبت کنیم نمایش داده بشه
        و طوره نباشه که همه درخواست دهنده ها در اپشن های فیلد سلکت نمایش داده بشن
        """
        context = super(LetterCreateView, self).get_context_data(**kwargs)
        context['form'].fields['request'].choices.field.queryset = Request.objects.filter(pk=self.kwargs['requestid'])
        context['request_id'] = self.kwargs['requestid']
        return context
    
    def get_initial(self):
        """
        در اینجا مقدار فیلد درخواست دهنده را با توجه به ادرس مقدار دهی میکنیم 
        """
        customer = self.kwargs['requestid']
        return {'request': customer}




class OrganCreateView(CreateView, LoginRequiredMixin, SuccessMessageMixin):
    model = Organ
    template_name = 'organ/create.html'
    #success_url = '/letters/'
    form_class = OrganForm
    success_message = 'سازمان جدید با موفقیت افزوده شد !'

    def get_success_url(self):
        p = self.kwargs['craete_letter_id']
        return f'/letter/create/{p}'
