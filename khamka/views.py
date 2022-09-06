from django.contrib.auth.decorators import login_required




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


def index(request):
    context = {}
    return render(request, 'panel.html', context=context)

def login(request):
    context = {}
    return render(request, 'login.html', context=context)

def registerrequest(request):
    context = {}
    return render(request, 'rere.html', context=context)