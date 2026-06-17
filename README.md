

# SNPkit
SNPKit is a BETA network utility toolkit for retrieving network, hardware and geolocation information. Future modules will include Discord webhook embed sending utilities and a custom RPC system for Discord.

---

## Installation:
- ### Windows:
```bash
pip install SNPkit
```
- ### Linux:
> Note: Assume the virtual environment (venv) has already been created!
```bash
pip install SNPkit
```
- ### Create Virtual Environment:
1. Windows:
```bash
python -m venv venv
venv\Scripts\activate.bat
```
2. Linux / macOS:
```bash
python -m venv venv
source venv/bin/activate
```
---

## Dependencies:
- Windows 10 / 11
- Python >=3.8  (Max. Python 3.14)

---

## Features:
- Retrieve public and local IP information
- Retrieve hardware information (CPU, RAM, OS, hostname, etc.)
- Geolocation lookup based on IP addresses
- Cross-platform support (Windows, Linux, macOS)
- Simple and lightweight
- BETA: Additional modules are currently under active development

---

## Examples:

### IP-Module:
```python
from snpkit.core import ip as ip_module   # Import the IP-Module

ip_module.make_default_ip_type("ipv4")    # Set the default IP retrievement Method

public_ip = ip_module.get_public_ip()     # Get the Public IP based on the default IP retrievement Method
private_ip = ip_module.get_private_ip()   # Get the Private IP
```

### MAC-Module:
```python
from snpkit.core import mac as mac_module                         # Import the MAC-Module

mac_address = mac_module.get_mac_address(letter_case="lower")     # Get the MAC-Address. Output based on the letter_case option
```
