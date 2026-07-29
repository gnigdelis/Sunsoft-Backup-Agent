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
        # Νέο μέγεθος
        #

        self.setFixedSize(130, 130)

    def setValue(self, value):

        self.value = max(0, min(100, value))

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        margin = 10
        size = min(self.width(), self.height()) - margin * 2

        rect_x = (self.width() - size) / 2
        rect_y = (self.height() - size) / 2

        #
        # Background
        #

        background_pen = QPen(
            QColor("#36393F"),
            8,
        )

        painter.setPen(background_pen)

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

        progress_pen = QPen(
            QColor(Theme.Colors.PRIMARY),
            8,
        )

        progress_pen.setCapStyle(Qt.RoundCap)

        painter.setPen(progress_pen)

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
            17,
            QFont.Bold,
        )

        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignCenter,
            f"{self.value}%",
        )