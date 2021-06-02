import psutil
import os
import subprocess
from subprocess import STDOUT

def mytestfun():
    return "this is from worker"

def cpu_percentage():
    cp = psutil.cpu_percent()
    return cp

def core_count():
    cc = psutil.cpu_count(logical=True)
    return cc

# cross platform
def memory_in_all():
    output = psutil.virtual_memory()
    print(output)
    print(list(output))
    return "ok done"


# for linux 
def total_in_mb():
    # for linux 
    # mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') 
    # mem_mega= mem_bytes/(1024.**2)
    output = psutil.virtual_memory()
    mem = list(output)
    return int(mem[0]/1024**2)

def used_in_mb():
    output = psutil.virtual_memory()
    mem = list(output)
    return int(mem[3]/1024**2)


def memory_use_percentage():
    # used
    used_ram = psutil.virtual_memory().percent
    # available
    memory_use_percentage = psutil.virtual_memory().available * 100 / psutil.virtual_memory().total
    return used_ram

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def total_disk():
    total = ""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        # print(f"=== Device: {partition.device} ===")
        # print(f"  Mountpoint: {partition.mountpoint}")
        # print(f"  File system type: {partition.fstype}")
        if partition.mountpoint =="/":
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # this can be catched due to the disk that
                # isn't ready
                continue
            # print(f"  Total Size: {get_size(partition_usage.total)}")
            # print(f"  Used: {get_size(partition_usage.used)}")
            # print(f"  Free: {get_size(partition_usage.free)}")
            # print(f"  Percentage: {partition_usage.percent}%")
            total = get_size(partition_usage.total)
    # get IO statistics since boot
    # disk_io = psutil.disk_io_counters()
    # print(f"Total read: {get_size(disk_io.read_bytes)}")
    # print(f"Total write: {get_size(disk_io.write_bytes)}")
    
    return float(total[0:-2]);

def total_usage():
    total = ""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition.mountpoint =="/":
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            total = get_size(partition_usage.used)
    
    return float(total[0:-2])


def total_free():
    total = ""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if partition.mountpoint =="/":
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                continue
            total = get_size(partition_usage.free)
    return float(total[0:-2]);

def service_check(service_name):
    cmd = '''systemctl status {} | grep "Active:"'''.format(service_name)
    result = subprocess.check_output(cmd, shell=True, stderr=STDOUT)
    return (result.decode("utf-8")).strip()
