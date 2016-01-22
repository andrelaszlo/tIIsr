import re

class Recorder:
    def __init__(self, logger):
        self.log = logger
        self._recording = False
        self._metadata = "Unknown song"

    def start(self, metadata):
        self._recording = True
        self._metadata = metadata
        self.log.info('Recording started')

    def save(self):
        if not self._recording: return
        self.log.info('Saving recording to "%s"' % self.filename(self._metadata))

    def filename(self, metadata):
        return "".join(re.findall("[A-Za-z0-9\- ]+", str(metadata))) + ".mp3"
