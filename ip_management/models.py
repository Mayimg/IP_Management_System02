from django.db import models
from django.core.exceptions import ValidationError
from ipaddress import ip_network
from .libs import ip_validation

# Create your models here.

class Device(models.Model):
    hostname = models.CharField(max_length=255, unique=True, blank=False)
    device_type = models.CharField(max_length=255, blank=False)
    description = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname

    def clean_hostname(self):
        if not self.hostname:
            raise ValidationError('Hostname cannot be blank.')
        if len(self.hostname) > 255:
            raise ValidationError('Hostname cannot be longer than 255 characters.')
        
    def clean_device_type(self):
        if self.device_type:
            raise ValidationError('Device type cannot be blank.')
        if len(self.device_type) > 255:
            raise ValidationError('Device type cannot be longer than 255 characters.')
        
    def clean(self):
        cleaned_data = super().clean()
        self.clean_hostname()
        self.clean_device_type()
        return cleaned_data

    
class IPAddressRange(models.Model):
    subnet = models.ForeignKey('Subnet', on_delete=models.CASCADE)
    purpose = models.CharField(max_length=255)
    start_ip_address = models.CharField(max_length=15)
    end_ip_address = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.start_ip_address} - {self.end_ip_address}'

class Subnet(models.Model):
    network_address = models.CharField(max_length=15)
    subnet_mask = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['network_address', 'subnet_mask']]

    def get_prefix_length(self):
        return ip_network(f'0.0.0.0/{self.subnet_mask}', strict=False).prefixlen

    def __str__(self):
        return self.network_address
    
    def clean_network_address(self):
        ip_validation.validate_subnet(self.network_address)

    def clean_network_mask(self):
        ip_validation.validate_subnet_mask(self.subnet_mask)

    def clean(self):
        cleaned_data = super().clean()
        self.clean_network_address()
        self.clean_network_mask()
        return cleaned_data


class IPAddress(models.Model):
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=15, unique=True)
    domain_name = models.CharField(max_length=255, blank=True)
    description = models.TextField( blank=True)
    last_ping_status = models.BooleanField(default=False)
    assigned_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'IP Address'
        verbose_name_plural = 'IP Addresses'
        ordering = ['ip_address']  # IPアドレスで昇順に並べる
        

    def clean_ip_address(self):
        ip_validation.validate_ipv4_address(self.ip_address)

    def __str__(self):
        return self.ip_address



