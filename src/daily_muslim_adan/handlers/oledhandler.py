
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106  # Use sh1106 for SH1106 displays (or ssd1306 for SSD1306)
from luma.core.render import canvas
from datetime import datetime
import time

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)


def display_current_time_date(datetime_now):
    current_time = datetime_now.strftime("%H:%M:%S")  # Format: HH:MM:SS
    current_date = datetime_now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD

    # Display on the OLED
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((10, 20), f"Time: {current_time}", fill="white")  # Display time
        draw.text((10, 40), f"Date: {current_date}", fill="white")  # Display date


def display_next_adan_name_time(prayer_name, adan_time, remaining_time): # Format: YYYY-MM-DD

    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, outline="white", fill="black")
        draw.text((5, 10), f"Next Prayer: {prayer_name}", fill="white")  # Display time
        draw.text((5, 25), f"Prayer Time: {adan_time}", fill="white")
        draw.text((5, 40), f"Remaining: {remaining_time}", fill="white")