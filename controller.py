from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout


# Constants
TITLE = 'Tunebot'
DISPLAY_SIZE = (1920, 1080)
COL_BG = (1, 1, 1, 1)
COL_TITLE = (0, 0.5, 0.5, 1)
COL_TEXT = (0.25, 0, 1, 1)
COL_BUTTON = (0)
FONT_TITLE = 'font/Rodina_Nesselova.otf'
FONT_UI = 'font/OpenSans-Regular.ttf'


class ControllerFrontend(GridLayout):
    """The application frontend."""

    class QueuePanel(GridLayout):
        """The queue panel, render title and upcoming tracks."""

        def __init__(self, **kwargs):
            """Instantiate the queue panel."""
            super(ControllerFrontend.QueuePanel, self).__init__(**kwargs)
            self.cols = 1
            self.rows = 11
            self.size_hint = (0.25, 1)
            self.add_widget(
                Label(text=TITLE, font_size='48sp', font_name=FONT_TITLE, color=COL_TITLE))

            for i in range(10):
                self.add_widget(
                    Label(text=f'Track {i}', font_name=FONT_UI, color=COL_TEXT))

    class ControlsPanel(GridLayout):
        """The controls and 'now playing' interface."""

        def __init__(self, **kwargs):
            """Instantiate the controls panel."""
            super(ControllerFrontend.ControlsPanel, self).__init__(**kwargs)
            # TODO: Change layout to something more practical
            with self.canvas:
                Rectangle(pos=(0.25 * DISPLAY_SIZE[0], 0), size=DISPLAY_SIZE)
            self.cols = 1
            self.rows = 1
            self.size_hint = (0.75, 1)
            self.add_widget(Label(text='Now Playing', font_name=FONT_UI))

    def __init__(self, **kwargs):
        """Instantiate the frontend."""
        super(ControllerFrontend, self).__init__(**kwargs)
        self.cols = 2
        self.rows = 1
        self.add_widget(ControllerFrontend.QueuePanel())
        self.add_widget(ControllerFrontend.ControlsPanel())

        Window.size = DISPLAY_SIZE
        Window.clearcolor = COL_BG


class TunebotController(App):
    """The controller application."""

    def build(self):
        """Construct the application."""
        return ControllerFrontend()


if __name__ == '__main__':
    TunebotController().run()
