from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

from tunebot.backend import BackEnd


# Constants
TITLE = 'Tunebot'
DISPLAY_SIZE = (1920, 1080)
COL_BG = (1, 1, 1, 1)
COL_TITLE = (0, 0.5, 0.5, 1)
COL_TEXT = (0.25, 0, 1, 1)
COL_BUTTON = (0)
FONT_TITLE = 'data/font/Rodina_Nesselova.otf'
FONT_UI = 'data/font/OpenSans-Regular.ttf'


class FrontEnd(App):
    """The frontend application."""

    # The frontend singleton
    FRONTEND = None

    class MainPanel(GridLayout):

        class QueuePanel(GridLayout):
            """The queue panel, render title and upcoming tracks."""

            def __init__(self, parent, **kwargs):
                """Instantiate the queue panel."""
                super(FrontEnd.MainPanel.QueuePanel, self).__init__(**kwargs)
                self._parent = parent
                self.cols = 1
                self.rows = 11
                self.size_hint = (0.25, 1)

            def refresh_queue(self, _):
                """Load the queue from the playlist."""
                self.clear_widgets()

                # Readd the title widget
                self.add_widget(
                    Label(text=TITLE, font_size='48sp', font_name=FONT_TITLE, color=COL_TITLE))

                # Add the queue
                for song in BackEnd.BACKEND.playlist:
                    self.add_widget(
                        Label(text=song.title, font_name=FONT_UI, color=COL_TEXT))

        class ControlPanel(GridLayout):
            """The controls and 'now playing' interface."""

            def __init__(self, parent, **kwargs):
                """Instantiate the control panel."""
                super(FrontEnd.MainPanel.ControlPanel,
                      self).__init__(**kwargs)
                self._parent = parent
                self.cols = 3
                self.rows = 2

                button_refresh = Button(text='Refresh')
                button_refresh.bind(
                    on_press=self._parent.on_button_refresh)
                self.add_widget(button_refresh)

                label_now_playing = Label(
                    text='Now Playing', font_name=FONT_UI, color=COL_TEXT)
                self.add_widget(label_now_playing)

                button_close = Button(text='Exit')
                button_close.bind(
                    on_press=self._parent.on_button_close)
                self.add_widget(button_close)

                button_prev_song = Button(text='Previous')
                button_prev_song.bind(
                    on_press=self._parent.on_button_prev_song)
                self.add_widget(button_prev_song)

                button_play_pause = Button(text='Play/Pause')
                button_play_pause.bind(
                    on_press=self._parent.on_button_play_pause)
                self.add_widget(button_play_pause)

                button_next_song = Button(text='Next')
                button_next_song.bind(
                    on_press=self._parent.on_button_next_song)
                self.add_widget(button_next_song)

        def __init__(self, **kwargs):
            """Instantiate the frontend."""
            super(FrontEnd.MainPanel, self).__init__(**kwargs)
            self.cols = 2
            self.rows = 1

            self.queue_panel = FrontEnd.MainPanel.QueuePanel(self)
            self.control_panel = FrontEnd.MainPanel.ControlPanel(self)
            self.add_widget(self.queue_panel)
            self.add_widget(self.control_panel)

            Window.size = DISPLAY_SIZE
            Window.clearcolor = COL_BG
            Window.borderless = True

        def on_button_refresh(self, _):
            """Refresh button callback."""
            BackEnd.BACKEND.refresh()

        def on_button_close(self, _):
            """Close button callback."""
            FrontEnd.FRONTEND.stop()

        def on_button_prev_song(self, _):
            """Previous song button callback."""
            pass

        def on_button_next_song(self, _):
            """Next song button callback."""
            pass

        def on_button_play_pause(self, _):
            """Play/pause button callback."""
            pass

    def build(self):
        """Initialize the controller frontend."""
        application = FrontEnd.MainPanel()
        BackEnd.BACKEND = BackEnd(application.queue_panel.refresh_queue)
        Clock.schedule_interval(BackEnd.BACKEND.refresh,
                                BackEnd.BACKEND.get_refresh_interval_sec())
        return application
