import unittest
import pandas as pd
import numpy as np
import ease

class TEST_avg_cost(unittest.TestCase):
    
    def test_avg_cost_input(self):
        cost = pd.read_csv('../Arranged_Data/Cost/df_cost.csv')
        #test if there is nan in input dataframe
        self.assertEqual(cost.isnull().sum().sum(),0)
        
    def test_avg_cost_output(self):
        cost = pd.read_csv('../Arranged_Data/Cost/df_cost.csv')
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        vote = ease.rf(prec, ts, tw, ws)
        output = ease.avg_cost(vote)
        # test the type of output
        self.assertIsInstance(output,dict)
        # test the output length
        self.assertLessEqual(len(output),6)
        
if __name__ == '__main__':
    unittest.main()
