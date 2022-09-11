from requisitions.models import Request
from requisitions.forms import RequestsForm, RequestsUpdateForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin



class RequestListView(LoginRequiredMixin ,ListView):
    paginate_by = 20
    model= Request    
    context_object_name= 'requests'
    template_name = 'requests/list.html'



class RequestCreateView(LoginRequiredMixin , SuccessMessageMixin,CreateView):
    model = Request
    template_name = 'requests/create.html'
    success_url = '/requestions/'
    form_class = RequestsForm
    success_message = "درخواست جدید با موفقیت افزوده شد !"


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


