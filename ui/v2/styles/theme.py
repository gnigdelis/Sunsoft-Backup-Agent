# ui/v2/styles/theme.py

from .colors import Colors
from .spacing import Spacing
from .radius import Radius
from .typography import Typography
from .stylesheet import build_stylesheet


class Theme:
    Colors = Colors
    Spacing = Spacing
    Radius = Radius
    Typography = Typography

    @staticmethod
    def stylesheet():
        return build_stylesheet()