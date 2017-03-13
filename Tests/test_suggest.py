import unittest
import pandas as pd
import numpy as np
import sys
sys.path.append('../EASE')

import ease

class TEST_suggest(unittest.TestCase):

    def test_suggest_output(self):
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        capacity = 5000
        vote = ease.rf(prec, ts, tw, ws)
        avg_cap = ease.avg_capacity(vote)
        possible_type_list = ease.possible_type(avg_cap)
        conventional, clean = ease.clean_or_conv(possible_type_list)
        conventional = ease.sort_and_pick(conventional)
        clean = ease.sort_and_pick(clean)
        
        source_co2 = {'Coal': 2133, 'Petro': 1700, 'NG': 1220}
        # test whether conventional type in source dictionary
        self.assertIn(conventional[-1],source_co2.keys())
        
if __name__ == '__main__':
    unittest.main()
