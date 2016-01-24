import glib
import dbus
from pprint import pprint
from dbus.mainloop.glib import DBusGMainLoop
import pdb
import logging
import argparse
import signal
import sys


from banner import banner
from metadata import Metadata
from recorder import Recorder
from pulse import get_sink_by_name
from functools import partial

def get_logger(debug=False):
    log = logging.getLogger("tIIsr")
    log.setLevel(logging.INFO)
    if debug:
        log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(name)s %(asctime)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)
    return log


def notifications(recorder, log, bus, message):
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


def get_encoder(enc):
    if enc == 'mp3':
        return "lame -r --vbr-new - {filename}"
    if enc == 'ogg':
        return "oggenc -b 192 -o {filename} --raw -"
    return enc


def get_ext(enc):
    if enc in ('mp3', 'ogg'):
        return enc
    return 'mp3'


def main(args, log):
    DBusGMainLoop(set_as_default=True)

    encoder = get_encoder(args.encoder)
    log.debug("Encoder set to: %s" % encoder)
    ext = args.extension if args.extension else get_ext(args.encoder)
    log.debug("Using extension: .%s" % ext)
    recorder = Recorder(log, get_sink_by_name(args.program), encoder, ext)
    message_filter = partial(notifications, recorder, log)

    bus = dbus.SessionBus()
    bus.add_match_string_non_blocking("interface='org.freedesktop.DBus.Properties'")
    bus.add_message_filter(message_filter)

    def signal_handler(signal, frame):
        log.info('Bye bye!')
        recorder.save()
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    mainloop = glib.MainLoop()
    try:
        mainloop.run()
    except KeyboardInterrupt:
        log.info('Shutting down')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='{}\nRip the Pulse output of certain programs'.format(banner),
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-e', '--encoder', default='mp3',
        help='Program used for encoding the stream. Valid values are ogg or ' +
        'mp3, but it can also be a command like: lame -r --vbr-new - {filename}'
    )

    parser.add_argument('-d', '--debug', action='store_true', default=False,
                        help='Enable debug logging')

    parser.add_argument('-p', '--program', required=True,
                        help='Record the output of this program, for example "vlc"')

    parser.add_argument('--extension', default=None, help="File extension")

    args = parser.parse_args()

    log = get_logger(args.debug)

    for line in banner.splitlines():
        if not line.strip(): continue
        log.info(line)

    log.info('tIIsr started, waiting for a song to start, press Ctrl-C to quit')
    main(args, log)
