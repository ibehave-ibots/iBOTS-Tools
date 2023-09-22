from dataclasses import dataclass, field
import pandas as pd
import streamlit as st

@dataclass
class Model:
    table: pd.DataFrame = field(default_factory=lambda: pd.DataFrame(data=[], columns=['name', 'status', 'state']))

    def set_data(self, data):
        self.table = pd.DataFrame(data, columns=['name', 'status', 'state'])

    def update_registrant_status(self, id, status):
        self.table.loc[id, 'status'] = status
        self.table.loc[id, 'state'] = status

if not 'model' in st.session_state:
    model = Model()
    model.set_data([
        {'name': 'Anna', 'status': 'waitlisted'},
        {'name': 'Banana','status': 'waitlisted'},
    ])
    st.session_state['model'] = model
    


model: Model = st.session_state['model']
def update():    
    updated_rows = st.session_state['data_editor']['edited_rows']
    assert len(updated_rows) == 1
    for idx, changes in updated_rows.items():
        match idx, changes:
            case int(i), {"status": str(new_status)}:
                model.update_registrant_status(id=i, status=new_status)
            case _:
                st.write("This change shouldn't be possible!", )

st.data_editor(model.table, key="data_editor", on_change=update)



