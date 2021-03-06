import OpenSync
import time
import datetime
import os
from psychopy import prefs

import os 
dir_path = os.path.dirname(os.path.realpath(__file__))

DATA_DIR = "{}/data/".format(dir_path)
PREFS = {
    # Hardware / display configuration
    'audioLib': ['PTB', 'sounddevice', 'pyo', 'pygame'],
    'audioLatencyMode': 4, # critical
    'winType': ['pygame'],
    # Setting to True makes text sharp, but causes problems with the dialogue
    'highDPI': False,
    'windowSize': (3840, 2160),
    'monitorName': 'Blade13scaled',
    'monitorWidth': 55,
    'fullScreen': True,

    # UI settings, colors, etc.
    'windowColor': (1, 1, 1),
    'textColor': (-1, -1, -1),
}

prefs.hardware['audioLib'] = PREFS.get('audioLib')
prefs.general['winType'] = PREFS.get('winType')
prefs.hardware['highDPI'] = PREFS.get('highDPI')
prefs.saveUserPrefs()

# this needs to happen after prefs are set
from lib.psy import Psypy
from lib.psyparticipant import display_participant_dialogue

participant_id = display_participant_dialogue()

xrunner = Psypy(conf = PREFS)


# gonna go out on a limb here before even testing
# and assume int markers are faster than string markers
# as such, let's define some constants, we can always remove later.
STATUS_MARKER = "plaback_status" # this is required to be a string
STATUS_PLAYING = 1
STATUS_STOPPED = 2


print(OpenSync.OpenSync_path())

playStatusMarker = OpenSync.markers.marker(STATUS_MARKER)

EEG = OpenSync.sensors.EEG()
EEG.OpenBCI_Cyton(daisy=True, port="COM3")

OpenSync.record_data("{}session_{}.xdf".format(
  DATA_DIR,
  datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")))

time.sleep(5)


# playStatusMarker.stream_marker(STATUS_PLAYING)


OpenSync.stop_record()
