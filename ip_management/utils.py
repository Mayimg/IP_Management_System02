import xlsxwriter
from .models import Device, Subnet, IPAddress
from io import BytesIO

def subnet_mask_to_prefix_length(subnet_mask):
    # サブネットマスクをプレフィクス長に変換する
    return sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))

def prefix_length_to_subnet_mask(prefix_length):
    # プレフィクス長をサブネットマスクに変換する
    mask = ((1 << 32) - (1 << 32 >> prefix_length))
    return f"{(mask >> 24) & 0xFF}.{(mask >> 16) & 0xFF}.{(mask >> 8) & 0xFF}.{mask & 0xFF}"

def export_to_excel():
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    worksheet = workbook.add_worksheet()
    # workbook = xlsxwriter.Workbook('IP_Management_System_Data.xlsx')
    # worksheet = workbook.add_worksheet()

    # Headers
    headers = ['Hostname', 'Device Type', 'IP Address', 'Subnet', 'Domain Name', 'Description']
    for col, text in enumerate(headers):
        worksheet.write(0, col, text)

    devices = Device.objects.all()
    row = 1
    for device in devices:
        ip_addresses = IPAddress.objects.filter(device=device)
        for ip in ip_addresses:
            data = [
                device.hostname,
                device.device_type,
                ip.ip_address,
                f'{ip.subnet.network_address}/{ip.subnet.get_prefix_length()}',
                ip.domain_name,
                ip.description,
            ]
            for col, text in enumerate(data):
                worksheet.write(row, col, text)
            row += 1

    workbook.close()
    output.seek(0)
    # return 'IP_Management_System_Data.xlsx'
    return output
    