"""
Display the dialogue for the psychopy participant ID
This is seperated from the `psy.py` to avoid a fullscreen
window covering the dialogue box.
"""
from psychopy import gui, core

def display_participant_dialogue() -> list:
    """
    Show participant information dialogue box
    """
    participant = None
    #pylint: disable=unsubscriptable-object
    # Only accept the ID if it is numeric
    while not isinstance(participant, list) or not participant[0].isnumeric():
        #pylint: enable=unsubscriptable-object
        # Standard psychopy dialogue box
        dlg = gui.Dlg(title="Please enter participant information")
        dlg.addField(label='ID (Numeric only)')
        participant = dlg.show()
        # Quit if cancel button on dialogue is pressed
        if participant is None:
            core.quit()
    return participant