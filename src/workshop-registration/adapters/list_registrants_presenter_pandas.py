from typing import List

import pandas as pd
from app import ListRegistrantPresenter, RegistrantSummary


class PandasListRegistrantPresenter(ListRegistrantPresenter):

    def show(self, registrants: List[RegistrantSummary]) -> None:
        registrants_list = []
        for registrant in registrants:
            registrants_list.append(registrant.to_dict())
        df = pd.DataFrame(registrants_list).rename_axis(index='num')
        df.index += 1
        del df['id']
        del df['workshop_id']
        print(df.to_csv(index=True, sep=','))