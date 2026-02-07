# Python WinWing32Throttle Interface

## ⚠️ Important Notice

This program is designed for output to the controller only (LCD, lights, vibration).
It does NOT handle any input from the controller.

Do NOT run this program together with SimAppPro or MobiFlight.
Running multiple programs that access the controller at the same time may cause conflicts or unstable behavior.

## Overview

This project allows you to easily control the backlight, rudder trim display, and vibration motors of the WinWing URSA MINOR 32 Throttle Metal / 32 PAC Metal using Python.

By adapting this program, the controller can be integrated with a wide range of aircraft and customized for different simulator setups. 

## Reference

### Class: `WinWing32Throttle`

The `WinWing32Throttle` class provides a simple Python interface for controlling output features of the **WinWing URSA MINOR 32 Throttle Metal / 32 PAC Metal** via HID communication.

---

### Backlight Control

### `set_thr_backlight(level: int)`

Sets the backlight brightness of the throttle unit.

**Parameters**

* `level` — Brightness value (typically 0–255)

---

### `set_pac_backlight(level: int)`

Sets the backlight brightness of the PAC unit.

**Parameters**

* `level` — Brightness value (typically 0–255)

---

### `set_backlight(level: int)`

Sets the backlight brightness of both throttle and PAC units.

**Parameters**

* `level` — Brightness value (typically 0–255)

---

### `set_lcd_brightness(level: int)`

Adjusts the LCD brightness on the PAC unit.

**Parameters**

* `level` — Brightness value (typically 0–255)

---

## Maker Lights

### `set_fault_light1(state: int | bool)`

Turns FAULT light 1 on or off.

### `set_fault_light2(state: int | bool)`

Turns FAULT light 2 on or off.

### `set_fire_light1(state: int | bool)`

Turns FIRE light 1 on or off.

### `set_fire_light2(state: int | bool)`

Turns FIRE light 2 on or off.

**Parameters (for all above)**

* `state` — 0/1 or boolean value
  (any non-zero value is treated as ON)

---

## Vibration Motors

### `set_vibration1(level: int)`

Sets the intensity of vibration motor 1.

### `set_vibration2(level: int)`

Sets the intensity of vibration motor 2.

**Parameters (for both)**

* `level` — Intensity value (typically 0–255)

---

## LCD Display

### `set_lcd(text: str)`

Displays text on the 7-segment style LCD

**Parameters**

* `text` — String to display

**Supported characters**

* Digits: `0–9`
* Symbols: `-`, `.`, space
* Letters: `R`, `L`

**Dot behavior**

* A dot (`.`) applies to the previous digit.
* A leading dot is ignored.

**Notes**

* Unsupported characters are displayed as blank segments.

---

### `set_rudder_trim(value: float)`

Formats and displays a rudder trim value on the LCD.

**Parameters**

* `value` — Rudder trim value

**Behavior**

* The value is clamped to **−20.0 to +20.0**
* Automatically formats left/right trim indication

**Display format**

* Positive value → right trim (`RXX.X`)
* Negative value → left trim (`LXX.X`)
* Zero → only number (`  0.0`)



### `close()`

Closes the HID device connection.

---

## example_FSLABS.py

This example script is designed for **MSFS FSLabs A321**.

To run the example, you must copy the following files from:

[MSFSPythonSimConnectMobiFlightExtension](https://github.com/Koseng/MSFSPythonSimConnectMobiFlightExtension)

* `mobiflight_variable_requests.py`
* `simconnect_mobiflight.py`
