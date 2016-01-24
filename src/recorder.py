import re
import os
import subprocess
from signal import SIGINT

class Recorder:
    def __init__(self, logger, sink, encoder, extension):
        self.log = logger
        self._sink = sink
        self._metadata = "Unknown song"
        self._recording_process = None
        self._extension = extension
        self._encoder = encoder

    def start(self, metadata):
        self._metadata = metadata
        filename = self.filename(metadata)
        self.log.info('Recording started, saving to %s' % filename)
        self._recording_process = self._record(filename)

    def _record(self, filename):
        template = "parec -d {sink}.monitor | %s" % self._encoder
        cmd = template.format(sink=self._sink, filename=filename)
        with open(os.devnull, 'wb') as devnull:
            # Set process group, see http://stackoverflow.com/a/4791612/98057
            process = subprocess.Popen(
                cmd, shell=True, stdout=devnull, stderr=devnull,
                preexec_fn=os.setsid) 
            self.log.debug('Recording started in process %s' % process.pid)
            return process

    def save(self):
        """Stop the current recording and save the file"""
        proc = self._recording_process
        if not proc:
            return
        self.log.debug('Stopping recording process %s' % proc.pid)
        os.killpg(os.getpgid(proc.pid), SIGINT)
        self.log.info('Saving recording to "%s"' % self.filename(self._metadata))

    def filename(self, metadata):
        name = "".join(re.findall("[A-Za-z0-9\- ]+", metadata.as_filename()))
        name = name.replace(' ', '_')
        name += "." + self._extension
        name = name.lower()
        return name
