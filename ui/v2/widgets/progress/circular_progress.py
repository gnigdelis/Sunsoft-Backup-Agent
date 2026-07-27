from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen,
)
from PySide6.QtWidgets import QWidget

from ui.v2.styles.theme import Theme


class CircularProgress(QWidget):

    def __init__(self, value=0, parent=None):

        super().__init__(parent)

        self.value = value

        #
        # Πιο compact μέγεθος
        #

        self.setMinimumSize(170, 170)
        self.setMaximumSize(170, 170)

    def setValue(self, value):

        self.value = max(0, min(100, value))

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)

        size = min(self.width(), self.height()) - 16

        rect_x = (self.width() - size) / 2
        rect_y = (self.height() - size) / 2

        #
        # Background
        #

        pen = QPen(
            QColor("#36393F"),
            10,
        )

        painter.setPen(pen)

        painter.drawArc(
            int(rect_x),
            int(rect_y),
            int(size),
            int(size),
            0,
            360 * 16,
        )

        #
        # Progress
        #

        pen = QPen(
            QColor(Theme.Colors.PRIMARY),
            10,
        )

        pen.setCapStyle(Qt.RoundCap)

        painter.setPen(pen)

        painter.drawArc(
            int(rect_x),
            int(rect_y),
            int(size),
            int(size),
            90 * 16,
            int(-360 * self.value / 100 * 16),
        )

        #
        # Percentage
        #

        painter.setPen(
            QColor(Theme.Colors.TEXT)
        )

        font = QFont(
            "Segoe UI",
            20,
            QFont.Bold,
        )

        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            f"{self.value}%",
        )