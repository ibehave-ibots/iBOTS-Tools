import sys
sys.path.append('..')

from web.create_app import create_app


app = create_app()
app.list_registrants(workshop_id="12345")
