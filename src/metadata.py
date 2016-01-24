class Metadata:
    def __init__(self, metadata):
        self._metadata = metadata
        self.album = metadata.get('xesam:album', 'Unknown Album')
        self.artist = self._get_property('xesam:albumArtist')
        self.track = metadata.get('xesam:title', 'Unknown Album')
        self.track_number = int(metadata.get('xesam:trackNumber'))
        self.art = metadata.get('xesam:artUrl')
        self.url = metadata.get('xesam:url')
        self.rating = float(metadata.get('xesam:autoRating'))

    def _get_property(self, prop, default=None):
        return self._metadata.get(prop, default)[0]

    def download_thumbnail(self):
        filename = str(self).lower().replace(' ', '_').replace('#', 'track')
        response = requests.get(self.url)
        if not response.ok:
            return
        with open(os.path.join('.', filename)) as out:
            out.write(response.content)
        log.info('')

    def __str__(self):
        return "{} ({} #{}) - {}".format(self.artist, self.album, self.track_number, self.track)

    def as_filename(self):
        return "{}-{}-{}-{}".format(
            self.artist, self.album, self.track_number, self.track)
