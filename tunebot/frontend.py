import vlc
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.image import AsyncImage
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from tunebot.backend import BackEnd


# Constants
TITLE = 'Tunebot'
DISPLAY_SIZE = (1920, 1080)
COL_BG = (1, 1, 1, 1)
COL_TITLE = (0, 0.5, 0.5, 1)
COL_TEXT = (0.25, 0, 1, 1)
COL_BUTTON = (0.8, 0.8, 0.8, 1)
FONT_TITLE = 'font/Rodina_Nesselova.otf'
FONT_UI = 'font/OpenSans-Regular.ttf'
DEFAULT_THUMB = 'https://www.pngkit.com/png/full/3-38748_musical-notes-png.png'


class FrontEnd(App):
    """The frontend application."""

    # The frontend singleton
    FRONTEND = None

    class Application(GridLayout):

        class QueuePanel(GridLayout):
            """The queue panel, render title and upcoming tracks."""

            def __init__(self, parent, **kwargs):
                """Instantiate the queue panel."""
                super(FrontEnd.Application.QueuePanel, self).__init__(**kwargs)
                self._parent = parent
                self.cols = 1
                self.rows = 11
                self.size_hint = (0.25, 1)

            def refresh(self):
                """Load the queue from the playlist."""
                self.clear_widgets()

                # Readd the title widget
                self.add_widget(
                    Label(text=TITLE, font_size='48sp', font_name=FONT_TITLE, color=COL_TITLE))

                # Add the queue
                for song in BackEnd.BACKEND.get_playlist():
                    self.add_widget(
                        Label(text=song.get_title(), font_name=FONT_UI, color=COL_TEXT))

        class ControlPanel(GridLayout):
            """The controls and 'now playing' interface."""

            def __init__(self, parent, **kwargs):
                """Instantiate the control panel."""
                super(FrontEnd.Application.ControlPanel,
                      self).__init__(**kwargs)
                self._parent = parent
                self.cols = 3
                self.rows = 3

            def refresh(self):
                """Refresh the control panel. Requires full rebuild"""
                self.clear_widgets()
                now_playing = BackEnd.BACKEND.get_now_playing()

                # Top row
                # =======

                # Refresh playlist
                button_refresh = Button(
                    text='Refresh', font_name=FONT_UI, color=COL_BUTTON
                )
                button_refresh.bind(
                    on_press=self._parent.on_button_refresh
                )
                self.add_widget(button_refresh)

                # Shuffle playlist
                button_shuffle = Button(
                    text='Shuffle', font_name=FONT_UI, color=COL_BUTTON
                )
                button_shuffle.bind(
                    on_press=self._parent.on_button_shuffle
                )
                self.add_widget(button_shuffle)

                # Close the app
                button_close = Button(
                    text='Exit', font_name=FONT_UI, color=COL_BUTTON
                )
                button_close.bind(
                    on_press=self._parent.on_button_close
                )
                self.add_widget(button_close)

                # Middle row
                # ==========

                # Display play/pause status
                self._label_play_pause = Label(
                    text='Paused' if self._parent._paused else 'Playing',
                    font_name=FONT_UI, color=COL_TEXT
                )
                self.add_widget(self._label_play_pause)

                # Display current track
                self._label_now_playing = Label(
                    text='None' if now_playing is None else now_playing.get_title(),
                    font_name=FONT_UI, color=COL_TEXT
                )
                self.add_widget(self._label_now_playing)

                # Display thumbnail image
                self._thumb_view = AsyncImage(
                    source=DEFAULT_THUMB if now_playing is None else now_playing.get_thumb()
                )
                self._thumb_view.nocache = True
                # self._thumb_view.allow_stretch = True
                self.add_widget(self._thumb_view)

                # Bottom row
                # ==========

                # Previous song
                button_prev_song = Button(
                    text='Previous', font_name=FONT_UI, color=COL_BUTTON
                )
                button_prev_song.bind(
                    on_press=self._parent.on_button_prev_song
                )
                self.add_widget(button_prev_song)

                # Play/pause
                button_play_pause = Button(
                    text='Play/Pause', font_name=FONT_UI, color=COL_BUTTON
                )
                button_play_pause.bind(
                    on_press=self._parent.on_button_play_pause
                )
                self.add_widget(button_play_pause)

                # Next song
                button_next_song = Button(
                    text='Next', font_name=FONT_UI, color=COL_BUTTON
                )
                button_next_song.bind(
                    on_press=self._parent.on_button_next_song
                )
                self.add_widget(button_next_song)

        def __init__(self, **kwargs):
            """Instantiate the frontend."""
            super(FrontEnd.Application, self).__init__(**kwargs)
            self.cols = 2
            self.rows = 1

            self._initialized = False
            self._paused = False
            self._vlc_instance = vlc.Instance()
            self._player = self._vlc_instance.media_player_new()

            self._queue_panel = FrontEnd.Application.QueuePanel(self)
            self._control_panel = FrontEnd.Application.ControlPanel(self)
            self.add_widget(self._queue_panel)
            self.add_widget(self._control_panel)

            Window.size = DISPLAY_SIZE
            Window.clearcolor = COL_BG
            # Window.borderless = True
            # Window.fullscreen = 'auto'

        def on_button_refresh(self, _):
            """Refresh button callback.

            Tells the backend to refresh the main playlist.
            Backend tells the frontend thread to update the GUI when refreshing is done.
            """
            BackEnd.BACKEND.refresh()

        def on_button_shuffle(self, _):
            """Shuffle button callback."""
            BackEnd.BACKEND.shuffle()
            self.refresh(None)

        def on_button_close(self, _):
            """Close button callback."""
            self.stop()
            FrontEnd.FRONTEND.stop()

        def on_button_prev_song(self, _):
            """Previous song button callback."""
            BackEnd.BACKEND.previous_song()
            self.refresh(None)
            self.play()

        def on_button_next_song(self, _):
            """Next song button callback."""
            BackEnd.BACKEND.next_song()
            self.refresh(None)
            self.play()

        def on_button_play_pause(self, _):
            """Play/pause button callback."""
            self._paused = not self._paused
            self.refresh(None)

            if self._paused:
                self._player.pause()
            else:
                self._player.play()

        def play(self):
            """Start playing the current song."""
            song = BackEnd.BACKEND.get_now_playing()

            if song is not None:
                self._player.stop()
                media = self._vlc_instance.media_new(song.get_url())
                media.get_mrl()
                self._player.set_media(media)
                self._player.play()

        def stop(self):
            """Stop playing music."""
            self._player.stop()

        def refresh(self, _):
            """Refresh the frontend."""
            self._queue_panel.refresh()
            self._control_panel.refresh()

            # On startup, start playing the first song after refresh
            if not self._initialized:
                self._initialized = True
                self.play()

    def build(self):
        """Initialize the controller frontend."""
        application = FrontEnd.Application()
        BackEnd.BACKEND = BackEnd(application.refresh)
        Clock.schedule_interval(BackEnd.BACKEND.refresh,
                                BackEnd.BACKEND.get_refresh_interval_sec())
        return application
