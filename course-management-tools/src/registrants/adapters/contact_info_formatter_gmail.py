from ..core.contact_info_formatter import ContactInfoFormatter


class GmailContactInfoFormatter(ContactInfoFormatter):
    def format_contact_info(self, registrants):
        contact_info = ""
        for registrant in registrants:
            contact_info += f"{registrant.email},\n"
        return contact_info
