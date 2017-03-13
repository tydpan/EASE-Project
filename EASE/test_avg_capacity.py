import unittest
import pandas as pd
import numpy as np
import ease

class TEST_avg_capacity(unittest.TestCase):
    
    def test_avg_cap_input(self):
        average_plant_capacity = pd.read_csv('../Arranged_Data/average_plant_capacity.csv')
        #test if there is nan in input dataframe
        self.assertEqual(average_plant_capacity.isnull().sum().sum(),0)
    
    def test_avg_cap_output(self):
        average_plant_capacity = pd.read_csv('../Arranged_Data/average_plant_capacity.csv')
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        vote = ease.rf(prec, ts, tw, ws)
        output = ease.avg_capacity(vote)
        #test the type of output dataset
        self.assertIsInstance(output,list)
        #test the length of output dataset
        self.assertEqual(len(output),6) 
if __name__ == '__main__':
    unittest.main()
