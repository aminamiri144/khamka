from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth import logout
from requisitions.models import Request
from letters.models import Letter
from customers.forms import CustomerForm
from customers.models import Customer, CodeAuthSMS
from django.middleware import csrf
from customers.models import CodeAuthSMS
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
import time
import random
import json
from khamka.forms import Customer_register_form
from requisitions.forms import RequestForm2
from .sms import SMS
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
            return login_required(view, login_url='/register')
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
        return self.req.session['authentication'][0][data]

    def add_session_data(self, key, value):
        self.req.session['authentication'][0][key] = value
        self.req.session.modified = True

    def get_input_phone(self, value, more):
        return f"""<label for="phoneNumber">لطفا شماره تلفن همراه خود را وارد کنید.</label>
            <input type="phone" id="phoneNumber" name="phoneNumber" class="form-control" value="{value}" {more} maxlength="11" required>"""

    def get_input_code(self):
        return """
            <label for="phoneNumber">کد 5 رقمی پیامک شده را وارد کنید</label>
            <input type="charfield" id="regcode" name="regcode" class="form-control" placeholder="کد 5 رقمی پیامک شده به شماره موبایل را وارد کنید" maxlength="5" required>
            <div class="timer" style="margin-top: 10px;">
                <p>زمان انقضای کد</p>
            </div>"""

    def create_new_session(self):
        self.req.session['authentication'] = [{
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

        send_auth_code = SMS()
        send_auth_code.send(phone_number, code, '160216')
        print(send_auth_code.status)

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

    def get_context(self, form, request_is_POST=True, title_lvl='', alert = ''):
        ex = ''
        if request_is_POST:
            try:
                ex = self.get_expiry_time_status(self.get_session_data('mobile_number'))
            except:
                ex = ''
        have_form = False if form == None else True

        print('### session:  ',self.req.session['authentication'][0])

        return {
            'form': form,
            'expiry_code_time': ex,
            'title_lvl': title_lvl,
            'alert': alert,
            'have_form': have_form
        }

    def get_customer_register_form(self):
        return Customer_register_form()


def create_customer():
    pass


def two_factor_auth_login(request):
    s = AuthSession(request)
    HTML_FILE = 'rere.html'
    EXPIRE_CODE_TIME = 120 # زمان اعتبار کد تایید به ثانیه
    TITLE_LEVELS = [
        'ورود به سامانه',
        'تایید شماره تلفن',
        'ثبت نام اولیه در سامانه',
        'خوش آمدید'
    ]
    
    if request.method == 'GET':
        # در این شرط بررسی می شود سشن مربوطه ساخته شده یا خیر 
        if 'authentication' in request.session:
            # در این مرحله اگر سشن لول یک باشد ، سشن جدید ساخته میشود و کد اعتبار سنجی قبلی غیر فعال می شود
            if s.get_session_data('session_lvl') == '1':
                auth = CodeAuthSMS.objects.filter(phone=s.get_session_data('mobile_number')).latest('time_expiry')
                print(auth)
                s.create_new_session()
            # اگر سشن لول برابر 2 باشد یعنی کاربر ثبت نام نکرده و فرم ثبت نام براش ارسال میشه
            elif s.get_session_data('session_lvl') == '2':
                context = s.get_context(form=s.get_customer_register_form(), title_lvl=TITLE_LEVELS[2])
                return render(request, HTML_FILE, context)
            # اگر سشن لول برابر 3 باشد و کاربر تایید شده باشد کاربر به صفحه پنل کاربری هدایت می شود
            elif s.get_session_data('session_lvl') == '3' and s.get_session_data('is_verified'):
                context = s.get_context(form=None, title_lvl=TITLE_LEVELS[3], alert=s.alert_rase('success', 'با موفقیت وارد سامانه شدید'))
                return render(request, HTML_FILE, context)
        # اگر سشن وجود نداشته باشد سشن ایجاد میشود و فرم وارد کردن شماره موبایل ارسال می شود
        else:
            s.create_new_session()
        context = s.get_context(form=s.get_input_phone('', """placeholder="شماره تلفن را وارد کنید. مثال 09123456789" """), request_is_POST=False, title_lvl=TITLE_LEVELS[0])
        return render(request, HTML_FILE, context)

    # POST request
    if request.method == 'POST':
        lvl = s.get_session_data('session_lvl')
        # SESSION LEVEL 0
        # اگر سشن لول  0 باشد و ریکوئست از نوع پست ، شماره موبایل وارد شده کاربر در یافت می شود و کد اعتبار سنجی ایجاد و ارسال می شود
        if lvl == '0':
            phone_number = request.POST['phoneNumber']
            s.add_session_data('mobile_number', phone_number)
            s.create_auth_code(phone_number, EXPIRE_CODE_TIME)
            s.add_session_data('session_lvl', '1')
            context = s.get_context(form=s.get_input_phone(phone_number, "disabled") + s.get_input_code(), title_lvl=TITLE_LEVELS[1])
            return render(request, HTML_FILE, context)

        # SESSION LEVEL 1
        # در این لول کابر کد تایید را ارسال کرده و یا زمان اعتبار کد به پایان رسیده
        elif lvl == '1':
            # بررسی میکند اگر زمان اعتبار سنجی کد تایید به پایان رسیده باشد، کاربر به فرم ورود مجدد شماره موبایل هدایت می شود
            try:
                request_data = json.loads(request.body)
                if request_data['status'] == 'finish_time':
                    s.create_new_session()
                    # context = {'data': s.get_input_phone('', ''),'expire_code_time' : EXPIRE_CODE_TIME}
                    context = s.get_context(form=s.get_input_phone('', """placeholder="شماره تلفن را وارد کنید. مثال 09123456789" """), title_lvl=TITLE_LEVELS[0], alert = s.alert_rase('danger', 'زمان اعتبار کد پیامک شده به پایان رسید! لطفا مجددا تلاش کنید.'))
                    return render(request, HTML_FILE, context)
            # اگر زمان کد اعتبار سنجی معتبر بود وارد مرحله زیر می شود
            except:
                auth_obj = s.get_latest_authCode()
                #بررسی فعال بودن و درست بودن کد تایید ارسال شده
                if auth_obj.is_active == True and auth_obj.code == int(request.POST.get('regcode')):
                    # در این مرحله بررسی میشود که کاربر یوزر وارد شده کارمند هست یا خیر، اگر کارمند بود لاگین می شو.د و به پنل اصلی هدایت می شود
                    if User.objects.filter(username__exact=auth_obj.phone).exists():
                        user = User.objects.get(username__exact=auth_obj.phone)
                        login(request, user)
                        return redirect('/panel')
                    # بررسی شماره تلفن و ورود به عنوان ارباب رجوع
                    elif Customer.objects.filter(phoneNumber=auth_obj.phone).exists():
                        s.add_session_data('session_lvl', '3')
                        s.add_session_data('is_verified', True)
                        return redirect('/register')
                    # در حالت زیر کاربر وجود ندارد و باید به فرم ثبت نام هدایت شود
                    else:
                        s.add_session_data('session_lvl', '2')
                        return redirect('/register')
                # در این حالت سشن کد تایید غیر فعال است و مجدد باید به مرحله سشن جدید در لول 0 هدایت شود
                elif auth_obj.is_active == False:
                    s.add_session_data('session_lvl', '0')
                    return redirect('/register')
                # در این مرحله اگر کد وارد شده اشتباه باشد مجدد کاربر به فرم وارد کردن کد هدایت میشود با پیغام مربوطه
                else:
                    print('auth Code is incorrect')
                    context = s.get_context(form=s.get_input_phone(s.get_session_data('mobile_number'), "disabled") + s.get_input_code(), title_lvl=TITLE_LEVELS[1], alert=s.alert_rase('warning', 'کد وارد شده اشتباه است ! مجددا کد را وارد کنید.'))
                    return render(request, HTML_FILE, context)
        # SESSION LEVEL 2
        # در این مرحله کاربر وارد شده کاستومر یا ارباب رجوعی است که قبلا ثبت نام نکرده و ثبت نام او انجام می شود
        elif lvl == '2':
            customer_form = Customer_register_form(request.POST)
            if customer_form.is_valid():
                phoneNumber= s.get_session_data('mobile_number')
                fullname = request.POST['fullname']
                codemeli = request.POST['codemeli']
                sex = request.POST['sex']
                customer_obj = Customer(
                    phoneNumber=phoneNumber,
                    fullname=fullname,
                    code_meli=codemeli,
                    sex=sex,
                )
                customer_obj.save()
                s.add_session_data('session_lvl', '3')
                s.add_session_data('is_verified', True)
                return redirect('/register')
            # فرم ارسالی کاربر کامل نیست و مجدد باید تکمیل کند
            else:
                print('form not valid')
                context = s.get_context(form=Customer_register_form(request.POST), title_lvl=TITLE_LEVELS[2])
                return render(request, HTML_FILE, context)
        # SESSION LEVEL 3
        # فکر کنم با توجه به اینکه نوع ریدایرکت های قبلی گت هست این شرط هیچگاه برقرار نیست و باید پاک کرد
        elif lvl == '3' and s.get_session_data('is_verified'):
            context = s.get_context(form=None, title_lvl=TITLE_LEVELS[3], alert=s.alert_rase('success', 'با موفقیت وارد سامانه شدید'))
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

        return redirect('/register')


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
