from django.shortcuts import render
import os
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from .models import Subnet
from .forms import SubnetForm
from .utils import subnet_mask_to_prefix_length
from .models import IPAddress
from .forms import IPAddressForm
from .models import Device
from .forms import DeviceForm
from django.views.generic import DetailView
from django.http import JsonResponse

# Create your views here.

def subnet_list(request):
    subnets = Subnet.objects.all().order_by('network_address')  # データベースから全てのサブネットを取得
    return render(request, 'ip_management/subnet_list.html', {'subnets': subnets})


class SubnetCreate(CreateView):
    model = Subnet
    form_class = SubnetForm
    template_name = 'ip_management/subnet_form.html'
    success_url = reverse_lazy('subnet-list')

class SubnetUpdate(UpdateView):
    model = Subnet
    form_class = SubnetForm
    template_name = 'ip_management/subnet_form.html'
    success_url = reverse_lazy('subnet-list')
    def get_initial(self):
        initial = super().get_initial()
        initial['prefix_length'] = subnet_mask_to_prefix_length(self.object.subnet_mask)
        return initial


class SubnetDelete(DeleteView):
    model = Subnet
    template_name = 'ip_management/subnet_confirm_delete.html'
    success_url = reverse_lazy('subnet-list')

class IPAddressList(ListView):
    model = IPAddress
    template_name = 'ip_management/ipaddress_list.html'
    context_object_name = 'ipaddresses' 
    paginate_by = 30

class IPAddressCreate(CreateView):
    model = IPAddress
    form_class = IPAddressForm
    template_name = 'ip_management/ipaddress_form.html'
    success_url = reverse_lazy('ipaddress-list')

class IPAddressUpdate(UpdateView):
    model = IPAddress
    form_class = IPAddressForm
    template_name = 'ip_management/ipaddress_form.html'
    success_url = reverse_lazy('ipaddress-list')

class IPAddressDelete(DeleteView):
    model = IPAddress
    template_name = 'ip_management/ipaddress_confirm_delete.html'
    success_url = reverse_lazy('ipaddress-list')

class DeviceList(ListView):
    model = Device
    template_name = 'ip_management/device_list.html'
    context_object_name = 'devices'
    paginate_by = 30
    def get_queryset(self):
        return Device.objects.all().order_by('hostname')  # ホスト名で昇順に並べ替え

class DeviceCreate(CreateView):
    model = Device
    form_class = DeviceForm
    template_name = 'ip_management/device_form.html'
    success_url = reverse_lazy('device-list')

class DeviceUpdate(UpdateView):
    model = Device
    form_class = DeviceForm
    template_name = 'ip_management/device_form.html'
    success_url = reverse_lazy('device-list')

class DeviceDelete(DeleteView):
    model = Device
    template_name = 'ip_management/device_confirm_delete.html'
    success_url = reverse_lazy('device-list')


class SubnetDetailView(DetailView):
    model = Subnet
    template_name = 'ip_management/subnet_detail.html'
    context_object_name = 'subnet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ipaddresses'] = self.object.ipaddress_set.all()  # Subnet に関連付けられた IPAddress のリストを取得
        return context
    
class DeviceDetailView(DetailView):
    model = Device
    template_name = 'ip_management/device_detail.html'
    context_object_name = 'device'

    def get_context_data(self, **kwargs) :
        context = super().get_context_data(**kwargs)
        context['ipaddresses'] = self.object.ipaddress_set.all() # Device に関連付けられた IPAddress のリストを取得
        return context
    

def ping_ip(request):
    # AJAXリクエストかどうかを確認
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        for ip in IPAddress.objects.all():
            response = os.system(f"ping -c 1 {ip.ip_address}")
            ip.last_ping_status = (response == 0)
            ip.save()
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"})