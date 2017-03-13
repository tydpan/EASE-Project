import unittest
import pandas as pd
import numpy as np

import sys
sys.path.append('../EASE')
import ease

class TEST_clean_or_conv(unittest.TestCase):
    
    def test_clean_or_conv(self):
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[22,1]
        ts = test.iloc[22,2]
        tw = test.iloc[22,3]
        ws = test.iloc[22,4]
        vote = ease.rf(prec, ts, tw, ws)
        avg_capacity = ease.avg_capacity(vote)
        possible_type = ease.possible_type(avg_capacity)
        conv, clean = ease.clean_or_conv(possible_type)
        
        # test the type of input
        self.assertIsInstance(possible_type,list)
        # test the type of output
        self.assertIsInstance(conv,list)
        self.assertIsInstance(clean,list)
        # test the element type inside of clean list
        for i in range(len(clean)):
            self.assertIsInstance(clean[i][2],str)
        
if __name__ == '__main__':
    unittest.main()
