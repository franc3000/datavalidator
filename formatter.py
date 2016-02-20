
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
    return colname
