from typing import List

from ..core.contact_info_repo import ContactInfoRepo
from ..core.contact_info_formatter_repo import ContactInfoFormatterRepo
from ..core.entities import Registrant


class PrintContactInfoRepo(ContactInfoRepo):
    def __init__(self, formatter: ContactInfoFormatterRepo):
        self.formatter = formatter

    def display_contact_info(self, registrants: List[Registrant]) -> None:
        formatted_contact_info = self.formatter.format_contact_info(registrants)
        print(formatted_contact_info, end="")
