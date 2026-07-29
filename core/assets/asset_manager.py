from pathlib import Path


class AssetManager:

    ROOT = Path("assets")

    @classmethod
    def branding(cls, *parts) -> str:
        return str(cls.ROOT.joinpath("branding", *parts))

    @classmethod
    def icon(cls, *parts) -> str:
        return str(cls.ROOT.joinpath("icons", *parts))

    @classmethod
    def image(cls, *parts) -> str:
        return str(cls.ROOT.joinpath("images", *parts))