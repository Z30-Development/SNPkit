import uuid

class MACModule:
    def __init__(self):
        self._letter_case = "lower"
        pass
    
    def get_mac_address(self, letter_case: str = None) -> str:
        mac = uuid.getnode()
        mac_address = ':'.join(f'{(mac >> ele) & 0xff:02x}' for ele in range(40, -1, -8))

        if not letter_case:
                letter_case = self._letter_case

        if letter_case == "upper":
            mac_address = mac_address.upper()
        elif letter_case == "lower":
            mac_address = mac_address.lower()
        else:
            raise ValueError("Invalid letter_case. Use 'upper', 'lower' or None for default.")

        return mac_address
    
_instance = MACModule()

def get_mac_address(letter_case: str = None) -> str:
    return _instance.get_mac_address(letter_case)