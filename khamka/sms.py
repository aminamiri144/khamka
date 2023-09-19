from .melipayamak import Api
from requisitions.models import Setting

# def send_validate_sms():
#     username = '9103264969'
#     password = 'ZY9C4'
#     api = Api(username, password)
#     sms_rest = api.sms()
#     to = '09103264969'
#     send = sms_rest.send_by_base_number('44583', to, '160216')
#     print(send)



class SMS:
    def __init__(self):
        self.status = None
    
    def api(self):
        username = Setting.objects.get(key__exact='sms_panel_username').value
        password = Setting.objects.get(key__exact='sms_panel_password').value
        return Api(username, password)
    
    def send(self, phone, number, message_code):
        self.status = self.api().sms().send_by_base_number(number, phone, message_code)
        return self.status




    

    
