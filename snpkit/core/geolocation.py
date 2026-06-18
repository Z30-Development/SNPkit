import geocoder
import ipaddress

class geolocation:
    def __init__(self, target_ip: str = "me"):
        self._target_ip = target_ip
        self._geo = None

    def _load(self):
        if self._geo is None:
            try:
                g = geocoder.ip(self._target_ip)
            except Exception as e:
                raise ConnectionError(
                    f"Failed to contact geolocation service: {e}"
                ) from e

            if not g.ok:
                raise ValueError(
                    f"Invalid IP or no geolocation data found for "
                    f"'{self._target_ip}'. "
                    "Use a public IPv4/IPv6 address or leave empty for default ('me')."
                )

            self._geo = g

        return self._geo

    def get_geolocation(self, target_ip: str = None) -> dict:
        if target_ip is not None:
            self._target_ip = target_ip
            self._geo = None

        return {
            "ip": self.ip,
            "type": self.type,
            "city": self.city,
            "state": self.state,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    @property
    def ip(self):
        return self._load().ip

    @property
    def type(self):
        try:
            version = ipaddress.ip_address(self.ip).version
            return f"IPv{version}"
        except ValueError:
            return None

    @property
    def city(self):
        return self._load().city

    @property
    def state(self):
        return self._load().state

    @property
    def country(self):
        return self._load().country

    @property
    def latitude(self):
        return self._load().lat

    @property
    def longitude(self):
        return self._load().lng