#ip_vvalidation.py

#IPアドレスのバリデーション

from django.core.exceptions import ValidationError
from ipaddress import IPv4Address, IPv4Network, AddressValueError, NetmaskValueError


def validate_ipv4_address(ip_address):
    try:
        IPv4Address(ip_address)
    except AddressValueError:
        raise ValidationError('Invalid IPv4 address')

def validate_subnet(subnet): 
    try:
        IPv4Network(subnet)
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 subnet')
    
def validate_subnet_mask(subnet_mask):
    try:
        mask = IPv4Network(f'0.0.0.0/{subnet_mask}', strict=False).netmask
        if str(mask) != subnet_mask:
            raise ValidationError('Invalid IPv4 subnet mask')
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 subnet mask')
        
def create_cidr_from_subnet(subnet, subnet_mask):
    validate_subnet(subnet)
    validate_subnet_mask(subnet_mask)

    try:
        network_address = IPv4Network(f'{subnet}/{subnet_mask}', strict=False)
        return str(network_address)
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 subnet or subnet mask')
    
def validate_ip_in_subnet(ip_address, subnet_cidr):
    validate_ipv4_address(ip_address)
    try:
        ip = IPv4Address(ip_address)
        network = IPv4Network(subnet_cidr)
        if ip not in network:
            raise ValidationError(f'{ip_address} is not in {subnet_cidr}')
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 address or subnet')
    
def is_network_address(ip_address, subnet_cidr):
    validate_ipv4_address(ip_address)
    try:
        ip = IPv4Address(ip_address)
        network = IPv4Network(subnet_cidr, strict=False)
        if ip == network.network_address:
            return True
        return False
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 address or subnet')

def is_host_address(ip_address, subnet_cidr):
    validate_ipv4_address(ip_address)
    try:
        ip = IPv4Address(ip_address)
        network = IPv4Network(subnet_cidr, strict=False)
        if ip == network.network_address or ip == network.broadcast_address:
            return False
        return True
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 address or subnet')

def is_broadcast_address(ip_address, subnet_cidr):
    validate_ipv4_address(ip_address)
    try:
        ip = IPv4Address(ip_address)
        network = IPv4Network(subnet_cidr, strict=False)
        if ip == network.broadcast_address:
            return True
        return False
    except (AddressValueError, NetmaskValueError):
        raise ValidationError('Invalid IPv4 address or subnet')
    
    
   






