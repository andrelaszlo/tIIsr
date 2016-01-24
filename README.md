```
████████╗████╗████╗███████╗██████╗
╚══██╔══╝╚██╔╝╚██╔╝██╔════╝██╔══██╗
   ██║    ██║  ██║ ███████╗██████╔╝
   ██║    ██║  ██║ ╚════██║██╔══██╗
   ██║   ████╗████╗███████║██║  ██║
   ╚═╝   ╚═══╝╚═══╝╚══════╝╚═╝  ╚═╝
```

[![asciicast](https://asciinema.org/a/26tb9uqv5h42611txkxm8chaw.png)](https://asciinema.org/a/26tb9uqv5h42611txkxm8chaw)

Rips the audio output of a media player and encodes the output as mp3 or ogg
(other formats are supported) and switches to a new file when the media player
changes song. The media player needs to send updates over D-Bus on the
`org.mpris.MediaPlayer2.Player` interface.

# Getting started

* Clone the repo
* Install the requirements
* Start ./tIIsr

# Requirements

The program requires the following:

* Python 2
* PulseAudio
* ogg, flac or mp3 encoder
* D-Bus

System packages (Arch Linux):

* extra/python-dbus
* extra/python2-gobject2
* extra/vorbis-tools (ogg)
* extra/lame (mp3)
* extra/flac (flac)

# Todo

* Testing
* Write tests (hehe)
* ID3-tagging

# Thanks to

* senzaroz, for idea (tisr, version 1) and support :)