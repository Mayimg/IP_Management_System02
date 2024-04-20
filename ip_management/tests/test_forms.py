from django.test import TestCase
from ..forms import SubnetForm
from ..forms import IPAddressForm
from ..models import Device
from ..models import Subnet
from ..models import IPAddress

from django.core.exceptions import ValidationError

class SubnetFormTest(TestCase) :
    def test_valid_form(self) :
        form_data = {
            'network_address': '10.0.0.0',
            'prefix_length': 8,
            'description': 'Test Subnet'
        }
        form = SubnetForm(data=form_data)
        self.assertTrue(form.is_valid())

        subnet = form.save()
        self.assertEqual(subnet.network_address, '10.0.0.0')
        self.assertEqual(subnet.subnet_mask, '255.0.0.0')
        self.assertEqual(subnet.description, 'Test Subnet')

    def test_invalid_network_address(self) :
        form_data = {
            'network_address': '300.0.0.0',
            'prefix_length': 8,
            'description': 'Test Subnet'
        }
        form = SubnetForm(data=form_data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError):
            form.clean()
    
    def test_invalid_prefix_length(self) :
       form_data = {
            'network_address': '10.0.0.0',
            'prefix_length': 33,
            'description': 'Test Subnet'
        }
       form = SubnetForm(data=form_data)
       self.assertFalse(form.is_valid())

       with self.assertRaises(ValidationError):
            form.clean()

    def test_invalid_network_address(self) :
        form_data = {
            'network_address': '192.168.0.1',
            'prefix_length': 24,
            'description': 'Invalid network address for subnet'
        }
        form = SubnetForm(data=form_data)
        self.assertFalse(form.is_valid())
        with self.assertRaises(ValidationError):
            form.clean()


class IPAddressFormTest(TestCase):
    def setUp(self):
        self.device = Device.objects.create(hostname='TestDevice', device_type='Test')
        self.subnet = Subnet.objects.create(network_address='192.168.0.0', subnet_mask='255.255.255.0', description='Test Subnet')

    def test_valid_form(self):
        form_data = {
            'device': self.device.id,
            'subnet': self.subnet.id,
            'ip_address': '192.168.0.1',
            'domain_name': 'test.example.com',
            'description': 'Test IP Address'
        }
        form = IPAddressForm(data=form_data)
        self.assertTrue(form.is_valid())

        ip_address = form.save()
        self.assertEqual(ip_address.device, self.device)
        self.assertEqual(ip_address.subnet, self.subnet)
        self.assertEqual(ip_address.ip_address, '192.168.0.1')
        self.assertEqual(ip_address.domain_name, 'test.example.com')
        self.assertEqual(ip_address.description, 'Test IP Address')

    

