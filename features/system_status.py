import psutil

def get_system_status():
    cpu = psutil.cpu_percent(interval=0.5)
    ram = psutil.virtual_memory().percent

    battery = psutil.sensors_battery()
    if battery:
        battery_percent = battery.percent
    else:
        battery_percent = "N/A"

    return {
        "cpu": cpu,
        "ram": ram,
        "battery": battery_percent
    }
