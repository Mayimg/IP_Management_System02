from django.test import TestCase
from ..models import Device, Subnet, IPAddress

class DeviceModelTest(TestCase):
    def setUp(self):
        Device.objects.create(hostname='Router1', device_type='Router')

    def test_device_creation(self):
        device = Device.objects.get(hostname='Router1')
        self.assertTrue(isinstance(device, Device))
        self.assertEqual(device.__str__(), device.hostname)


class SubnetModelTest(TestCase):
    def setUp(self):
        Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
    
    def test_subnet_creation(self):
        subnet = Subnet.objects.get(network_address='10.0.0.0')
        self.assertTrue(isinstance(subnet, Subnet))
        self.assertEqual(subnet.__str__(), subnet.network_address)
        self.assertEqual(subnet.get_prefix_length(), 8)

class IPAddressModelTest(TestCase):
    def setUp(self):
        subnet = Subnet.objects.create(network_address='10.0.0.0', subnet_mask='255.0.0.0')
        device = Device.objects.create(hostname='Router1', device_type='Router')
        IPAddress.objects.create(subnet=subnet, device=device, ip_address='10.0.0.1')

    def test_ip_address_creation(self):
        ip_address = IPAddress.objects.get(ip_address='10.0.0.1')
        self.assertTrue(isinstance(ip_address, IPAddress))
        self.assertEqual(ip_address.__str__(), ip_address.ip_address)
        self.assertEqual(ip_address.subnet.network_address, '10.0.0.0')
        self.assertEqual(ip_address.device.hostname, 'Router1')
        self.assertEqual(ip_address.subnet.get_prefix_length(), 8)
        
