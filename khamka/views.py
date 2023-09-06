from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import logout
from django.shortcuts import redirect
from requisitions.models import Request
from letters.models import Letter
from requisitions.forms import RequestsForm, RequestForm2
from customers.forms import CustomerForm
from customers.models import Customer
from django.middleware import csrf
from customers.models import CodeAuthSMS
import time
import random
import json
# class Index(TemplateView):
#     template_name = "landing/index.html"


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


class UserLoginView(LoginView):
    """
    برای لاگین شدن کاربر استفاده میشود و
    از LoginView خود جانگو و فرم آن استفاده میکند

    """
    template_name = 'login.html'
    success_url = '/'

    def get_redirect_url(self):
        return '/'

    # def form_valid(self, form):
    #     """
    #     برای لاگ کردن ورود کاربر استفاده میشود

    #     Arguments:
    #         form:
    #             فرم ارسال شده است
    #     """
    #     res = super().form_valid(form)
    #     return res


class SoonView(LoginRequiredMixin, TemplateView):
    template_name = "soon.html"


class PanelView(LoginRequiredMixin, TemplateView):
    template_name = "panel.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['new_requests'] = Request.objects.filter(status='1')
        context['waiting_letters'] = Letter.objects.filter(status='1')
        return context


def registerrequest(request):
    if request.method == 'GET':
        if 'mobile_auth' in request.session:
            print('session is already created')
        else:
            request.session['mobile_auth'] = [{
                'mobile_number': '',
                'is_verified': False,
                'session_lvl': '0',
            }]
            request.session.modified = True
            print('session is now create')
        context = {'data': """<label for="phoneNumber">لطفا شماره تلفن همراه خود را وارد کنید.</label>
              <input type="phone" id="phoneNumber" name="phoneNumber" class="form-control">"""}
        return render(request, 'rere.html', context=context)

    if request.method == 'POST':
        lvl = request.session['mobile_auth'][0]['session_lvl']
        if lvl == '0':
            request.session['mobile_auth'][0]['mobile_number'] = request.POST['phoneNumber']
            code = random.randint(10000, 99999)

            authCode = CodeAuthSMS(
                phone=request.POST['phoneNumber'],
                code=code,
                is_active=True,
                time_expiry=str(int(time.time()) + 120),
            )
            authCode.save()

            print(request.session['mobile_auth'])
            request.session['mobile_auth'][0]['session_lvl'] = '1'
            request.session.modified = True
            context = {
                'data': f"""
            <label for="phoneNumber">لطفا شماره تلفن همراه خود را وارد کنید.</label>
            <input type="phone" id="phoneNumber" name="phoneNumber" class="form-control" placeholder="{request.session['mobile_auth'][0]['mobile_number']}">
            <label for="phoneNumber">کد پیامک شده را وارد کنید</label>
            <input type="charfield" id="regcode" name="regcode" class="form-control" placeholder="کد 5 رقمی پیامک شده به شماره موبایل را وارد کنید">
            <div class="timer" style="justify-content: center; align-items: center; height: 5vh;">
                <p>2:00</p>
            </div>
            """,
            }
            return render(request, 'rere.html', context=context)
        if lvl == '1':
            if request.method == 'POST':
                request_data = json.loads(request.body)
                if request_data['status'] == 'finish_time':
                    request.session['mobile_auth'] = [{
                        'mobile_number': '',
                        'is_verified': False,
                        'session_lvl': '0',
                    }]
                    request.session.modified = True
                    context = {'data':
                       """
                        <label for="phoneNumber">لطفا شماره تلفن همراه خود را وارد کنید.</label>
                        <input type="phone" id="phoneNumber" name="phoneNumber" class="form-control">
                        """}
                    return render(request, 'rere.html', context=context)


class UserLogoutView(LoginRequiredMixin, View):
    """
    برای خروج کاربر یا اصطلاحاً لاگ آوت استفاده میشود
    و پس از لاگ اوت کاربر را به صفحه لاگین هدایت میکند

    Arguments:
        request:
           درخواست ارسال شده به صفحه است

    """

    def get(self, request):
        # request.user.last_logout = timezone.now()
        # request.user.last_activity = timezone.now()
        # request.user.save()
        # log_save(request.user, 1, 2, True)
        logout(request)

        return redirect('/accounts/login')


def register_customer_request(request):

    message = ''
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        request_form = RequestForm2(request.POST)
        if customer_form.is_valid() and request_form.is_valid():
            is_customer_exist = Customer.objects.filter(
                phoneNumber=customer_form.cleaned_data['phoneNumber']).exists()
            if not is_customer_exist:
                customer = Customer(
                    phoneNumber=customer_form.cleaned_data['phoneNumber'],
                    fullname=customer_form.cleaned_data['fullname'],
                    organ=customer_form.cleaned_data['organ'],
                    code_meli=customer_form.cleaned_data['code_meli'],
                    sex=customer_form.cleaned_data['sex'],
                    phone=customer_form.cleaned_data['phone'],
                    address=customer_form.cleaned_data['address'],
                )
                customer.save()
                requestions = Request(
                    number=request_form.cleaned_data['number'],
                    title=request_form.cleaned_data['title'],
                    register_date=request_form.cleaned_data['register_date'],
                    customer=customer,
                    description=request_form.cleaned_data['description'],
                    status=request_form.cleaned_data['status'],
                    result=request_form.cleaned_data['result'],
                    category=request_form.cleaned_data['category'],
                    created_by=request_form.cleaned_data['created_by'],
                )
                requestions.save()

                return redirect(f'/requestions/detail/{requestions.id}')

            else:
                message = 'این درخواست دهنده با این شماره موبایل قبلا ثبت شده. لطفا از صفحه درخواست دهندگان اقدام به ثبت درخواست کنید.'

        context = {
            'request_form': request_form,
            'customer_form': customer_form,
            'message': message,
        }
        return render(request, 'register_both_customer_request.html', context=context)

    context = {
        'request_form': RequestForm2,
        'customer_form': CustomerForm,
    }
    return render(request, 'register_both_customer_request.html', context=context)
