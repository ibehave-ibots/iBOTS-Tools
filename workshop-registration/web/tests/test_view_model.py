import pandas.testing as pdt
import pytest
import pandas as pd

from web.view_model import ViewModel


def test_updating_table_gets_new_data_and_doesnt_change_original():
    model = ViewModel()
    old_table = model.table.copy()
    
    registrants = [
        {'id': '123', 
         'workshop_id': 'abc', 
         'name': 'Joe', 
         'email': 'j@j.com', 
         'registered_on': 'yesterday', 
         'group_name': 'AG Ag',
         'status': 'waitlisted',
        },
    ]
    new_model = model.update_registrant_table(registrants=registrants)
    row = new_model.table.iloc[0]
    for idx, row in new_model.table.iterrows():
        reg = registrants[idx]
        for name in reg:
            assert reg[name] == row[name]
        
    pdt.assert_frame_equal(model.table, old_table)


def test_setting_status_updates_correct_row_in_table():
    table = pd.DataFrame([
        {'id': '123', 'status': 'waitlisted', 'state': 'waitlisted'},
        {'id': '345', 'status': 'waitlisted', 'state': 'waitlisted'},
    ])
    model = ViewModel(table=table)
    new_model = model.set_registration_status(id='123', status='approved')
    assert model.table.iloc[0]['status'] == 'waitlisted'  # original not changed
    assert model.table.iloc[0]['state'] == 'waitlisted'  # original not changed
    assert new_model.table.iloc[0]['status'] == 'approved'  # new changed
    assert new_model.table.iloc[0]['state'] == 'approved'  # new changed
    assert new_model.table.iloc[1]['status'] == 'waitlisted'  # second row not changed
    assert new_model.table.iloc[1]['state'] == 'waitlisted'  # second row not changed

    new_model2 = new_model.set_registration_status(id='345', status='rejected')
    assert new_model2.table.iloc[1]['status'] == 'rejected'  # second row changed
    assert new_model2.table.iloc[1]['state'] == 'rejected'  # second row changed
    assert new_model2.table.iloc[0]['status'] == 'approved'  # first row not changed
    assert new_model2.table.iloc[0]['state'] == 'approved'  # first row not changed



# def test_updating_