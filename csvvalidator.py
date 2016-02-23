__author__ = 'hellpanerrr'
from formatter import format_col_name
import warnings
from itertools import tee
from datetime import datetime


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class HeaderError(Error):
    """Exception raised for errors in the header.

    Attributes:
        column -- column in which the error occurred
        msg  -- explanation of the error
    """

    def __init__(self, msg, column=None, ):
        self.column = column
        self.msg = msg

    def __repr__(self):
        if self.column:
            return repr('%s in %s' % (self.msg, self.column))
        else:
            return repr(self.msg)


class CSVValidator(object):
    def __init__(self, schema, column_name_dict):
        self.schema = schema
        self.checks = []
        self.column_name_dict = column_name_dict

    def add_header_check(self, *args):
        self.checks.append('mock header check')

    def add_record_length_check(self, *args):
        self.checks.append('mock record_length_check')

    def add_value_check(self, *args):
        self.checks.append('mock value_check')

    def add_record_check(self, *args):
        self.checks.append('mock record_check')
        pass

    @staticmethod
    def execute_check(check):
        print 'Executing mock check %s' % check
        return True

    @staticmethod
    def append_column(array, content=''):
        '''Appends a column to the end of a table'''
        for n, i in enumerate(array):
            array[n].append(content)
        return array

    @staticmethod
    def map_header(header, schema_dict):
        '''Replaces header columns with the ones in schema_dict'''

        for n, col in enumerate(header):
            if col in schema_dict:
                header[n] = schema_dict[col]

        return header

    def process_schema(self, schema, need_mapping=False):
        if schema:
            ret = {}
            if type(schema) == dict:
                if 'fields' in schema:
                    for d in schema['fields']:
                        ret[d.pop('name')] = d
                elif need_mapping:
                    new_schema = {}
                    for name in schema:
                        new_schema[format_col_name(name)] = schema[name]

                    for d in self.map_header(new_schema.keys(),self.column_name_dict):
                        ret[d] = new_schema[d]
            return ret

    def process_header(self, data):
        header = data.next()

        header = map(format_col_name, header)

        header = self.map_header(header, self.column_name_dict)

        if len(header) > len(self.column_name_dict):
            raise HeaderError('Extra columns.')
        elif len(header) < len(self.column_name_dict):
            missing_columns = set(header) - set(self.column_name_dict.keys())
            warnings.warn('Columns are missing: [%s]' % ', '.join(missing_columns))
            for col in missing_columns:
                header.append(col)
        return header, len(missing_columns)

    def output_file(self, data):
        pass

    @staticmethod
    def type_mapping():
        return {
            'string': str,
            'int': int,
            'date': datetime

        }

    def apply_schema_checks_to_cell(self, cell, name, schema):
        checks = schema[name]
        if 'type' in checks:
            assert type(cell) == self.type_mapping(checks['type'])
        if 'range' in checks:
            assert checks['range'][0] < cell < checks['range'][1]

    def validate(self, data):
        individual_checks = map(self.execute_check, self.checks)
        header, number_of_missing_columns = self.process_header(data)
        schema = self.process_schema(self.schema,need_mapping=True)
        data, data_backup = tee(data)
        for n, row in enumerate(data):
            for j, cell in enumerate(row):
                name = header[j]
                self.apply_schema_checks_to_cell(cell, name, schema)
