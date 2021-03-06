import os
import json
import sys
import csv
from csvvalidator import *
from examples import schema_corelogic


from column_name_dict import column_name_dict

def main():
    #schema_corelogic.corelogic
    # validator = CSVValidator(json.load(open('examples/schema_corelogic.json')),column_name_dict)
    # print column_name_dict
    # # basic header and record length checks
    # validator.add_header_check('EX1', 'bad header')
    # validator.add_record_length_check('EX2', 'unexpected record length')
    #
    # # some simple value checks
    # validator.add_value_check(
    #     'LAST MARKET SALE PRICE', float, 'EX3', 'LAST MARKET SALE PRICE must be number')

    # validator.add_value_check(
    #     'patient_id', int, 'EX4', 'patient id must be an integer')
    # validator.add_value_check(
    #     'gender', enumeration('M', 'F'), 'EX5', 'invalid gender')
    # validator.add_value_check(
    #     'state', number_range_inclusive(0, 120, int), 'EX6', 'invalid age in years')
    # validator.add_value_check(
    #     'date_inclusion', datetime_string('%Y-%m-%d'), 'EX7', 'invalid date')

    # a more complicated record check
    # def check_state(r):
    #     state = int(r['PROPERTY STATE'])
    #     valid = state == 'TX'
    #     if not valid:
    #         raise RecordError('EX8', 'invalid Property State')
    # validator.add_record_check(check_state)

    # validate the data and write problems to stdout
    # data = csv.reader(open('examples/corelogic_master_sow02.csv'), delimiter=',')

    validator = CSVValidator(json.load(open('examples/schema_corelogic.json')),column_name_dict)

    data = 'examples/corelogic_master_sow02.csv'
    validator.validate(data)
    bad_rows, fixed_df = validator.run_schema_checks()

    def check_state(cell):
        valid = 5<cell<100
        if not valid:
            raise Error('invalid Property State')

    print 'Bad rows percent: %s' % (len(bad_rows)*1.0/(len(fixed_df)*100 ))
    ### write errors to the bad_rows variable (default) ###
    validator.add_generic_check({'type_of_check':'custom' ,'column':'cltv','value':check_state})
    validator.run_checks()


    ### throw an exception immediately ###
    validator.clear_checks()
    validator.add_generic_check({'type_of_check':'custom' ,'column':'cltv','value':check_state,'exception':Error})
    validator.run_checks()

    #data_header = map_header(data_header, column_name_dict)

    #problems = validator.validate(data)
    #write_problems(problems, sys.stdout)



if __name__ == '__main__':
    main()
