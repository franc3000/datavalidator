import warnings
import traceback
import csv
import pandas as pd
from dateutil.parser import parse
from functools import partial

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

def format_col_name(colname):
    """
    Lowercase column name, replace/remove special characters
    """
    colname = colname.lower()
    colname = colname.replace(' ', '_')
    colname = colname.replace('%', 'pct')
    colname = colname.replace('+', 'plus')
    colname = colname.replace('.', '_')
    colname = colname.replace(':', '_')
    colname = colname.replace('/', '_')
    colname = colname.replace('(', '')
    colname = colname.replace(')', '')
    colname = colname.replace('-', '_')
    colname = colname.replace('__', '_')
    colname = colname.replace('__', '_')
    colname = colname.replace('#', '')
    colname = colname.replace('&_', '')
    colname = colname.replace('1st', 'first')
    return str(colname)

class CSVValidator(object):
    def __init__(self, schema, column_name_dict):
        self.schema = schema
        self.checks = []
        self.column_name_dict = column_name_dict

    @staticmethod
    def execute_check(check):
        print 'Executing mock check %s' % check
        return True


    def process_schema(self, need_mapping=False):
        if self.schema:
            schema = pd.DataFrame(self.schema['fields'])
            df = pd.DataFrame(data = [schema.T.values[1]], columns = schema.T.values[0])
            self.schema = df.to_dict(orient='records')[0]


    def output_file(self, data):
        pass

    @staticmethod
    def type_mapping():
        return {
            'string': str,
            'int': int,
            'date': parse

        }
    def add_generic_check(self, check):
        self.checks.append(check)

    def add_header_check(self, value, message):
        self.checks.append({'type': 'header','message':message, 'value':value })

    def add_record_length_check(self, value, message):
        self.checks.append({'type': 'length','message':message, 'value':value })

    def add_value_check(self, column, column_type, value, message):
        self.checks.append({'type': 'value','message':message, 'column':column, 'column_type':type,'value':value })

    def run_checks(self):
        if self.checks:
            checks = self.checks
            for check in checks:
                if 'column' in check:
                    print 'a'
                    self.run_column_check(check)
                elif 'header' in check['type']:
                    pass
                elif 'length' in check['type']:
                    pass


    def run_schema_checks(self):
        df = self.df
        bad_rows = {}
        new_df = pd.DataFrame([])
        for col in df:
            check = {'column':col,'type':'type','value':self.schema[col],'not_update_value':True}
            result = self.apply_column_check(check=check)
            new_col = []
            for n,cell in enumerate(result):
                if not cell[0]:
                    if n not in bad_rows:
                        bad_rows[n] = []
                    else:
                        bad_rows[n].append('Column %s check for %s==%s' % (col,check['type'],check['value']))
                new_col.append(cell[1])
            new_df[col]=new_col
        return bad_rows,new_df

    def apply_column_check(self, check):

        bad_rows = {}

        #check = {'column':col,'type':'type','value':self.schema[col]}
        column = check['column']
        result = map(partial(self.apply_check_to_cell,check=check), self.df[column])

        new_col = []
        print 'Checking %s ' % column
        for n,cell in enumerate(result):
            if not cell[0]:
                if n not in bad_rows:
                    bad_rows[n] = []
                else:
                    bad_rows[n].append('Column %s check for %s==%s' % (column,check['type'],check['value']))
                    new_col.append(cell)
            new_col.append(cell)
        if not check.get('update_value'):
            self.df[column] = [i[1] for i in new_col]
        return new_col


#         column = check['column']
#         if column in self.df.columns:
#             print 'Checking column %s for %s==%s' % (column,check['type'],check['value'])
#             return map(partial(apply_check_to_cell,check=check), self.df[column])

    def apply_check_to_cell(self,cell, check):
        mapping = {
                'string': str,
                'int': int,
                'date': parse

            }
        if check['type'] == 'type':
            try:
                ret = mapping[check['value']](cell)

                return (True, ret)
            except:
                print traceback.print_exc()
                return (False, cell)
        elif check['type'] == 'value':
            try:
                ret = check['value'] == cell
                return (True, cell)
            except:
                return (False, cell)
        elif check['type'] == 'custom':
            try:
                ret = check['value'](cell)
                return (True, cell)
            except:
                return (False, cell)





    def validate(self, data):
      #  individual_checks = map(self.execute_check, self.checks)
        self.process_schema(need_mapping=False)

        header = csv.reader(open(data)).next()
        df = pd.read_csv(data,names=header)[1:]
        df.columns = map(format_col_name, df.columns)

        df.columns = [self.column_name_dict[i] if i in self.column_name_dict else i for i in df.columns ]
        #schema = map(format_col_name, self.schema.keys())
        #self.schema = schema
        #schema = {column_name_dict[i]:self.schema[i] if i in column_name_dict else i for i in self.schema}

        ### formatting schema using dictionary for this to run properly ###
        schema = {}
        for i in self.schema:
            if i in self.column_name_dict:
                schema[self.column_name_dict[i]] = self.schema[i]
            else:
                schema[i] = self.schema[i]
        self.missing_columns = []
        self.schema = schema
        self.df = df
        if len(schema) > len(df.columns):
            self.missing_columns = set(schema) - set(df.columns)
            warnings.warn('Columns are missing: [%s]' % ', '.join(self.missing_columns))
            for col in self.missing_columns:
                df[col] = ''
        elif len(schema) < len(df.columns):
            extra_columns = set(df.columns) - set(self.schema)
            warnings.warn('Extra columns: [%s]' % ', '.join(extra_columns))

            raise HeaderError('Extra columns.')
        self.df = df
