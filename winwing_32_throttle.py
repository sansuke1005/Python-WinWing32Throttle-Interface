import hid

VID = 0x4098
PID = 0xB920

BASE_LCD1 =[0xF0, 0x00, 0x40, 0x38, 0x01, 0xB9, 0x00, 0x00, 0x02, 0x01, 0x00, 0x00, 0x49, 0x30, 0x17, 0x00, 0x00, 0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x01, 0xB9, 0x00, 0x00, 0x00, 0x00, 0x00]
BASE_LCD2 =[0xF0, 0x00, 0x41, 0x0E, 0x00, 0x03, 0x01, 0x00, 0x00, 0x49, 0x30, 0x17, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
BASE = [0x02, 0x01, 0xB9, 0x00, 0x00, 0x03, 0x49, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

DEV_THR = 0x10
DEV_PAC = 0x01

T_BACKLIGHT = 0x00
T_LCD       = 0x02
T_MAKER     = 0x02
T_FAULT1    = 0x03
T_FIRE1     = 0x04
T_FAULT2    = 0x05
T_FIRE2     = 0x06
T_VIB1      = 0x0E
T_VIB2      = 0x10

PLANE_INDEX = {
    "dot": 0,
    "G": 1,
    "F": 2,
    "E": 3,
    "D": 4,
    "C": 5,
    "B": 6,
    "A": 7,
}

SEG = {
    "0": "ABCDEF",
    "1": "BC",
    "2": "ABGED",
    "3": "ABGCD",
    "4": "FGBC",
    "5": "AFGCD",
    "6": "AFGECD",
    "7": "ABC",
    "8": "ABCDEFG",
    "9": "ABFGCD",
    "-": "G",
    " ": "",
    "R": "ABCEFG",
    "L": "FED"
}

PLANE_OFFSETS = [25,29,33,37,41,45,49,53]

def _pad64(pkt: list[int]) -> list[int]:
    return pkt + [0x00] * (64 - len(pkt))

def _u8(x: int) -> int:
    return max(0, min(255, int(x)))

def _bit(x) -> int:
    return 1 if int(x) else 0

def format_trim_lr(value: float) -> str:
    value = max(-20.0, min(20.0, float(value)))

    if value > 0:
        text = f"R{value:4.1f}"
    elif value < 0:
        text = f"L{abs(value):4.1f}"
    else:
        text = "  0.0"

    return text.ljust(6)[:6]

class WinWing32Throttle:
    def __init__(self, vid=VID, pid=PID):
        self.vid = vid
        self.pid = pid
        self.dev = hid.device()
        self.dev.open(vid, pid)

    def close(self):
        try:
            self.dev.close()
        except Exception:
            pass

    def _set_value(self, device: int, target: int, value: int):
        pkt = BASE.copy()
        pkt[1] = _u8(device)
        pkt[7] = _u8(target)
        pkt[8] = _u8(value)
        self.dev.write(_pad64(pkt))

    def set_thr_backlight(self, level: int):
        self._set_value(DEV_THR, T_BACKLIGHT, level)

    def set_pac_backlight(self, level: int):
        self._set_value(DEV_PAC, T_BACKLIGHT, level)
    
    def set_backlight(self, level: int):
        self.set_thr_backlight(level)
        self.set_pac_backlight(level)
    
    def set_lcd_brightness(self, level: int):
        self._set_value(DEV_PAC, T_LCD, level)

    def set_maker_brightness(self, level: int):
        self._set_value(DEV_THR, T_MAKER, level)

    def set_fault_light1(self, state: int):
        self._set_value(DEV_THR, T_FAULT1, _bit(state))
    
    def set_fault_light2(self, state: int):
        self._set_value(DEV_THR, T_FAULT2, _bit(state))

    def set_fire_light1(self, state: int):
        self._set_value(DEV_THR, T_FIRE1, _bit(state))

    def set_fire_light2(self, state: int):
        self._set_value(DEV_THR, T_FIRE2, _bit(state))

    def set_vibration1(self, level: int):
        self._set_value(DEV_THR, T_VIB1, level)

    def set_vibration2(self, level: int):
        self._set_value(DEV_THR, T_VIB2, level)

    
    def set_lcd(self, text):
        text = text.ljust(6)[:6]

        planes = [0]*8

        digit = 0
        i = 0
        while i < len(text) and digit < 6:
            ch = text[i]

            if ch == ".":
                if digit > 0:
                    planes[PLANE_INDEX["dot"]] |= (1 << (digit-1))
                i += 1
                continue

            for seg in SEG.get(ch, ""):
                planes[PLANE_INDEX[seg]] |= (1 << digit)

            digit += 1
            i += 1

        p1 = BASE_LCD1[:]

        for pi, mask in enumerate(planes):
            ofs = PLANE_OFFSETS[pi]
            p1[ofs] = mask

        self.dev.write(p1)
        self.dev.write(BASE_LCD2)
    
    def set_rudder_trim(self, value: float):
        self.set_lcd(format_trim_lr(value))
