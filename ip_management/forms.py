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

def generate_subnet_masks():
    # 255.255.255.255から始まり、0.0.0.0までのすべてのサブネットマスクを生成
    subnet_masks = []
    for i in range(256):
        for j in range(i + 1):
            # ビット列を生成
            bits = '1' * j + '0' * (32 - j)
            # 8ビットごとに分割して、整数に変換
            mask_parts = [str(int(bits[k:k + 8], 2)) for k in range(0, 32, 8)]
            # ドットで結合してサブネットマスクを生成
            mask = '.'.join(mask_parts)
            if mask not in subnet_masks:
                subnet_masks.append(mask)
    return subnet_masks


class SubnetForm(forms.ModelForm):
    prefix_length = forms.IntegerField(label='Prefix Length', min_value=0, max_value=32)

    class Meta:
        model = Subnet
        fields = ['network_address', 'prefix_length', 'description']

    def clean(self):
        cleaned_data = super().clean()
        network_address = cleaned_data.get('network_address')
        prefix_length = cleaned_data.get('prefix_length')

        # ここにプレフィックス長からサブネットマスクを計算するロジックを追加
        subnet_mask = str(IPv4Network(f'0.0.0.0/{prefix_length}').netmask)

        # バリデーション後にサブネットマスクをcleaned_dataに追加
        cleaned_data['subnet_mask'] = subnet_mask
        return cleaned_data

    # フォームを保存する際には、プレフィックス長をサブネットマスクに変換して保存
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.subnet_mask = self.cleaned_data['subnet_mask']
        if commit:
            instance.save()
        return instance

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

    def clean_ip_address(self):
        ip_address = self.cleaned_data['ip_address']
        validate_ipv4_address(ip_address)
        return ip_address

    def clean(self):
        cleaned_data = super().clean()
        ip_address_input = cleaned_data.get('ip_address')
        subnet_instance = cleaned_data.get('subnet')

        if not ip_address_input or not subnet_instance:
            raise ValidationError('サブネットとIPアドレスは必須です。')

        ip_addresses = IPAddress.objects.filter(subnet=subnet_instance)

        if ip_addresses.filter(ip_address=ip_address_input).exists():
            raise ValidationError(f'{ip_address_input}はすでに登録されています。')

        # サブネットのCIDR表記を作成する
        subnet_cidr = f'{subnet_instance.network_address}/{subnet_instance.get_prefix_length()}'
        network = ip_network(subnet_cidr)

        # 入力されたIPアドレスがサブネットに含まれているか確認
        if ip_address(ip_address_input) not in network:
            raise ValidationError(f'{ip_address_input}は{subnet_cidr}に所属しません。')

        return cleaned_data

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['hostname', 'device_type', 'description']
