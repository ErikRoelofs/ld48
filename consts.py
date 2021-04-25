# sizes
WIDTH = 200
HEIGHT = 1000
SPACE_TO_SURFACE_DEPTH = 200
NOTCH_STEP = 100

SYSTEM_SIZE = 130
SYSTEM_PANEL_GAP = 10


# colors
BACKGROUND_SEA_START = (0, 157, 196)
BACKGROUND_SEA_END = (0, 0, 0)
SPACESHIP_COLOR_START = (128, 128, 128)
SPACESHIP_COLOR_END = (25, 25, 25)
NOTCH_COLOR = (255, 255, 255)
PANEL_COLOR = (70, 70, 70)

POWER_PLANT_COLOR = (22, 244, 20)
POWER_PLANT_UNUSED = (0, 0, 0)
POWER_PLANT_CHARGING = (128, 105, 0)
POWER_PLANT_OVERLOAD = (255, 0, 0)
BATTERY_COLOR = (255, 211, 0)
BATTERY_EMPTY = (0, 0, 0)
BATTERY_FLASH = (255, 0, 0)

OVERHEAT_END_COLOR = (255, 0, 0)
GOOD_TEMPERATURE_COLOR = (0, 255, 0)
FREEZING_END_COLOR = (0, 0, 255)

SONAR_COLOR = (255, 0, 0)

DAMAGE_COLORS = []
for i in range(0, 255, 5):
    DAMAGE_COLORS.append((i, i, i))

# speeds
FREEFALL_SPEED = 100
WATERBRAKE_SPEED = 900
POWER_ON_SPEED = 10
SONAR_SPEED = 300


# screens
ALTIMETER_SCREEN = 1
SYSTEM_CONTROLS_SCREEN = 2
POWER_CONTROLS_SCREEN = 3

# stats
MAX_ENGINE_THRUST = 100
ENGINE_SPEED_CHANGE = 50
MAX_BATTERY_CAPACITY = 10000
MAX_POWER_PRODUCTION = 400
MAX_POWER_PRODUCTION_LOSS_PERCENTAGE = 0.8

MAX_CLIMATE_CONTROL_CORRECT = 30

MAX_TEMPERATURE = 600
SUB_OVERHEAT_TRESHOLD = 500
IDEAL_TEMPERATURE = 300
SUB_FREEZING_TRESHOLD = 100
MIN_TEMPERATURE = 0

SUB_TEMPERATURE_CAPTURE = 0.2
AUDIO_QUALITY_DROPOFF = 1/10000

BIOME_EFFECT_DISTANCE = 200
SONAR_CHARGE_TIME = 3
SONAR_REVEAL_TIME = 0.5


# sounds
SOUND_SPLASH = 1
SOUND_RELEASE = 2
SOUND_ENGINE = 3
SOUND_IMPACT_RANDOM = 4
SOUND_AMBIENT = 5
SOUND_HOTSPOT = 6
SOUND_COLDSPOT = 7
SOUND_SONAR = 8
SOUND_WEIRD1 = 9
SOUND_WEIRD2 = 10

SOUND_DRAGON = 11
SOUND_CRAB = 12
SOUND_COW = 13
