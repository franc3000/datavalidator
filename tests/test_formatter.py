from ..formatter import format_col_name

def test_format():
    colname = 'OWNER 1 LABEL NAME'
    correct = 'owner_1_label_name'

    new_colname = format_col_name(colname)

    assert new_colname == correct



if __name__ == '__main__':
	test_format()
