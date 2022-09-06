from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render


class LoginRequiredMixin(object):
    """
    این کلاس در بررسی لاگین بودن یا نبودن
    کاربر کاربرد دارد.
    """

    login_required = True

    @classmethod
    def as_view(cls, **kwargs):
        self = cls()
        view = super(LoginRequiredMixin, cls).as_view(**kwargs)
        if self.login_required:
            return login_required(view)
        else:
            return view



class SuccessMessageMixin:
    """
    Add a success message on successful form submission.
    """
    success_message = ''
    css = ''
    
    def form_valid(self, form):
        response = super().form_valid(form)
        success_message = self.get_success_message(form.cleaned_data)
        if success_message:
            messages.success(self.request, success_message)
        return response

    def get_success_message(self, cleaned_data):
        return self.success_message % cleaned_data




def index(request):
    context = {}
    return render(request, 'panel.html', context=context)

def login(request):
    context = {}
    return render(request, 'login.html', context=context)

def registerrequest(request):
    context = {}
    return render(request, 'rere.html', context=context)