from snpkit.core import mac as mac_module

mac_address = mac_module.get_mac_address(letter_case="lower")
print(f"MAC Address: {mac_address}")