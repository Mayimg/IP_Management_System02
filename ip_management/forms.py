from django.forms import ModelForm
from .models import Subnet
from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from .utils import prefix_length_to_subnet_mask
from ipaddress import IPv4Network
from .models import IPAddress
from ipaddress import ip_network, ip_address
from .models import IPAddressRange
from django import forms
from .models import Subnet
from ipaddress import IPv4Network
from .models import Device
from .libs import ip_validation

class SubnetForm(forms.ModelForm):
    prefix_length = forms.IntegerField(label='Prefix Length', min_value=0, max_value=32)

    class Meta:
        model = Subnet
        fields = ['network_address', 'prefix_length', 'description']

    def clean_network_address(self):
        network_address = self.cleaned_data.get('network_address')
        if network_address:
            try:
                ip_validation.validate_subnet(network_address)
            except ValidationError as e:
                raise ValidationError(e)
        return network_address

    def clean_prefix_length(self):
        prefix_length = self.cleaned_data.get('prefix_length')
        if prefix_length is None:
            raise ValidationError('Prefix length is required.')
        elif not 0 <= prefix_length <= 32:
            raise ValidationError('Prefix length must be between 0 and 32.')
        self.prefix_length = prefix_length
        return prefix_length

    def clean_is_network_address(self):
        network_address = self.cleaned_data.get('network_address')
        if network_address and self.prefix_length:
            subnet_cidr = f'{network_address}/{self.prefix_length}'
            if not ip_validation.is_network_address(network_address, subnet_cidr):
                raise ValidationError(f'{network_address} is not a network address.')
        return network_address

    def clean(self):
        cleaned_data = super().clean()
        prefix_length = cleaned_data.get('prefix_length')

        self.clean_prefix_length()

        subnet_mask = str(IPv4Network(f'0.0.0.0/{prefix_length}').netmask)
        self.instance.subnet_mask = subnet_mask

        self.clean_network_address()
        self.clean_is_network_address()

        cleaned_data['subnet_mask'] = subnet_mask
        return cleaned_data
    
    def save(self, commit=True):
        subnet = Subnet(
            network_address=self.cleaned_data['network_address'],
            description=self.cleaned_data['description']
        )
        prefix_length = self.cleaned_data['prefix_length']
        subnet_mask = str(IPv4Network(f'0.0.0.0/{prefix_length}').netmask)
        subnet.subnet_mask = subnet_mask
        if commit:
            subnet.full_clean()
            subnet.save()
        return subnet
    
class IPAddressRangeForm(forms.ModelForm):
    class Meta:
        model = IPAddressRange
        fields = ['subnet', 'purpose', 'start_ip_address', 'end_ip_address']

    def clean(self):
        cleaned_data = super().clean()
        subnet = cleaned_data.get('subnet')
        start_ip_address = cleaned_data.get('start_ip_address')
        end_ip_address = cleaned_data.get('end_ip_address')


class IPAddressForm(forms.ModelForm):
    class Meta:
        model = IPAddress
        fields = ['device', 'subnet', 'ip_address', 'domain_name', 'description']

    def clean_device(self):
        device_instance = self.cleaned_data.get('device')
        if not device_instance:
            raise ValidationError('Device is required.')
        return device_instance
    
    def clean_subnet(self):
        subnet_instance = self.cleaned_data.get('subnet')  
        if not subnet_instance:
            raise ValidationError('Subnet is required.')
        return subnet_instance
    
    def clean_ip_address(self):
        ip_address = self.cleaned_data.get('ip_address')
        if not ip_address:
            raise ValidationError('IP Address is required.')
        validate_ipv4_address(ip_address)
        return ip_address
    
    def clean(self):
        cleaned_data = super().clean()

        self.clean_device()
        self.clean_subnet()
        self.clean_ip_address()

        return cleaned_data

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hostname', 'device_type', 'description']
