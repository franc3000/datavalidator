def test_A():
    cols = ['apprlndval', 'apprtotval', 'assdimpval']
    correct = ['appr_land_value', 'appr_total_value', 'assd_improvement_value']

    # map the col names
    new_cols = []

    assert new_cols == correct
