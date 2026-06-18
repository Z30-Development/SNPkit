import platform
import psutil
import socket

try:
    from cpuinfo import get_cpu_info as cpuinfo_get_cpu_info
except ImportError:
    cpuinfo_get_cpu_info = None


class CPUInfoError(Exception):
    """Base exception for CPU information errors."""
    pass


class CPUInfoDependencyError(CPUInfoError):
    """Raised when a required dependency is missing."""
    pass


class CPUModule:
    def __init__(self):
        pass

    def get_cpu_info(self) -> dict:
        """
        Returns detailed CPU information.

        Returns:
            dict: CPU information.
        """

        try:
            if get_cpu_info is None:
                raise CPUInfoDependencyError(
                    "py-cpuinfo is not installed. Run: pip install py-cpuinfo"
                )

            cpu = cpuinfo_get_cpu_info()
            freq = psutil.cpu_freq()

            return {
                "name": cpu.get("brand_raw"),
                "architecture": platform.machine(),
                "bits": cpu.get("bits"),
                "physical_cores": psutil.cpu_count(logical=False),
                "logical_threads": psutil.cpu_count(logical=True),
                "process_count": len(psutil.pids()),
                "current_frequency_ghz": (
                    round(freq.current / 1000, 2) if freq else None
                ),
                "min_frequency_ghz": (
                    round(freq.min / 1000, 2) if freq else None
                ),
                "max_frequency_ghz": (
                    round(freq.max / 1000, 2) if freq else None
                ),
                "usage_percent": psutil.cpu_percent(interval=1),
            }

        except CPUInfoDependencyError:
            raise

        except PermissionError as e:
            raise CPUInfoError(
                "Permission denied while accessing CPU information."
            ) from e

        except Exception as e:
            raise CPUInfoError(
                f"Failed to retrieve CPU information: {e}"
            ) from e

    def get_cpu_name(self) -> str:
        return self.get_cpu_info()["name"]

    def get_physical_cores(self) -> int:
        return self.get_cpu_info()["physical_cores"]

    def get_logical_threads(self) -> int:
        return self.get_cpu_info()["logical_threads"]

    def get_process_count(self) -> int:
        return self.get_cpu_info()["process_count"]

    def get_architecture(self) -> str:
        return self.get_cpu_info()["architecture"]

    def get_current_frequency(self) -> float:
        return self.get_cpu_info()["current_frequency_ghz"]

    def get_max_frequency(self) -> float:
        return self.get_cpu_info()["max_frequency_ghz"]

    def get_usage(self) -> float:
        return self.get_cpu_info()["usage_percent"]


_cpu_instance = CPUModule()


def get_cpu_info() -> dict:
    return _cpu_instance.get_cpu_info()


def get_cpu_name() -> str:
    return _cpu_instance.get_cpu_name()


def get_physical_cores() -> int:
    return _cpu_instance.get_physical_cores()


def get_logical_threads() -> int:
    return _cpu_instance.get_logical_threads()


def get_process_count() -> int:
    return _cpu_instance.get_process_count()


def get_architecture() -> str:
    return _cpu_instance.get_architecture()


def get_current_frequency() -> float:
    return _cpu_instance.get_current_frequency()


def get_max_frequency() -> float:
    return _cpu_instance.get_max_frequency()


def get_usage() -> float:
    return _cpu_instance.get_usage()






# ------------------------------------------------------------------------------------

try:
    import pynvml
except ImportError:
    pynvml = None


class GPUInfoError(Exception):
    """Base exception for GPU information errors."""
    pass


class GPUInfoDependencyError(GPUInfoError):
    """Raised when a required dependency is missing."""
    pass


class GPUModule:
    def __init__(self):
        pass

    def get_gpu_info(self) -> dict:
        """
        Returns detailed GPU information.

        Returns:
            dict: GPU information.
        """

        try:
            if pynvml is None:
                raise GPUInfoDependencyError(
                    "pynvml is not installed. Run: pip install nvidia-ml-py"
                )

            pynvml.nvmlInit()

            handle = pynvml.nvmlDeviceGetHandleByIndex(0)

            mem = pynvml.nvmlDeviceGetMemoryInfo(handle)
            util = pynvml.nvmlDeviceGetUtilizationRates(handle)

            try:
                temperature = pynvml.nvmlDeviceGetTemperature(
                    handle,
                    pynvml.NVML_TEMPERATURE_GPU
                )
            except Exception:
                temperature = None

            return {
                "name": pynvml.nvmlDeviceGetName(handle),
                "memory_total_mb": round(mem.total / 1024**2, 2),
                "memory_used_mb": round(mem.used / 1024**2, 2),
                "memory_free_mb": round(mem.free / 1024**2, 2),
                "memory_usage_percent": round(
                    (mem.used / mem.total) * 100, 2
                ),
                "gpu_usage_percent": util.gpu,
                "memory_controller_usage_percent": util.memory,
                "temperature_c": temperature,
            }

        except GPUInfoDependencyError:
            raise

        except PermissionError as e:
            raise GPUInfoError(
                "Permission denied while accessing GPU information."
            ) from e

        except Exception as e:
            raise GPUInfoError(
                f"Failed to retrieve GPU information: {e}"
            ) from e

        finally:
            if pynvml is not None:
                try:
                    pynvml.nvmlShutdown()
                except Exception:
                    pass

    def get_gpu_name(self) -> str:
        return self.get_gpu_info()["name"]

    def get_gpu_memory_total(self) -> float:
        return self.get_gpu_info()["memory_total_mb"]

    def get_gpu_memory_used(self) -> float:
        return self.get_gpu_info()["memory_used_mb"]

    def get_gpu_memory_free(self) -> float:
        return self.get_gpu_info()["memory_free_mb"]

    def get_gpu_memory_usage(self) -> float:
        return self.get_gpu_info()["memory_usage_percent"]

    def get_gpu_usage(self) -> float:
        return self.get_gpu_info()["gpu_usage_percent"]

    def get_gpu_temperature(self) -> float:
        return self.get_gpu_info()["temperature_c"]


_gpu_instance = GPUModule()


def get_gpu_info() -> dict:
    return _gpu_instance.get_gpu_info()


def get_gpu_name() -> str:
    return _gpu_instance.get_gpu_name()


def get_gpu_memory_total() -> float:
    return _gpu_instance.get_gpu_memory_total()


def get_gpu_memory_used() -> float:
    return _gpu_instance.get_gpu_memory_used()


def get_gpu_memory_free() -> float:
    return _gpu_instance.get_gpu_memory_free()


def get_gpu_memory_usage() -> float:
    return _gpu_instance.get_gpu_memory_usage()


def get_gpu_usage() -> float:
    return _gpu_instance.get_gpu_usage()


def get_gpu_temperature() -> float:
    return _gpu_instance.get_gpu_temperature()


# ------------------------------------------------------------------------------------


class RAMInfoError(Exception):
    """Base exception for RAM information errors."""
    pass


class RAMInfoDependencyError(RAMInfoError):
    """Raised when a required dependency is missing."""
    pass


class RAMModule:
    def __init__(self):
        pass

    def get_ram_info(self) -> dict:
        """
        Returns detailed RAM information.

        Returns:
            dict: RAM information.
        """

        try:
            mem = psutil.virtual_memory()
            swap = psutil.swap_memory()

            return {
                "total_gb": round(mem.total / (1024 ** 3), 2),
                "available_gb": round(mem.available / (1024 ** 3), 2),
                "used_gb": round(mem.used / (1024 ** 3), 2),
                "free_gb": round(mem.free / (1024 ** 3), 2),
                "usage_percent": mem.percent,

                "swap_total_gb": round(swap.total / (1024 ** 3), 2),
                "swap_used_gb": round(swap.used / (1024 ** 3), 2),
                "swap_free_gb": round(swap.free / (1024 ** 3), 2),
                "swap_usage_percent": swap.percent,
            }

        except PermissionError as e:
            raise RAMInfoError(
                "Permission denied while accessing RAM information."
            ) from e

        except Exception as e:
            raise RAMInfoError(
                f"Failed to retrieve RAM information: {e}"
            ) from e

    def get_total_ram(self) -> float:
        return self.get_ram_info()["total_gb"]

    def get_available_ram(self) -> float:
        return self.get_ram_info()["available_gb"]

    def get_used_ram(self) -> float:
        return self.get_ram_info()["used_gb"]

    def get_free_ram(self) -> float:
        return self.get_ram_info()["free_gb"]

    def get_ram_usage(self) -> float:
        return self.get_ram_info()["usage_percent"]

    def get_swap_usage(self) -> float:
        return self.get_ram_info()["swap_usage_percent"]


_instance = RAMModule()


def get_ram_info() -> dict:
    return _instance.get_ram_info()


def get_total_ram() -> float:
    return _instance.get_total_ram()


def get_available_ram() -> float:
    return _instance.get_available_ram()


def get_used_ram() -> float:
    return _instance.get_used_ram()


def get_free_ram() -> float:
    return _instance.get_free_ram()


def get_ram_usage() -> float:
    return _instance.get_ram_usage()


def get_swap_usage() -> float:
    return _instance.get_swap_usage()



# ------------------------------------------------------------------------------------

class NetworkAdapterError(Exception):
    """Base exception for network adapter errors."""
    pass


class NetworkModule:
    def __init__(self):
        pass

    def get_network_adapters(self) -> list:
        try:
            adapters = []

            addresses = psutil.net_if_addrs()
            stats = psutil.net_if_stats()

            for name, addr_list in addresses.items():
                ipv4 = None
                ipv6 = None
                mac = None

                for addr in addr_list:
                    if addr.family == socket.AF_INET:
                        ipv4 = addr.address

                    elif addr.family == socket.AF_INET6:
                        ipv6 = addr.address

                    elif (
                        getattr(psutil, "AF_LINK", None)
                        and addr.family == psutil.AF_LINK
                    ):
                        mac = addr.address

                adapter_stats = stats.get(name)

                adapters.append({
                    "name": name,
                    "is_up": (
                        adapter_stats.isup
                        if adapter_stats
                        else None
                    ),
                    "speed_mbps": (
                        adapter_stats.speed
                        if adapter_stats
                        else None
                    ),
                    "mtu": (
                        adapter_stats.mtu
                        if adapter_stats
                        else None
                    ),
                    "ipv4": ipv4,
                    "ipv6": ipv6,
                    "mac_address": mac,
                })

            return adapters

        except Exception as e:
            raise NetworkAdapterError(
                f"Failed to retrieve network adapters: {e}"
            ) from e

    def get_adapter_names(self) -> list:
        return [
            adapter["name"]
            for adapter in self.get_network_adapters()
        ]

    def get_active_adapters(self) -> list:
        return [
            adapter
            for adapter in self.get_network_adapters()
            if adapter["is_up"]
        ]

    def get_primary_adapter(self) -> dict | None:
        adapters = self.get_active_adapters()

        return adapters[0] if adapters else None


_network_instance = NetworkModule()


def get_network_adapters() -> list:
    return _network_instance.get_network_adapters()


def get_adapter_names() -> list:
    return _network_instance.get_adapter_names()


def get_active_adapters() -> list:
    return _network_instance.get_active_adapters()


def get_primary_adapter() -> dict | None:
    return _network_instance.get_primary_adapter()