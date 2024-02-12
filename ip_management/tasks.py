import os
from .models import IPAddress

def ping_ip_addresses():
    for ip in IPAddress.objects.all():
        response = os.system("ping -c 1 " + ip.ip_address)
        # PINGコマンドが0を返した場合は成功、それ以外は失敗
        ip.last_ping_status = (response == 0)
        ip.save()
        