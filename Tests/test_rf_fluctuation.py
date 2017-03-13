import unittest
import pandas as pd
import numpy as np
import ease

class TEST_rf_fluctuation(unittest.TestCase):
    
    def test_rf_fluctuation_output(self):
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        output = ease.rf_fluctuation(prec, ts, tw, ws)
        
        #test the type of output
        self.assertIsInstance(output,list)
        #test the length of output
        self.assertEqual(len(output),3) 
        #test fluctuation level
        std = output[1]
        self.assertLess(std, 0.01)

if __name__ == '__main__':
    unittest.main()
