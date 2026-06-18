from snpkit.core import ip as ip_module

ip_module.make_default_ip_type("ipv4")
print("Default IP type set to IPv4")

public_ip_v4 = ip_module.get_public_ip()
print(f"Public IP (IPv4): {public_ip_v4}")

public_ip_v6 = ip_module.get_public_ip(type="ipv6")
print(f"Public IP (IPv6): {public_ip_v6}")

private_ip = ip_module.get_private_ip()
print(f"Private IP: {private_ip}")