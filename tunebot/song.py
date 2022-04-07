import pafy

from util.log import Log


class Song:
    """The song object."""

    def __init__(self, url):
        """Initialize a song."""
        self._log = Log()
        self._video = None
        self._url = url
        self._title = 'Unknown'
        self._author = 'Unknown'
        self._thumb = 'Unknown'

    def resolve(self):
        """Try to resolve the url."""
        success = False

        try:
            self._video = pafy.new(self._url)
            self._url = self._video.getbestaudio().url
            self._title = self._video.title
            self._author = self._video.author
            self._thumb = self._video.bigthumb
            success = True
        except Exception as e:
            self._log.error(
                'An error occurred trying to resolve the following url:')
            self._log.no_prefix(self._url)
            self._log.no_prefix(e)

        return success

    def get_url(self):
        """Get this song's URL."""
        return self._url

    def get_title(self):
        """Get the title of the video this song was linked to."""
        return self._title

    def get_author(self):
        """Get the name of the channel that uploaded this song."""
        return self._author

    def get_thumb(self):
        """Get the url to the song's thumbnail image."""
        return self._thumb

    def __str__(self):
        """Represent the song as a string."""
        return f'{self._title} by {self._author}'
