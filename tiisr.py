#!/bin/env python2

import glib
import dbus
from pprint import pprint
from dbus.mainloop.glib import DBusGMainLoop
import pdb
import requests
import logging
import argparse

from banner import banner
from metadata import Metadata
from recorder import Recorder

def get_logger():
    log = logging.getLogger("tIIsr")
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


log = get_logger()
recorder = Recorder(log)


def notifications(bus, message):
    try:
        if message.get_member() != "PropertiesChanged":
            return
    
        args = message.get_args_list()
        interface_name, changed_properties, invalidated_properties = args
    
        if str(interface_name) != "org.mpris.MediaPlayer2.Player":
            return
    
        track = Metadata(changed_properties.get('Metadata', {}))
    
        recorder.save()
    
        log.info("Now playing: %s" % track)
        recorder.start(track)
    except Exception as ex:
        log.exception("Something went wrong")


def main():
    DBusGMainLoop(set_as_default=True)

    bus = dbus.SessionBus()
    bus.add_match_string_non_blocking("interface='org.freedesktop.DBus.Properties'")
    bus.add_message_filter(notifications)

    mainloop = glib.MainLoop()
    mainloop.run()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='{}\nRip the Pulse output of certain programs'.format(banner),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-e', '--encoder',
                        default='mp3',
                        help='Program used for encoding the stream (ogg or mp3)')
    args = parser.parse_args()

    for line in banner.splitlines():
        if not line.strip(): continue
        log.info(line)

    log.info('tIIsr started, waiting for a song to start')
    main()
