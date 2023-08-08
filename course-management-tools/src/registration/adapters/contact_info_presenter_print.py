from typing import List

from ..core.contact_info_presenter import ContactInfoPresenter
from ..core.contact_info_formatter import ContactInfoFormatter
from ..core.entities import Registrant
from ...external.console import Console


class PrintContactInfoPresenter(ContactInfoPresenter):
    def __init__(self, formatter: ContactInfoFormatter, console: Console):
        self.formatter = formatter
        self.console = console

    def display_contact_info(self, registrants: List[Registrant]) -> None:
        formatted_contact_info = self.formatter.format_contact_info(registrants)
        self.console.print(formatted_contact_info, end="")
