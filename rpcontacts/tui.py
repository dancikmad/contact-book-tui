from textual.app import App
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Footer, Header, Button, Label

class ContactsApp(App):
    CSS_PATH = "rpcontacts.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("q", "request_quit", "Quit"),
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

    def action_request_quit(self):
        """
        Method that takes a screen instance as its first argument. The second
        argument should be the funtion object that will process the dialog's response
        which is `check_answer()`
        """
        def check_answer(accepted):
            if accepted:
                self.exit()

        self.push_screen(QuestionDialog("Do you want to quit?"), check_answer)


class QuestionDialog(Screen):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.message = message

    def compose(self):
        no_button = Button("No", variant="primary", id="no")
        no_button.focus()

        yield Grid(
            Label(self.message, id="question"),
            Button("Yes", variant="error", id="yes"),
            no_button,
            id="question-dialog",
        )

    def on_button_pressed(self, event):
        if event.button.id == "yes":
            self.dismiss(True)
        else:
            self.dismiss(False)
