# ui/v2/styles/stylesheet.py

from .colors import Colors


def build_stylesheet():
    return f"""
    QWidget {{
        background-color: {Colors.BACKGROUND};
        color: {Colors.TEXT};
        font-family: Segoe UI;
        font-size: 10pt;
    }}

    QFrame {{
        background-color: {Colors.SURFACE};
        border: 1px solid {Colors.BORDER};
        border-radius: 10px;
    }}

    QPushButton {{
        background-color: {Colors.PRIMARY};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 14px;
    }}

    QPushButton:hover {{
        background-color: {Colors.PRIMARY_HOVER};
    }}

    QPushButton:pressed {{
        background-color: {Colors.PRIMARY_PRESSED};
    }}
    """