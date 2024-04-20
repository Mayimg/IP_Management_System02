from django.test import TestCase
from ..models import Device, Subnet, IPAddress
from django.core.exceptions import ValidationError
from django.db import IntegrityError


class DeviceModelTest(TestCase):
    def test_device_creation(self):
        Device.objects.create(hostname='Router1', device_type='Router')
        device = Device.objects.get(hostname='Router1')
        self.assertTrue(isinstance(device, Device))
        self.assertEqual(device.__str__(), device.hostname)

    def test_unique_hostname(self):
        Device.objects.create(hostname='Router1', device_type='Router')
        with self.assertRaises(IntegrityError):
            Device.objects.create(hostname='Router1', device_type='Router_Duplicate')

    def test_hostname_blank(self): 
       with self.assertRaises(ValidationError):
        device = Device(hostname='', device_type='Router')
        device.full_clean()

    def test_device_type_blank(self):
        Device.objects.create(hostname='Router1', device_type='')
        device = Device.objects.get(hostname='Router1')
        self.assertTrue(isinstance(device, Device))
        self.assertEqual(device.device_type, '')

    def test_device_description_blank(self):
        Device.objects.create(hostname='Router1', device_type='Router', description='')
        device = Device.objects.get(hostname='Router1')
        self.assertTrue(isinstance(device, Device))
        self.assertEqual(device.description, '')
    
    def test_device_duplicate_type(self):
        Device.objects.create(hostname='Router1', device_type='Router')
        Device.objects.create(hostname='Router2', device_type='Router')
        device1 = Device.objects.get(hostname='Router1')
        device2 = Device.objects.get(hostname='Router2')
        self.assertTrue(isinstance(device1, Device))
        self.assertTrue(isinstance(device2, Device))
        self.assertEqual(device1.device_type, 'Router')
        self.assertEqual(device2.device_type, 'Router')


class SubnetModelTest(TestCase):
    def test_subnet_creation(self):
        Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
        subnet = Subnet.objects.get(network_address='10.0.0.0')
        self.assertTrue(isinstance(subnet, Subnet))
        self.assertEqual(subnet.__str__(), subnet.network_address)
        self.assertEqual(subnet.get_prefix_length(), 8)

    def test_invalid_subnet_creation(self):
        with self.assertRaises(ValidationError):
            subnet = Subnet.objects.create(network_address='999.0.0.0', subnet_mask='255.0.0.0')
            subnet.full_clean()

    def test_invalid_subnet_mask_creation(self):
        with self.assertRaises(ValidationError):
            subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.256')
            subnet.full_clean()

    def test_nonNetworkAddress_creation(self):
        with self.assertRaises(ValidationError):
            subnet = Subnet.objects.create(network_address='10.0.0.1', subnet_mask='255.0.0.0')
            subnet.full_clean()
        with self.assertRaises(ValidationError):
            subnet = Subnet.objects.create(network_address='10.255.255.255', subnet_mask='255.0.0.0')
            subnet.full_clean()

    def test_subnet_unique_together(self):
        Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0', description='Test 1')
        with self.assertRaises(IntegrityError):
            Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0', description='Test 2')


class IPAddressModelTest(TestCase):
    def test_ip_address_creation(self):
        subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
        device = Device.objects.create(hostname='Router1', device_type='Router')
        ip_address = IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.0.0.1')
        self.assertTrue(isinstance(ip_address, IPAddress))
        self.assertEqual(ip_address.__str__(), ip_address.ip_address)
        self.assertEqual(ip_address.subnet.network_address, '10.0.0.0')
        self.assertEqual(ip_address.device.hostname, 'Router1')
        
    def test_invalid_ip_address_creation(self):
        subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
        device = Device.objects.create(hostname='Router1', device_type='Router')
        with self.assertRaises(ValidationError):
            ip_address = IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.0.0.256')
            ip_address.full_clean()

    def test_ip_invalid_ip_in_subnet(self):
        subnet = Subnet.objects.create(network_address='192.168.1.0', subnet_mask='255.255.255.0')
        device = Device.objects.create(hostname='Router1', device_type='Router')
        with self.assertRaises(ValidationError):
            ip_address = IPAddress.objects.create(subnet=subnet, device=device, ip_address='192.168.3.1')
            ip_address.full_clean()

    def test_ip_network_address(self):
        subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
        device = Device.objects.create(hostname='Router1', device_type='Router')
        with self.assertRaises(ValidationError):
            ip_address = IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.0.0.0')
            ip_address.full_clean()

    def test_ip_broadcast_address(self):
        subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
        device = Device.objects.create(hostname='Router1', device_type='Router')
        with self.assertRaises(ValidationError):
            ip_address = IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.255.255.255')
            ip_address.full_clean()

    def test_ip_address_unique_together(self):
        subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0') 
        device = Device.objects.create(hostname='Router1', device_type='Router')
        IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.0.0.1')
        with self.assertRaises(IntegrityError):
            IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.0.0.1')

