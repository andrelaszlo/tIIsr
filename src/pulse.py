import os
import subprocess
from subprocess import CalledProcessError

# This is how the redirection of sinks and sources are supposed to work
# All programs (sink inputs) are using the default sink to begin with:
#  +-------+    +----+
#  |Program|--->|Sink|
#  +-------+    +----+
# When we find the sink used by the program, then we can start recording from it.

def get_sink_by_name(name):
    """Returns the name of the sink used by a program (sink input)
    """
    cmd = (r'pacmd list-sink-inputs' +
           r'| grep -B50 "application.process.binary = \"%s\""' +
           r'| grep sink:' +
           r'| tail -n1' +
           r'| sed "s/^.*<\(.*\)>$/\\1/"') % name
    sink_name = subprocess.check_output(cmd, shell=True).strip()
    return sink_name if sink_name else None
