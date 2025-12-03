import board
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.layers import Layers
from kmk.modules.encoder import EncoderHandler
from kmk.extensions.peg_oled_Display import Oled, OledDisplayMode, OledReactionType, OledData
from kmk.extensions.media_keys import MediaKeys

# Initialize keyboard
keyboard = KMKKeyboard()

# Initialize modules
layers = Layers()
encoder_handler = EncoderHandler()
media_keys = MediaKeys()

# Add modules to keyboard
keyboard.modules = [layers, encoder_handler]
keyboard.extensions = [media_keys]

# Define matrix pins - ACTUAL WIRING
# Rows: Pin 1 (GPIO26/A0), Pin 2 (GPIO27/A1), Pin 3 (GPIO28/A2)
# Columns: Pin 8 (GPIO1/RX), Pin 9 (GPIO2/SCK), Pin 10 (GPIO4/MISO)
keyboard.col_pins = (board.D1, board.D2, board.D4)  # Column 0, Column 1, Column 2
keyboard.row_pins = (board.D26, board.D27, board.D28)  # Row 0, Row 1, Row 2
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# Configure rotary encoder - ACTUAL WIRING
# A -> Pin 7 (GPIO0/TX), B -> Pin 4 (GPIO29/A3)
# Format: (pin_a, pin_b, button_pin, divisor)
encoder_handler.pins = ((board.D0, board.D29, None, False),)

# Configure OLED Display
# SDA -> GPIO6, SCL -> GPIO7
oled_ext = Oled(
    OledData(
        corner_one={0: OledReactionType.STATIC, 1: ["Layer"]},
        corner_two={
            0: OledReactionType.LAYER,
            1: ["Productivity", "Gaming", "Media", "Soundboard"]
        },
    ),
    toDisplay=OledDisplayMode.TXT,
    flip=False,
)
keyboard.extensions.append(oled_ext)

# Define custom macros for each mode
# Productivity macros
COPY = KC.LCTRL(KC.C)
PASTE = KC.LCTRL(KC.V)
CUT = KC.LCTRL(KC.X)
UNDO = KC.LCTRL(KC.Z)
SAVE = KC.LCTRL(KC.S)
SELECT_ALL = KC.LCTRL(KC.A)
FIND = KC.LCTRL(KC.F)
NEW_TAB = KC.LCTRL(KC.T)
CLOSE_TAB = KC.LCTRL(KC.W)

# Gaming macros
QUICK_SAVE = KC.F5
QUICK_LOAD = KC.F9
SCREENSHOT = KC.F12
INVENTORY = KC.TAB
MAP = KC.M
JUMP = KC.SPACE
CROUCH = KC.LCTRL
RELOAD = KC.R
INTERACT = KC.E

# Media macros
PLAY_PAUSE = KC.MEDIA_PLAY_PAUSE
NEXT_TRACK = KC.MEDIA_NEXT_TRACK
PREV_TRACK = KC.MEDIA_PREV_TRACK
VOL_DOWN = KC.MEDIA_VOLUME_DOWN
MUTE = KC.MEDIA_MUTE
VOL_UP = KC.MEDIA_VOLUME_UP
STOP = KC.MEDIA_STOP
CALC = KC.MACRO("calc")  # Opens calculator on Windows
BROWSER = KC.MACRO("Chrome")  # Opens Chrome
#those last 2 probably don't work but I am going to fix that once I can test the other stuff

# Discord Soundboard macros
# These trigger Discord's default soundboard keybinds (F13-F21)
# You'll need to assign these keys to your soundboard sounds in Discord settings
SOUND1 = KC.F13  
SOUND2 = KC.F14  
SOUND3 = KC.F15  
SOUND4 = KC.F16 
SOUND5 = KC.F17  
SOUND6 = KC.F18 
SOUND7 = KC.F19  
SOUND8 = KC.F20  
SOUND9 = KC.F21  

# Define keymap with 4 layers
# Each layer has 9 keys arranged in 3x3 matrix
keyboard.keymap = [
    # Layer 0: Productivity Mode
    [
        COPY,       PASTE,      CUT,        # Row 1: SW1, SW2, SW7
        UNDO,       SAVE,       SELECT_ALL, # Row 2: SW5, SW3, SW8
        FIND,       NEW_TAB,    CLOSE_TAB,  # Row 3: SW6, SW4, SW9
    ],
    # Layer 1: Gaming Mode
    [
        QUICK_SAVE, QUICK_LOAD, SCREENSHOT, # Row 1
        INVENTORY,  MAP,        JUMP,       # Row 2
        CROUCH,     RELOAD,     INTERACT,   # Row 3
    ],
    # Layer 2: Media Mode
    [
        PLAY_PAUSE, NEXT_TRACK, PREV_TRACK, # Row 1
        VOL_DOWN,   MUTE,       VOL_UP,     # Row 2
        STOP,       CALC,       BROWSER,    # Row 3
    ],
    # Layer 3: Discord Soundboard Mode
    [
        SOUND1,     SOUND2,     SOUND3,     # Row 1
        SOUND4,     SOUND5,     SOUND6,     # Row 2
        SOUND7,     SOUND8,     SOUND9,     # Row 3
    ],
]

# Configure encoder behavior per layer
# (Turn Left, Turn Right, Button Press)
encoder_handler.map = [
    # Layer 0: Productivity
    ((KC.TO(3), KC.TO(1), KC.NO),),  # Left->Layer 3, Right->Layer 1
    # Layer 1: Gaming
    ((KC.TO(0), KC.TO(2), KC.NO),),  # Left->Layer 0, Right->Layer 2
    # Layer 2: Media
    ((KC.TO(1), KC.TO(3), KC.NO),),  # Left->Layer 1, Right->Layer 3
    # Layer 3: Soundboard
    ((KC.TO(2), KC.TO(0), KC.NO),),  # Left->Layer 2, Right->Layer 0
]

if __name__ == '__main__':
    keyboard.go()
