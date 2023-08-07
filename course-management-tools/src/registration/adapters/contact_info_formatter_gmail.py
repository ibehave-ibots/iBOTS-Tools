from ..core.contact_info_formatter import ContactInfoFormatter


class GmailContactInfoFormatter(ContactInfoFormatter):
    def format_contact_info(self, registrants):
        contact_info = ""
        for registrant_idx, registrant in enumerate(registrants):
            contact_info += f"{registrant.email}"
            is_not_last_registrant = registrant_idx < len(registrants) - 1
            if is_not_last_registrant:
                contact_info += ",\n"
        return contact_info
