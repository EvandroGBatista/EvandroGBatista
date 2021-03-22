import viola
from viola.core.db import Bedpe, Vcf
import pandas as pd

def assert_vcf_equal(left, right, check_like=True):
    ls_left_table = left.table_list
    ls_right_table = right.table_list
    assert set(ls_left_table) == set(ls_right_table)
    for tablename in ls_left_table:
        df_left = left.get_table(tablename)
        df_right = right.get_table(tablename)
        if df_left.empty & df_right.empty:
            continue
        try:
            pd.testing.assert_frame_equal(df_left, df_right, check_like=check_like)
        except AssertionError:
            print('\nwhen asserting {} table, following error occured!'.format(tablename))
            raise 
    
    # assert metadata
    assert left._metadata == right._metadata