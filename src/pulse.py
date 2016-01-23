import subprocess

def get_sink_input_by_name(name):
    """Returns the index of a sing given its binary name or None if no sink is
    found.

    """
    cmd = ("pacmd list-sink-inputs" +
           "| grep -B50 -i \"application.process.binary = \\\"%s\\\"\"" +
           "| grep index" + 
           "| tail -n1" +
           "| cut -f2 -d:" +
           "| tr -d \" \"") % name
    index = subprocess.check_output(cmd, shell=True).strip()
    try:
        return int(index)
    except ValueError:
        return None

if __name__ == '__main__':
    print get_sink_input_by_name('vlc')
