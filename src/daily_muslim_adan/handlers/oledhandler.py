from luma.core.interface.serial import i2c
from luma.oled.device import sh1106  # Use sh1106 for SH1106 displays (or ssd1306 for SSD1306)
from luma.core.render import canvas
from datetime import datetime
import time
import logging

# Initialize logging
logger = logging.getLogger(__name__)

serial = i2c(port=1, address=0x3C)
device = sh1106(serial)

def retry_display_operation(operation_func, max_retries=3, delay=0.1):
    """Retry display operations with exponential backoff for intermittent I2C errors."""
    for attempt in range(max_retries):
        try:
            operation_func()
            return True
        except OSError as e:
            if e.errno == 5:  # Input/output error
                if attempt < max_retries - 1:
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"I2C error on attempt {attempt + 1}, retrying in {wait_time:.2f}s: {e}")
                    time.sleep(wait_time)
                else:
                    logger.error(f"I2C error after {max_retries} attempts, giving up: {e}")
                    return False
            else:
                logger.error(f"Unexpected OSError: {e}")
                return False
        except Exception as e:
            logger.error(f"Unexpected error during display operation: {e}")
            return False
    return False

def display_current_time_date(datetime_now):
    """Display current time and date on OLED with retry logic."""
    current_time = datetime_now.strftime("%H:%M:%S")  # Format: HH:MM:SS
    current_date = datetime_now.strftime("%Y-%m-%d")  # Format: YYYY-MM-DD

    def _display():
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((10, 20), f"Time: {current_time}", fill="white")  # Display time
            draw.text((10, 40), f"Date: {current_date}", fill="white")  # Display date
    
    return retry_display_operation(_display)

def display_next_adan_name_time(prayer_name, adan_time, remaining_time):
    """Display next prayer information on OLED with retry logic."""
    def _display():
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, outline="white", fill="black")
            draw.text((5, 10), f"Next Prayer: {prayer_name}", fill="white")  # Display time
            draw.text((5, 25), f"Prayer Time: {adan_time}", fill="white")
            draw.text((5, 40), f"Remaining: {remaining_time}", fill="white")
    
    return retry_display_operation(_display)

