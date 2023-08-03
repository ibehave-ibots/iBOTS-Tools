from ..core.contact_info_formatter_repo import ContactInfoFormatterRepo


class GmailContactInfoFormatterRepo(ContactInfoFormatterRepo):
    def __init__(self):
        self.delimiter = ","

    def format_contact_info(self, registrants):
        contact_info = ""
        for registrant_idx, registrant in enumerate(registrants):
            contact_info += f"{registrant.email}"
            is_last_registrant = registrant_idx < len(registrants) - 1
            if is_last_registrant:
                contact_info += self.delimiter
        return contact_info
