from rpcontacts.tui import ContactsApp
from rpcontacts.database import Database

def main():
    app = ContactsApp(db=Database())
    app.run()

if __name__ == "__main__":
    main()
