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
from customers.models import Customer, CodeAuthSMS
from django.middleware import csrf
from customers.models import CodeAuthSMS
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
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
    success_url = '/panel'

    def get_redirect_url(self):
        return '/panel'

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


class AuthSession:
    def __init__(self, request):
        self.req = request

    def get_session_data(self, data):
        return self.req.session['mobile_auth'][0][data]

    def add_session_data(self, key, value):
        self.req.session['mobile_auth'][0][key] = value
        self.req.session.modified = True

    def get_input_phone(self, value, more):
        return f"""<label for="phoneNumber">لطفا شماره تلفن همراه خود را وارد کنید.</label>
            <input type="phone" id="phoneNumber" name="phoneNumber" class="form-control" value="{value}" {more} maxlength="11" required>"""

    def get_input_code(self):
        return """
            <label for="phoneNumber">کد 5 رقمی پیامک شده را وارد کنید</label>
            <input type="charfield" id="regcode" name="regcode" class="form-control" placeholder="کد 5 رقمی پیامک شده به شماره موبایل را وارد کنید" maxlength="5" required>
            <div class="timer" style="justify-content: center; align-items: center; height: 5vh;">
                <p>زمان انقضای کد</p>
            </div>"""

    def create_new_session(self):
        self.req.session['mobile_auth'] = [{
            'mobile_number': '',
            'is_verified': False,
            'session_lvl': '0',
        }]
        self.req.session.modified = True

    def create_auth_code(self, phone_number, expiry_time):
        code = random.randint(10000, 99999)
        authCode = CodeAuthSMS(
            phone=phone_number,
            code=code,
            is_active=True,
            time_expiry=str(int(time.time()) + expiry_time),
        )
        authCode.save()

    def get_latest_authCode(self):
        return CodeAuthSMS.objects.filter(phone=self.get_session_data('mobile_number')).latest('time_expiry')

    def alert_rase(self, type, message):
        return f"""
            <div class="alert alert-{ type }" role="alert">
                 {message}
            </div>
        """

    def get_expiry_time_status(self, phone_number):
        a = CodeAuthSMS.objects.filter(
            phone=phone_number).latest('time_expiry')
        remaining_expiry_time = int(time.time()) - int(a.time_expiry)
        return abs(remaining_expiry_time)

    def get_context(self, data, request_is_POST=True, title_lvl=''):
        ex = ''
        if request_is_POST:
            ex = self.get_expiry_time_status(
                self.get_session_data('mobile_number'))

        return {
            'data': data,
            'expiry_code_time': ex,
            'title_lvl': title_lvl,
        }

    def get_register_customer_form(self):
        return """
            <label for="fullname">نام و نام خانوادگی</label>
            <input type="charfield" id="fullname" name="fullname" class="form-control" required>
            <label for="codemeli">کد ملی</label>
            <input type="charfield" id="codemeli" name="codemeli" class="form-control" maxlength="10" required>  
        """


def two_factor_auth_login(request):
    s = AuthSession(request)
    HTML_FILE = 'rere.html'
    EXPIRE_CODE_TIME = 120
    TITLE_LEVELS = [
        'ورود به سامانه',
        'تایید شماره تلفن',
        'ثبت نام اولیه در سامانه',
        'ثبت درخواست'
    ]
    if request.method == 'GET':
        if 'mobile_auth' in request.session and s.get_session_data('session_lvl') == '1':
            auth = CodeAuthSMS.objects.filter(
                phone=s.get_session_data('mobile_number')).latest('time_expiry')
            print(auth)
            s.create_new_session()
        else:
            s.create_new_session()
        context = s.get_context(data=s.get_input_phone(
            '', """placeholder="شماره تلفن را وارد کنید. مثال 09123456789" """), request_is_POST=False, title_lvl=TITLE_LEVELS[0])
        return render(request, HTML_FILE, context)

    # POST request
    if request.method == 'POST':
        lvl = s.get_session_data('session_lvl')

        # SESSION LEVEL 0
        if lvl == '0':
            phone_number = request.POST['phoneNumber']
            s.add_session_data('mobile_number', phone_number)
            s.create_auth_code(phone_number, EXPIRE_CODE_TIME)

            print(request.session['mobile_auth'])
            s.add_session_data('session_lvl', '1')
            context = s.get_context(data=s.get_input_phone(
                phone_number, "disabled") + s.get_input_code(), title_lvl=TITLE_LEVELS[1])
            return render(request, HTML_FILE, context)

        # SESSION LEVEL 1
        elif lvl == '1':
            try:
                request_data = json.loads(request.body)
                if request_data['status'] == 'finish_time':
                    s.create_new_session()
                    # context = {'data': s.get_input_phone('', ''),'expire_code_time' : EXPIRE_CODE_TIME}
                    context = s.get_context(data=s.get_input_phone(
                        '', ''), title_lvl=TITLE_LEVELS[0])
                    return render(request, HTML_FILE, context)
            except Exception as e:
                auth_obj = s.get_latest_authCode()
                # بررسی فعال بودن کد تایید و
                if auth_obj.is_active == True and auth_obj.code == int(request.POST.get('regcode')):
                    print('login successful')
                    # بررسی شماره تلفن و ورود به صورت کارمند
                    try:
                        user_obj = User.objects.filter(
                            username__exact=auth_obj.phone)[0].username
                    except:
                        user_obj = None
                    # بررسی شماره تلفن و ورود به عنوان ارباب رجوع
                    if auth_obj.phone == user_obj:
                        user = User.objects.get(username__exact=auth_obj.phone)
                        # user.backend = 'django.contrib.auth.backends.ModelBackend'
                        login(request, user)
                        print('user is admin -> login ')
                        return redirect('/panel')

                    elif not Customer.objects.filter(phoneNumber=auth_obj.phone).exists():
                        s.add_session_data('session_lvl', '2')
                        return redirect('/register')

                elif auth_obj.is_active == False:
                    print('login failed - time expired')
                else:
                    print('auth Code is incorrect')
                    context = s.get_context(data=s.alert_rase('warning', 'کد وارد شده اشتباه است !') + s.get_input_phone(s.get_session_data('mobile_number'), "disabled") + s.get_input_code(), title_lvl=TITLE_LEVELS[1])
                    return render(request, HTML_FILE, context)
        elif lvl == '2':

            if request.POST.get('fullname'):
                print('fullname is :' , request.POST['fullname'])
                context = s.get_context(data=s.get_register_customer_form(), title_lvl=TITLE_LEVELS[2])
                print(request.session)
                return render(request, HTML_FILE, context)
            else:
                print('fullname is empty')
                context = s.get_context(data=s.get_register_customer_form(), title_lvl=TITLE_LEVELS[2])
                print(request.session)
                return render(request, HTML_FILE, context)


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
