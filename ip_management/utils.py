def subnet_mask_to_prefix_length(subnet_mask):
    # サブネットマスクをプレフィクス長に変換する
    return sum(bin(int(x)).count('1') for x in subnet_mask.split('.'))

def prefix_length_to_subnet_mask(prefix_length):
    # プレフィクス長をサブネットマスクに変換する
    mask = ((1 << 32) - (1 << 32 >> prefix_length))
    return f"{(mask >> 24) & 0xFF}.{(mask >> 16) & 0xFF}.{(mask >> 8) & 0xFF}.{mask & 0xFF}"

