"""
Psychopy middleware. Provides display / stimulus functionality for the experiment.
"""

from psychopy import visual, event, monitors, core, data

class Psypy:
    """
    Wrapper class for reusable psychopy activities
    Attributes
    ----------
    conf : dict
        Settings for psychopy. See config.psy
    mon : monitors.Monitor
        The psychopy active monitor configuration
    win : visual.Window
        The psychopy active window to display stimuli
    wait_keys : list
        Keys that will be waited for on psychopy stimuli
    """

    conf: dict
    mon: monitors.Monitor
    win: visual.Window
    wait_keys: list = ['space', 'escape']

    def __init__(self, conf: dict) -> None:
        self.conf = conf
        self.mon = self.prepare_monitor()
        self.win = self.get_window()

    def prepare_monitor(self) -> monitors.Monitor:
        """
        Set up psychopy monitor
        """

        mon = monitors.Monitor(self.conf.get('monitorName'))
        mon.setSizePix(self.conf.get('winSize'))
        mon.setWidth(self.conf.get('monitorWidth'))
        return mon

    def wait_for_key(self) -> list:
        """
        Just a reusable wrapper for the psychopy key event
        """

        # Only listen for keys we want
        key = event.waitKeys(keyList=self.wait_keys)
        # If key is esc, leave the experiment
        if 'escape' in key:
            core.quit()
        return key

    def get_window(self) -> visual.Window:
        """
        Return a window for drawing stimuli
        """

        return visual.Window(
            size=self.conf.get('windowSize'),
            fullscr=self.conf.get('fullScreen'),
            monitor=self.mon,
            color=self.conf.get('windowColor'))

    def display_text_message(self, txt: str, wait: bool = True) -> None:
        """
        Display psychopy message / instructions
        """

        msg = visual.TextStim(self.win, text=txt.strip(), color=self.conf.get('textColor'))
        msg.draw()
        self.win.flip()
        if wait:
            self.wait_for_key()

    def display_text_sequence(self, txt: str) -> list:
        """
        Display word by word text sequence
        """

        # Prepare timer
        stopwatch = core.Clock()
        sequence_data = []
        sequence = 1
        # Display the given text word by word
        for word in txt.split():
            # ignore blank / non-words
            word = word.strip()
            if word == '':
                continue
            # Prepare the word display
            msg = visual.TextStim(self.win, text=word, color=self.conf.get('textColor'))
            msg.draw()
            # Show the word
            self.win.flip()
            # Start timer
            stopwatch.reset()
            self.wait_for_key()
            time = stopwatch.getTime()
            # Collate data for this word
            sequence_data.append({
                'timestamp': data.getDateStr(format='%Y-%m-%d %H:%M:%S'),
                'word': word,
                'time': time,
                'sequence': sequence
            })
            sequence += 1
        return sequence_data