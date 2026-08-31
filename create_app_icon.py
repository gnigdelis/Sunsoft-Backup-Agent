from pathlib import Path
import sys

from PIL import Image
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QImage, QPainter
from PySide6.QtSvg import QSvgRenderer


PROJECT_ROOT = Path(__file__).resolve().parent

SVG_PATH = (
    PROJECT_ROOT
    / "assets"
    / "icons"
    / "support_agent.svg"
)

WINDOW_DIR = (
    PROJECT_ROOT
    / "assets"
    / "branding"
    / "window"
)

PNG_PATH = (
    WINDOW_DIR
    / "support_agent_1024.png"
)

ICO_PATH = (
    WINDOW_DIR
    / "app.ico"
)


def main():

    if not SVG_PATH.exists():

        raise FileNotFoundError(
            f"Missing SVG icon: {SVG_PATH}"
        )

    WINDOW_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    #
    # Render the actual Support Agent SVG
    # into a high-resolution transparent PNG.
    #

    size = 1024

    image = QImage(
        size,
        size,
        QImage.Format.Format_ARGB32,
    )

    image.fill(
        Qt.GlobalColor.transparent
    )

    renderer = QSvgRenderer(
        str(SVG_PATH)
    )

    if not renderer.isValid():

        raise RuntimeError(
            f"Invalid SVG icon: {SVG_PATH}"
        )

    painter = QPainter(
        image
    )

    renderer.render(
        painter
    )

    painter.end()

    if not image.save(
        str(PNG_PATH),
        "PNG",
    ):

        raise RuntimeError(
            f"Could not create PNG: {PNG_PATH}"
        )

    #
    # Create a real Windows ICO with multiple sizes.
    #

    png = Image.open(
        PNG_PATH
    ).convert(
        "RGBA"
    )

    png.save(
        ICO_PATH,
        format="ICO",
        sizes=[
            (256, 256),
            (128, 128),
            (64, 64),
            (48, 48),
            (32, 32),
            (24, 24),
            (16, 16),
        ],
    )

    print(
        f"Created: {ICO_PATH}"
    )
    print(
        f"Source:  {SVG_PATH}"
    )


if __name__ == "__main__":

    try:

        main()

    except Exception as exc:

        print(
            f"ERROR: {exc}"
        )

        sys.exit(1)
