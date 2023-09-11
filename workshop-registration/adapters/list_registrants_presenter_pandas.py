from typing import List

import pandas as pd
from app import ListRegistrantPresenter, RegistrantSummary


class PandasListRegistrantPresenter(ListRegistrantPresenter):

    def show(self, registrants: List[RegistrantSummary]) -> None:
        registrants_list = []
        for registrant in registrants:
            registrants_list.append(registrant.to_dict())
        df = pd.DataFrame(registrants_list)
        print(df.to_string())