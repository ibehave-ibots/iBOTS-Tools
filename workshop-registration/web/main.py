import sys
sys.path.append('..')

from web.create_repo import create_repo


app = create_repo()
app.list_registrants(workshop_id="12345")
