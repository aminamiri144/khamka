from django.shortcuts import render
from letters.models import Letter
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.detail import DetailView
from khamka.views import LoginRequiredMixin, SuccessMessageMixin
from letters.forms import LetterForm
# Create your views here.



class LetterCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Letter
    template_name = 'letter/create.html'
    success_url = '/letters/'
    form_class = LetterForm
    success_message = "درخواست دهنده جدید با موفقیت افزوده شد !"