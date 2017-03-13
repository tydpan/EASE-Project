import unittest
import pandas as pd
import numpy as np

import sys
sys.path.append('../EASE')
import ease

class TEST_possible_type(unittest.TestCase):

    def test_possible_type_input(self):
        cap_pop = pd.read_csv('../Arranged_Data/average_plant_capacity.csv')
        #test if there is nan in input capacity dataframe
        self.assertEqual(cap_pop.isnull().sum().sum(),0)
        
    def test_possible_type_output(self):
        average_plant_capacity = pd.read_csv('../Arranged_Data/average_plant_capacity.csv')
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        vote = ease.rf(prec, ts, tw, ws)
        avg_cap_list = ease.avg_capacity(vote)
        output = ease.possible_type(avg_cap_list)
        
        #test the type of output dataset
        self.assertIsInstance(output,list)
        
        #calculate how many conventional energy resource have been filtered
        type_list = []
        for i in range(len(ease.possible_type(avg_cap_list))):
            type = ease.possible_type(avg_cap_list)[i][-1]
            type_list.append(type)
            conventional_ = ['Coal', 'NG', 'Petro']
        filtered = []
        for i in conventional_:
            if i in type_list:
                pass
            else:
                filtered.append(i)
                
        #test if all the clean resources have been filtered out
        self.assertLess(len(filtered),3)

if __name__ == '__main__':
    unittest.main()
