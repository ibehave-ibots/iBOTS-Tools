from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

@dataclass
class Model:
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(data=[], columns=['name', 'status']))

    def update_registrant_status(self, id, status):
        self.table.loc[id, 'status'] = status

if not 'model' in st.session_state:
    st.session_state['model'] = Model(
        table=pd.DataFrame([
            {'name': 'Anna', 'status': 'waitlisted'},
            {'name': 'Banana','status': 'waitlisted'},
        ])
    )


model: Model = st.session_state['model']

st.data_editor(model.table, key="data_editor")
editor_updates = st.session_state['data_editor']
if editor_updates['edited_rows']:
    for idx, changes in editor_updates['edited_rows'].items():
        match idx, changes:
            case int(i), {"status": str(new_status)}:
                ...
                model.update_registrant_status(id=i, status=new_status)
            case _:
                ...
                # st.error("This change shouldn't be possible!")
    st.experimental_rerun()


st.write(model.table)


