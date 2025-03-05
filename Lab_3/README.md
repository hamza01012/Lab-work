### **Lab 3: Home Task Solution**
**IoT Fundamentals**  
**Instructor: Mr. Nasir Mahmood**  
**BSAI 6th - Department of Computer Science - NTU**  

---

## **Task 1: Displaying Temperature & Humidity on OLED**

### **Code to Display Temperature & Humidity on OLED (MicroPython)**
```python
from machine import Pin, I2C
import ssd1306
import dht
import time

# Initialize I2C for OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
display = ssd1306.SSD1306_I2C(128, 64, i2c)

# Initialize DHT11 Sensor
dht_pin = Pin(4, Pin.IN)
sensor = dht.DHT11(dht_pin)

while True:
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        display.fill(0)
        display.text("Temp: {}C".format(temp), 0, 0)
        display.text("Humidity: {}%".format(hum), 0, 10)
        display.show()
        
        time.sleep(2)
    except OSError as e:
        print("Failed to read sensor data")
```
### **Observations:**
- The OLED successfully displays temperature and humidity values.
- Emojis or symbols for temperature/humidity may not be supported directly.
- Blowing on the sensor causes a minor increase in humidity and temperature, confirming its sensitivity.

---

## **Task 2: Running the Code Without Interrupt**

### **Observations Before and After Interrupt:**
- Without interrupts, the microcontroller continuously polls the sensor, wasting CPU cycles.
- Before interrupt:
  - The code runs in a continuous loop.
  - The microcontroller is busy checking for changes even if none occur.
- After interrupt:
  - The microcontroller executes only when a condition is met (e.g., button press, sensor threshold).
  - Power consumption reduces, and processing efficiency improves.

---

## **Task 3: Understanding Debounce Issue**

### **What is a debounce issue and why do we get rid of it?**
- A debounce issue occurs when a mechanical switch or button generates multiple signals due to its internal contacts bouncing before settling.
- This can cause unintended multiple inputs (e.g., one button press registering multiple times).
- We eliminate debounce issues to ensure reliable and accurate input detection.

### **Applications where debounce issues can be threatening:**
- Medical devices: Incorrect input readings could be life-threatening.
- Keypad-based security systems: Multiple signals might cause authentication failures.
- Industrial automation: Unwanted multiple signals may cause machine malfunctions.
- Gaming controllers: Unintentional rapid button presses can affect gameplay.

### **Why does debounce occur?**
- **Mechanical contacts**: Physical switches take time to settle after being pressed.
- **Not a compiler error**: The compiler executes instructions as written.
- **Not a logical error**: The logic of the program is correct, but the hardware introduces noise.
- **Not due to a cheap microcontroller**: Even expensive microcontrollers experience debounce, as it’s a hardware phenomenon.

### **Common debounce solutions:**
- **Software-based**: Adding a small delay (e.g., `time.sleep(0.05)`) or using state change detection.
- **Hardware-based**: Using capacitors or Schmitt triggers to smooth signals.

---

## **Task 4: Why Do We Use Interrupts?**

### **Why do we use interrupts?**
- Interrupts allow a microcontroller to respond to real-time events without continuously checking (polling) for changes.
- They enhance efficiency by executing specific functions only when needed.

### **How does an interrupt lower processing cost?**
- **Reduces CPU usage**: Instead of checking inputs in a loop, the microcontroller can sleep or perform other tasks.
- **Faster response time**: The system reacts immediately to external triggers.
- **Efficient power management**: Useful in battery-powered applications where reducing unnecessary processing extends battery life.

### **Example Code Using Interrupt on ESP32 (MicroPython):**
```python
from machine import Pin
import time

button_pin = Pin(2, Pin.IN, Pin.PULL_UP)
button_pressed = False

def handle_interrupt(pin):
    global button_pressed
    button_pressed = True

button_pin.irq(trigger=Pin.IRQ_FALLING, handler=handle_interrupt)

while True:
    if button_pressed:
        print("Button Pressed!")
        button_pressed = False
    time.sleep(0.1)
```

### **Conclusion:**
- Interrupts optimize processing time by responding only when an event occurs.
- They are crucial for handling real-time input in embedded systems efficiently.

---

### **Final Remarks:**
This lab demonstrated practical applications of the DHT11 sensor, OLED display, debounce handling, and interrupts in microcontrollers. By implementing these concepts in MicroPython, students gain hands-on experience in building efficient and reliable IoT systems.

