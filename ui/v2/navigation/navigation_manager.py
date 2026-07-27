from PySide6.QtWidgets import QStackedWidget


class NavigationManager:
    """
    Handles page registration and page navigation.
    """

    def __init__(self, stack: QStackedWidget):
        self.stack = stack
        self.pages = {}

    def register(self, name: str, widget):
        self.pages[name] = widget
        self.stack.addWidget(widget)

    def show(self, name: str):
        if name not in self.pages:
            return

        self.stack.setCurrentWidget(
            self.pages[name]
        )