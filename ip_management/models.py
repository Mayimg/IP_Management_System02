from django.db import models
from ipaddress import ip_network

# Create your models here.

class Device(models.Model):
    hostname = models.CharField(max_length=255, unique=True)
    device_type = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.hostname

class Subnet(models.Model):
    network_address = models.CharField(max_length=15)
    subnet_mask = models.CharField(max_length=15)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['network_address', 'subnet_mask']]

    def get_prefix_length(self):
        # ip_network 関数を使用してサブネットのプレフィックス長を取得
        # ここで self.subnet_mask はサブネットマスクの文字列であることが前提
        return ip_network(f'0.0.0.0/{self.subnet_mask}', strict=False).prefixlen

    def __str__(self):
        return self.network_address

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
        
    def __str__(self):
        return self.ip_address



