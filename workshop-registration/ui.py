from adapters import StreamlitRegistrantPresenter
from app import RegistrantSummary

registrants = [
    RegistrantSummary(
        name="eve",
        email="e@e.com",
        status="approved",
        registered_on="25092023",
        workshop_id="12345",
        id="54321",
        group_name="Prof. Sangee"
    ),
    RegistrantSummary(
        name="adam",
        email="a@a.com",
        status="rejected",
        registered_on="29102023",
        workshop_id="7890",
        id="0987",
        group_name="Prof. Bee"
    )
]
presenter = StreamlitRegistrantPresenter()
presenter.show_update(registrant=registrants[0])
# presenter.show(registrants=registrants)