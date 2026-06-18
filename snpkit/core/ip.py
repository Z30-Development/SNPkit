from urllib.request import urlopen
from urllib.error import URLError
import socket

class IPv6NotAvailableError(Exception):
    """Will be raised when there is no public IPv6 address available."""
    pass

class IPModule:
    def __init__(self):
        self._default_ip_type: str = None

    def make_default_ip_type(self, type: str) -> None:
        """Sets the default IP type for get_public_ip(type=None)."""
        if type == "":
            self._default_ip_type = None
        else:
            type = type.lower()
            if type not in ("ipv4", "ipv6"):
                raise ValueError("Invalid IP type. Use 'ipv4', 'ipv6' or '' to reset.")
            self._default_ip_type = type

    def has_ipv6(self) -> bool:
        try:
            infos = socket.getaddrinfo(
                socket.gethostname(),
                None,
                socket.AF_INET6
            )

            for info in infos:
                ip = info[4][0]

                if (
                    ip != "::1"
                    and not ip.startswith("fe80:")
                    and not ip.startswith("fc")
                    and not ip.startswith("fd")
                ):
                    return True

            return False

        except socket.gaierror:
            return False

    def get_public_ip(self, type: str = None) -> str:
        try:
            resolved_type = type if type is not None else self._default_ip_type

            if resolved_type is None:
                ip = urlopen("https://api.ipify.org").read().decode("utf-8")
                return ip + " (Default IP type: IPv4)"

            else:
                resolved_type = resolved_type.lower()

                if resolved_type == "ipv4":
                    ip = urlopen("https://api4.ipify.org").read().decode("utf-8")

                elif resolved_type == "ipv6":
                    if not self.has_ipv6():
                        raise IPv6NotAvailableError("No public IPv6 address is available on this system.")

                    ip = socket.getaddrinfo(socket.gethostname(), None, socket.AF_INET6)[0][4][0]

                else:
                    raise ValueError("Invalid IP type. Use 'ipv4', 'ipv6' or leave empty for default.")

                return ip

        except (IPv6NotAvailableError, ValueError):
            raise

        except URLError as e:
            raise ConnectionError("Unable to connect to the IP service.") from e

        except ConnectionError:
            raise ConnectionError("Unable to connect to the IP service. Please check your internet connection.")

        except Exception:
            raise Exception("An unexpected error occurred while fetching the public IP.")
        
    def get_private_ip(self) -> str:
        try:
            hostname = socket.gethostname()
            private_ip = socket.gethostbyname(hostname)
            return private_ip
        except socket.gaierror:
            raise ConnectionError("Unable to resolve the hostname to a private IP address.")
        
_instance = IPModule()

def make_default_ip_type(type: str = None) -> None:
    _instance.make_default_ip_type(type)

def get_public_ip(type: str = None) -> str:
    return _instance.get_public_ip(type)

def get_private_ip() -> str:
    return _instance.get_private_ip()