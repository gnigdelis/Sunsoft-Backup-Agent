# ui/v2/styles/typography.py

from PySide6.QtGui import QFont


class Typography:

    @staticmethod
    def title():
        return QFont("Segoe UI", 18, QFont.Bold)

    @staticmethod
    def heading():
        return QFont("Segoe UI", 12, QFont.Bold)

    @staticmethod
    def body():
        return QFont("Segoe UI", 10)

    @staticmethod
    def small():
        return QFont("Segoe UI", 9)