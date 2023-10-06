import os 
import pytest
from pytest import mark
from adapters import Spreadsheet_attendancepresenter
from app.attendance_presenter import AttendanceSummary
    

def test_correct_number_of_rows_written_to_csv_file():

    #GIVEN
    # presenter and list of attendance summaries
    presenter = Spreadsheet_attendancepresenter()
    attendance_summaries =[
        AttendanceSummary(
                name = 'Alice',
                email = 'a@a.com',
                hours_per_session = {'session1': 0.8,
                                     'session2': 3.0,
                                    'session3' : 0.0,
                                    'session4' : 1.2
                                    }
        ),
        AttendanceSummary(
                name = 'Balice',
                email = 'b@a.com',
                hours_per_session = {'session1': 1.8,
                                     'session2': 2.7,
                                    'session3' : 4.2,
                                    'session4' : 0.2
                                    }
        )

    ]

    #WHEN
    presenter.write_csv(attendance_summaries=attendance_summaries, output_filename='test.csv')

    #THEN
    assert os.path.isfile('test.csv')
    with open('test.csv', 'r') as f:
        lines = f.readlines()
    assert len(lines) == len(attendance_summaries) + 1

    os.remove('test.csv')


#Does not work - why not?!
@pytest.fixture
def delete_test_spreadsheet_file():
    yield
    os.remove('test.csv')