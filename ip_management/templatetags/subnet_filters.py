from django import template
from ipaddress import ip_network

register = template.Library()

@register.filter(name='subnet_mask_to_prefix_length')
def subnet_mask_to_prefix_length(subnet_mask):
    # サブネットマスクをプレフィクス長に変換
    return sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))


@register.simple_tag
def cidr_notation(network_address, subnet_mask):
    # ip_networkクラスを使用して、ネットワークアドレスとサブネットマスクからCIDR表記を生成します。
    network = ip_network(f"{network_address}/{subnet_mask}", strict=False)
    return str(network.with_prefixlen)
