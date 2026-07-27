from dataclasses import dataclass


@dataclass
class InstallationResult:

    success: bool = False

    external_tax_provider_found: bool = False
    web_pos_found: bool = False
    amvrosia_found: bool = False
    snservice_found: bool = False

    installation_path: str = ""

    message: str = ""