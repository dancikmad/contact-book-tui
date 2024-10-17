from textual.app import App, on
from textual.containers import Grid, Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import Footer, Header, Button, Label, DataTable, \
    Static, Input

class ContactsApp(App):
    CSS_PATH = "rpcontacts.tcss"
    BINDINGS = [
        ("m", "toggle_dark", "Toggle dark mode"),
        ("a", "add", "Add"),
        ("q", "request_quit", "Quit"),
        ("d", "delete", "Delete"),
        ("c", "clear_all", "Clear All"),
        ("q", "request_quit", "Quit"),
    ]

    def __init__(self, db):
        super().__init__()
        self.db = db

    def compose(self):
        """
        Method to build the app's main screen
        """
        yield Header()
        contacts_list = DataTable(classes="contacts-list")
        contacts_list.focus()
        contacts_list.add_columns("Name", "Phone", "Email")
        contacts_list.cursor_type = "row"
        contacts_list.zebra_stripes = True
        add_button = Button("Add", variant="success", id="add")
        add_button.focus()
        buttons_panel = Vertical(
            add_button,
            Button("Delete", variant="warning", id="delete"),
            Static(classes="separator"),
            Button("Clear All", variant="error", id="clear"),
            classes="buttons_panel"
        )
        yield Horizontal(contacts_list, buttons_panel)
        yield Footer()

    @on(Button.Pressed, "#add")
    def action_add(self):
        def check_contact(contact_data):
            if contact_data:
                self.db.add_contact(contact_data)
                id, *contact = self.db.get_last_contact()
                self.query_one(DataTable).add_row(*contact, key=id)

        self.push_screen(InputDialog(), check_contact)

    def on_mount(self):
        """
        Method to set up some properties of the main screen, like title and subtitle
        """
        self.title = 'RP Contacts'
        self.sub_title = "A Contacts Book App with Textual & Python"
        self._load_contacts()

    def _load_contacts(self):
        contacts_list = self.query_one(DataTable)
        for contact_data in self.db.get_all_contacts():
            id, *contact = contact_data
            contacts_list.add_row(*contact, key=id)



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


class InputDialog(Screen):
    def compose(self):
        yield Grid(
            Label("Add Contact", id="title"),
            Label("Name:", classes="label"),
            Input(
                placeholder="Contact Name",
                classes="input",
                id="name",
            ),
            Label("Phone:", classes="label"),
            Input(
                placeholder="Contact Phone",
                classes="input",
                id="phone",
            ),
            Label("Email:", classes="label"),
            Input(
                placeholder="Contact Email",
                classes="input",
                id="email",
            ),
            Static(),
            Button("Cancel", variant='warning', id='cancel'),
            Button("Ok", variant='success', id='ok'),
            id='input-dialog',
        )

    def on_button_pressed(self, event):
        if event.button.id == "ok":
            name = self.query_one("#name", Input).value
            phone = self.query_one("#phone", Input).value
            email = self.query_one("#email", Input).value
            self.dismiss((name, phone, email))

        else:
            self.dismiss(())
