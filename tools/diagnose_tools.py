import torch
import psutil
import platform
from datetime import datetime
import cpuinfo
import socket
import uuid
import re



def print_gpu_info(device,logger = None):
    #? Additional Info when using cuda:
    print("="*25)
    if device.type == 'cuda':
        # logger.log_parameter("gpu model" , torch.cuda.get_device_name(0))
        print('--> Memory Usage:')
        print('--> Allocated:', round(torch.cuda.memory_allocated(0)/1024**3,1), 'GB')
        print('--> Cached:   ', round(torch.cuda.memory_reserved(0)/1024**3,1), 'GB')
    else:
        print("--> NO GPU available.")


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

def System_information(device,logger=None):
    uname = platform.uname()
    print(f"System: {uname.system}")
    print(f"Node Name: {uname.node}")
    print(f"Release: {uname.release}")
    print(f"Version: {uname.version}")
    print(f"Machine: {uname.machine}")
    print(f"Processor: {uname.processor}")
    # logger.log_parameter("Processor" , cpuinfo.get_cpu_info()['brand_raw'])
    print(f"Ip-Address: {socket.gethostbyname(socket.gethostname())}")
    print(f"Mac-Address: {':'.join(re.findall('..', '%012x' % uuid.getnode()))}")
    

    #? Boot Time
    print("="*40, "Boot Time", "="*40)
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)
    print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")


    #? print CPU information
    print("="*40, "CPU Info", "="*40)
    #? number of cores
    # logger.log_parameter("cpu: Physical cores" , psutil.cpu_count(logical=False))
    # logger.log_parameter("cpu: Total cores" , psutil.cpu_count(logical=True))
    #? CPU frequencies
    cpufreq = psutil.cpu_freq()
    print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
    print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
    print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
    #? CPU usage
    print("CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(f"Core {i}: {percentage}%")
    print(f"Total CPU Usage: {psutil.cpu_percent()}%")


    #? Memory Information
    print("="*40, "Memory Information", "="*40)
    
    #? get the memory details
    svmem = psutil.virtual_memory()
    print(f"Total: {get_size(svmem.total)}")
    # logger.log_parameter("Available Ram" , get_size(svmem.available))
    
    print(f"Used: {get_size(svmem.used)}")
    print(f"Percentage: {svmem.percent}%")
    
    print_gpu_info(device,logger)
