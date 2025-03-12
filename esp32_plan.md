# Running Waze Home CLI on ESP32 with MicroPython

After analyzing this repository, I can see that it's a CLI application that uses the WazeRouteCalculator package to fetch route information between locations (primarily home and work). Running this on an ESP32 with MicroPython would require significant changes due to the differences between standard Python and MicroPython, as well as the hardware constraints of the ESP32.

## Key Challenges

1. **MicroPython Limitations**: MicroPython is a subset of Python designed for microcontrollers with limited resources.

2. **Missing Dependencies**: Several packages you're using aren't available in MicroPython:
   - WazeRouteCalculator
   - click (for CLI)
   - rich (for formatted console output)
   - python-dotenv

3. **Resource Constraints**: ESP32 has limited RAM (typically 320KB-520KB) and processing power.

4. **No Command Line Interface**: ESP32 doesn't have a traditional CLI environment.

## Required Changes

### 1. Simplify the Architecture

You'll need to redesign the application to work as a standalone program rather than a CLI:

```python
# Simple ESP32 version
import network
import urequests as requests
import time
import json

# Connect to WiFi
def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            time.sleep(1)
    print('Network config:', wlan.ifconfig())
```

### 2. Replace WazeRouteCalculator with Direct API Calls

Since WazeRouteCalculator isn't available for MicroPython, you'll need to implement a simplified version of the API calls:

```python
def get_waze_route(origin, destination):
    # Simplified coordinates for your common locations
    locations = {
        "home": {"lat": -31.8941, "lon": 115.7586},
        "work": {"lat": -31.9523, "lon": 115.8613}
    }
    
    # Get coordinates
    origin_coords = locations.get(origin, None)
    dest_coords = locations.get(destination, None)
    
    if not origin_coords or not dest_coords:
        return {"error": "Unknown location"}
    
    # Simplified Waze API call
    try:
        url = "https://www.waze.com/row-RoutingManager/routingRequest"
        params = {
            "from": f"x:{origin_coords['lon']} y:{origin_coords['lat']}",
            "to": f"x:{dest_coords['lon']} y:{dest_coords['lat']}",
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "true",
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": 1,
            "options": "AVOID_TRAILS:t,AVOID_TOLL_ROADS:f,AVOID_FERRIES:f"
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "referer": "https://www.waze.com/"
        }
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API error: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
```

### 3. Implement a Simple Output Mechanism

Instead of using rich for formatted output, use simple print statements or connect to an LCD display:

```python
def display_route_info(route_data):
    if "error" in route_data:
        print("Error:", route_data["error"])
        return
    
    if "alternatives" in route_data and route_data["alternatives"]:
        route = route_data["alternatives"][0]["response"]
        print("Route Information:")
        print(f"Time: {route['totalSeconds'] // 60} minutes")
        print(f"Distance: {route['totalLength'] / 1000:.1f} km")
        
        # For LCD display
        # lcd.clear()
        # lcd.write(f"Time: {route['totalSeconds'] // 60}min")
        # lcd.move_to(0, 1)
        # lcd.write(f"Dist: {route['totalLength'] / 1000:.1f}km")
```

### 4. Create a Simple User Interface

You could use buttons on the ESP32 to trigger different routes:

```python
from machine import Pin
import time

# Setup buttons
home_to_work_btn = Pin(12, Pin.IN, Pin.PULL_UP)
work_to_home_btn = Pin(14, Pin.IN, Pin.PULL_UP)

# Main loop
def main():
    # Connect to WiFi
    connect_wifi("your_ssid", "your_password")
    
    while True:
        if home_to_work_btn.value() == 0:  # Button pressed
            print("Getting route from home to work...")
            route_data = get_waze_route("home", "work")
            display_route_info(route_data)
            time.sleep(0.5)  # Debounce
            
        if work_to_home_btn.value() == 0:  # Button pressed
            print("Getting route from work to home...")
            route_data = get_waze_route("work", "home")
            display_route_info(route_data)
            time.sleep(0.5)  # Debounce
            
        time.sleep(0.1)  # Small delay in main loop
```

### 5. Optimize Memory Usage

MicroPython has limited memory, so you'll need to optimize:

- Use simpler data structures
- Process API responses in chunks
- Avoid storing large objects in memory
- Use garbage collection when needed

```python
import gc

# After processing large responses
gc.collect()
```

## Hardware Requirements

To implement this on an ESP32, you would need:

1. **ESP32 Development Board**: Any ESP32 board with sufficient memory (preferably with at least 4MB flash)

2. **Input Method**: 
   - Buttons for selecting routes
   - Or a small keypad/touchscreen

3. **Output Method**:
   - LCD display (I2C or SPI interface)
   - Or LED indicators for simple status

4. **Power Supply**: USB power or battery with voltage regulator

## Example Implementation

Here's a simplified example of how your application might look on an ESP32:

```python
import network
import urequests as requests
import time
import json
import gc
from machine import Pin, I2C
import ssd1306  # For OLED display

# WiFi credentials
WIFI_SSID = "your_wifi_ssid"
WIFI_PASSWORD = "your_wifi_password"

# Locations
LOCATIONS = {
    "home": {"lat": -31.8941, "lon": 115.7586, "name": "91 Abbett St"},
    "work": {"lat": -31.9523, "lon": 115.8613, "name": "11 Mount St"}
}

# Setup hardware
i2c = I2C(scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
home_to_work_btn = Pin(12, Pin.IN, Pin.PULL_UP)
work_to_home_btn = Pin(14, Pin.IN, Pin.PULL_UP)

# Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        display.fill(0)
        display.text("Connecting to", 0, 0)
        display.text("WiFi...", 0, 10)
        display.show()
        
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        timeout = 0
        while not wlan.isconnected() and timeout < 10:
            time.sleep(1)
            timeout += 1
    
    if wlan.isconnected():
        display.fill(0)
        display.text("WiFi Connected", 0, 0)
        display.text(wlan.ifconfig()[0], 0, 10)
        display.show()
        time.sleep(2)
        return True
    else:
        display.fill(0)
        display.text("WiFi Failed", 0, 0)
        display.show()
        return False

# Get route from Waze
def get_route(origin, destination):
    origin_data = LOCATIONS.get(origin)
    dest_data = LOCATIONS.get(destination)
    
    if not origin_data or not dest_data:
        return None
    
    display.fill(0)
    display.text("Getting route...", 0, 0)
    display.text(f"From: {origin_data['name']}", 0, 10)
    display.text(f"To: {dest_data['name']}", 0, 20)
    display.show()
    
    try:
        url = "https://www.waze.com/row-RoutingManager/routingRequest"
        params = {
            "from": f"x:{origin_data['lon']} y:{origin_data['lat']}",
            "to": f"x:{dest_data['lon']} y:{dest_data['lat']}",
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "false",  # Save bandwidth
            "returnInstructions": "true",
            "timeout": 60000,
            "nPaths": 1
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0",
            "referer": "https://www.waze.com/"
        }
        
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            result = response.json()
            response.close()
            gc.collect()  # Free memory
            return result
        else:
            response.close()
            return None
    except Exception as e:
        display.fill(0)
        display.text("Error:", 0, 0)
        display.text(str(e)[:16], 0, 10)
        display.text(str(e)[16:32], 0, 20)
        display.show()
        time.sleep(3)
        return None

# Display route information
def display_route_info(route_data):
    if not route_data or "alternatives" not in route_data or not route_data["alternatives"]:
        display.fill(0)
        display.text("No route found", 0, 0)
        display.show()
        return
    
    try:
        route = route_data["alternatives"][0]["response"]
        
        # Calculate time and distance
        time_min = route.get("totalSeconds", 0) // 60
        distance_km = route.get("totalLength", 0) / 1000
        
        # Display information
        display.fill(0)
        display.text("Route Info:", 0, 0)
        display.text(f"Time: {time_min} min", 0, 15)
        display.text(f"Dist: {distance_km:.1f} km", 0, 25)
        
        # Traffic condition
        if "routeType" in route:
            if route["routeType"] == "SLOW":
                traffic = "Heavy traffic"
            elif route["routeType"] == "MODERATE":
                traffic = "Moderate traffic"
            else:
                traffic = "Light traffic"
            display.text(traffic, 0, 40)
        
        display.show()
    except Exception as e:
        display.fill(0)
        display.text("Error parsing", 0, 0)
        display.text("route data", 0, 10)
        display.show()

# Main function
def main():
    if not connect_wifi():
        return
    
    display.fill(0)
    display.text("Waze Route", 0, 0)
    display.text("Calculator", 0, 10)
    display.text("Press button:", 0, 30)
    display.text("1: Home->Work", 0, 40)
    display.text("2: Work->Home", 0, 50)
    display.show()
    
    while True:
        if home_to_work_btn.value() == 0:  # Button pressed
            route_data = get_route("home", "work")
            if route_data:
                display_route_info(route_data)
            time.sleep(0.5)  # Debounce
            
        if work_to_home_btn.value() == 0:  # Button pressed
            route_data = get_route("work", "home")
            if route_data:
                display_route_info(route_data)
            time.sleep(0.5)  # Debounce
            
        time.sleep(0.1)  # Small delay in main loop

# Run the program
if __name__ == "__main__":
    main()
```

## Conclusion

Converting your Waze Home CLI to run on an ESP32 with MicroPython requires:

1. **Reimplementing the core functionality** without relying on packages not available in MicroPython
2. **Creating a hardware interface** with buttons and a display instead of a CLI
3. **Optimizing for limited resources** by simplifying data structures and reducing memory usage
4. **Handling network connectivity** in a more robust way for an embedded device
5. **Implementing error handling** appropriate for a device that runs continuously

This is a significant redesign of your application, but it would allow you to create a dedicated "Waze commute time" device that could be mounted in your home or car to quickly check route times without needing a computer or smartphone. 