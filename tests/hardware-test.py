from snpkit.core import hardware as hw


def run_cpu_tests():
    print("\n[CPU TEST]")

    print("CPU Info:", hw.get_cpu_info())
    print("Name:", hw.get_cpu_name())
    print("Cores:", hw.get_physical_cores())
    print("Threads:", hw.get_logical_threads())
    print("Processes:", hw.get_process_count())
    print("Arch:", hw.get_architecture())
    print("Freq current:", hw.get_current_frequency())
    print("Freq max:", hw.get_max_frequency())
    print("Usage:", hw.get_usage())


def run_gpu_tests():
    print("\n[GPU TEST]")

    try:
        print("GPU Info:", hw.get_gpu_info())
        print("Name:", hw.get_gpu_name())
        print("Memory total:", hw.get_gpu_memory_total())
        print("Memory used:", hw.get_gpu_memory_used())
        print("Memory free:", hw.get_gpu_memory_free())
        print("Usage:", hw.get_gpu_usage())
        print("Temp:", hw.get_gpu_temperature())
    except Exception as e:
        print("GPU not available:", e)


def run_ram_tests():
    print("\n[RAM TEST]")

    print("RAM Info:", hw.get_ram_info())
    print("Total:", hw.get_total_ram())
    print("Available:", hw.get_available_ram())
    print("Used:", hw.get_used_ram())
    print("Free:", hw.get_free_ram())
    print("Usage %:", hw.get_ram_usage())
    print("Swap %:", hw.get_swap_usage())


def run_network_tests():
    print("\n[NETWORK TEST]")

    print("Adapters:", hw.get_network_adapters())
    print("Names:", hw.get_adapter_names())
    print("Active:", hw.get_active_adapters())
    print("Primary:", hw.get_primary_adapter())


if __name__ == "__main__":
    print("=== SNPKIT HARDWARE TEST START ===")

    run_cpu_tests()
    run_gpu_tests()
    run_ram_tests()
    run_network_tests()

    print("\n=== TEST COMPLETE ===")