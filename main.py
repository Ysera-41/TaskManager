from app.database import init_db
from gui.main_window import start_gui

if __name__ == "__main__":
    init_db()
    start_gui()