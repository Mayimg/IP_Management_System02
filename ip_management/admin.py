from django.contrib import admin
from .models import Subnet, IPAddress, Device

# Register your models here.

# モデルを管理サイトに登録
admin.site.register(Subnet)
admin.site.register(IPAddress)
admin.site.register(Device)

