import pafy

from util.log import Log


class Song:
    """The song object."""

    def __init__(self, url):
        """Initialize a song."""
        self._log = Log()
        self._url = url
        self._video = None
        self.title = 'Unknown'
        self.author = 'Unknown'
        self.thumb = 'Unknown'

    def resolve(self):
        """Try to resolve the url."""
        success = False

        try:
            self._video = pafy.new(self._url)
            self.title = self._video.title
            self.author = self._video.author
            self.thumb = self._video.thumb
            success = True
        except Exception as e:
            self._log.error(
                'An error occurred trying to resolve the following url:')
            self._log.no_prefix(self._url)
            self._log.no_prefix(e)

        return success

    def __str__(self):
        """Represent the song as a string."""
        return f'{self.title} by {self.author}'
