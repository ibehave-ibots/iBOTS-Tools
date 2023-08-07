from typing import List

from ..core.contact_info_presenter import ContactInfoPresenter
from ..core.contact_info_formatter import ContactInfoFormatter
from ..core.entities import Registrant


class PrintContactInfoPresenter(ContactInfoPresenter):
    def __init__(self, formatter: ContactInfoFormatter):
        self.formatter = formatter

    def display_contact_info(self, registrants: List[Registrant]) -> None:
        formatted_contact_info = self.formatter.format_contact_info(registrants)
        print(formatted_contact_info, end="")
