from textual.app import App
from textual.widgets import Footer, Header

class ContactsApp(App):
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode")
    ]
    def compose(self):
        """
        Method to build the app's main screen
        """
        yield Header()
        yield Footer()

    def on_mount(self):
        """
        Method to set up some properties of the main screen, like title and subtitle
        """
        self.title = 'RP Contacts'
        self.sub_title = "A Contacts Book App with Textual & Python"

    def action_toggle_dark(self):
        """
        Method that the app must invoke when pressing the action key.
        """
        self.dark = not self.dark
