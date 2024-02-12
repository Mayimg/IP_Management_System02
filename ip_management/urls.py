from django.urls import path
from . import views


urlpatterns = [
    path('subnets/', views.subnet_list, name='subnet-list'),
    path('subnets/add/', views.SubnetCreate.as_view(), name='subnet-add'),
    path('subnets/<int:pk>/', views.SubnetUpdate.as_view(), name='subnet-update'),
    path('subnets/<int:pk>/delete/', views.SubnetDelete.as_view(), name='subnet-delete'),
    path('ipaddresses/', views.IPAddressList.as_view(), name='ipaddress-list'),
    path('ipaddresses/add/', views.IPAddressCreate.as_view(), name='ipaddress-add'),
    path('ipaddresses/<int:pk>/', views.IPAddressUpdate.as_view(), name='ipaddress-update'),
    path('ipaddresses/<int:pk>/delete/', views.IPAddressDelete.as_view(), name='ipaddress-delete'),
    path('devices/', views.DeviceList.as_view(), name='device-list'),
    path('devices/add/', views.DeviceCreate.as_view(), name='device-add'),
    path('devices/<int:pk>/', views.DeviceUpdate.as_view(), name='device-update'),
    path('devices/<int:pk>/delete/', views.DeviceDelete.as_view(), name='device-delete'),
    path('subnets/<int:pk>/ipaddresses/', views.SubnetDetailView.as_view(), name='subnet-ipaddress-list'),
    path('devices/<int:pk>/ipaddresses/', views.DeviceDetailView.as_view(), name='device-ipaddress-list'),
    path('ping_ip/', views.ping_ip, name='ping-ip'),
    path('download_excel/', views.download_excel_file, name='download_excel'),
    # その他のURLパターン...
]
