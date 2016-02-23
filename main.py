import os
import json
import sys
import csv
from csvvalidator import *
from examples import schema_corelogic

from column_name_dict import column_name_dict

def main():

    validator = CSVValidator(schema_corelogic.corelogic,column_name_dict)
    print column_name_dict
    # basic header and record length checks
    validator.add_header_check('EX1', 'bad header')
    validator.add_record_length_check('EX2', 'unexpected record length')

    # some simple value checks
    validator.add_value_check(
        'LAST MARKET SALE PRICE', float, 'EX3', 'LAST MARKET SALE PRICE must be number')

    # validator.add_value_check(
    #     'patient_id', int, 'EX4', 'patient id must be an integer')
    # validator.add_value_check(
    #     'gender', enumeration('M', 'F'), 'EX5', 'invalid gender')
    # validator.add_value_check(
    #     'state', number_range_inclusive(0, 120, int), 'EX6', 'invalid age in years')
    # validator.add_value_check(
    #     'date_inclusion', datetime_string('%Y-%m-%d'), 'EX7', 'invalid date')

    # a more complicated record check
    def check_state(r):
        state = int(r['PROPERTY STATE'])
        valid = state == 'TX'
        if not valid:
            raise RecordError('EX8', 'invalid Property State')
    validator.add_record_check(check_state)

    # validate the data and write problems to stdout
    data = csv.reader(open('examples/corelogic_master_sow02.csv'), delimiter=',')



    #data_header = map_header(data_header, column_name_dict)

    problems = validator.validate(data)
    #write_problems(problems, sys.stdout)



if __name__ == '__main__':
    main()
