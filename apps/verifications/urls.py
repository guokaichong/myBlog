from django.urls import path, re_path

from . import views

app_name = "verifications"

urlpatterns = [
    # image_code_id为uuid格式
    path('image_codes/<uuid:image_code_id>/', views.ImageCode.as_view(), name='image_code'),
    #  /image_codes/123e4567-e89b-12d3-a456-426655440000dhosdhod
    re_path('usernames/(?P<username>\w{5,20})/', views.CheckUsernameView.as_view(), name='check_username'),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/', views.CheckMobileView.as_view(), name='check_mobiles'),
    path('sms_codes/', views.SmsCodesView.as_view(), name='sms_codes'),
]