from simconnect_mobiflight import SimConnectMobiFlight
from mobiflight_variable_requests import MobiFlightVariableRequests
from winwing_32_throttle import WinWing32Throttle
from time import sleep


def map_clamped(x, in_min, in_max, out_min, out_max):
    if in_max == in_min:
        return int(out_min)
    x = max(min(x, in_max), in_min)
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def apply_rudder_trim(v):
    if v == 900001:
        ww.set_lcd("----")
    elif v == 900002:
        ww.set_lcd("    ")
    elif v == 988888:
        ww.set_lcd("8 8.8")
    else:
        ww.set_rudder_trim(v / 10)

sm = SimConnectMobiFlight()
vr = MobiFlightVariableRequests(sm)
vr.clear_sim_variables()

ww = WinWing32Throttle()

ww.set_lcd_brightness(255)

WATCH = {
    "rudder_trim": {
        "expr": "(L:FSL_PED_RUD_TRM)",
        "transform": lambda v: v,
        "apply": apply_rudder_trim,
    },
    "integ": {
        "expr": "(L:VC_PED_INTEG_LT_MainPnl_Knob)",
        "transform": lambda v: map_clamped(v, 3, 270, 0, 255),
        "apply": ww.set_backlight, 
    },
    "intlt": {
        "expr": "(L:VC_OVHD_INTLT_AnnLt_Switch)",
        "transform": lambda v: int(v != 0) * 100 + 155,
        "apply": ww.set_maker_brightness, 
    },
    "fire1": {
        "expr": "(L:VC_PED_ENGFIRE_1_LT_TOP)",
        "transform": lambda v: int(v != 0),
        "apply": ww.set_fire_light1,
    },
    "fire2": {
        "expr": "(L:VC_PED_ENGFIRE_2_LT_TOP)",
        "transform": lambda v: int(v != 0),
        "apply": ww.set_fire_light2,
    },
    "fault1": {
        "expr": "(L:VC_PED_ENGFIRE_1_LT_BOT)",
        "transform": lambda v: int(v != 0),
        "apply": ww.set_fault_light1,
    },
    "fault2": {
        "expr": "(L:VC_PED_ENGFIRE_2_LT_BOT)",
        "transform": lambda v: int(v != 0),
        "apply": ww.set_fault_light2,
    },
}

last = {k: None for k in WATCH}

try:
    while True:
        for name, spec in WATCH.items():
            try:
                raw = vr.get(spec["expr"])
                tv = spec["transform"](raw)

                if tv != last[name]:
                    spec["apply"](tv)
                    last[name] = tv

            except Exception as e:
                print(f"[{name}] error: {e}")

        sleep(0.1)

finally:
    ww.close()
