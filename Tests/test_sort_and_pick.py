import unittest
import pandas as pd
import numpy as np
import sys
sys.path.append('../EASE')

import ease

class TEST_sort_and_pick(unittest.TestCase):
    
    def test_sort_and_pick_output(self):
        
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[3,1]
        ts = test.iloc[3,2]
        tw = test.iloc[3,3]
        ws = test.iloc[3,4]
        vote = ease.rf(prec, ts, tw, ws)
        avg_cap = ease.avg_capacity(vote)
        possible_type = ease.possible_type(avg_cap)
        conv, clean = ease.clean_or_conv(possible_type)
        output_conv = ease.sort_and_pick(conv)
        output_clean = ease.sort_and_pick(clean)
        
        # test the type of output
        self.assertIsInstance(output_conv,list)
        self.assertIsInstance(output_clean,list)
        # test if output clean energy is in output convetional list
        conventional_list = ['Coal','NG','Petro']
        self.assertNotIn(output_clean[-1],conventional_list)
        #test the length of output
        self.assertEqual(len(output_conv),3)
        self.assertEqual(len(output_clean),3)
            
if __name__ == '__main__':
    unittest.main()
