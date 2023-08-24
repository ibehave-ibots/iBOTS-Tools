from typing import NamedTuple
from src.registrants.core.workflows import RegistrantsWorkflows
from src.registrants.adapters.registrants_repo_zoom import ZoomRegistrantsRepo
from src.external.zoom_api.zoom_api import ZoomRestApi
from src.external.zoom_api.zoom_oauth import create_access_token
from src.external.console import Console
from src.registrants.adapters.contact_info_formatter_gmail import (
    GmailContactInfoFormatter,
)
from src.registrants.adapters.contact_info_presenter_print import (
    PrintContactInfoPresenter,
)
from src.registrants.interactors.cli import RegistrantsCLIInteractor
from src.registrants.adapters.cli_argparse import ArgparseCLI

access_token = create_access_token()["access_token"]
interactor = RegistrantsCLIInteractor(
    cli=ArgparseCLI(),
    workflows=RegistrantsWorkflows(
        registrants_repo=ZoomRegistrantsRepo(
            zoom_api=ZoomRestApi(), access_token=access_token
        )
    ),
    presenter=PrintContactInfoPresenter(
        formatter=GmailContactInfoFormatter(), console=Console()
    ),
)
interactor.display_approved_registrants_contact_info()
