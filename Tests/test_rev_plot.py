import unittest
import pandas as pd
import numpy as np

import sys
sys.path.append('../EASE')
import ease

class TEST_rev_plot(unittest.TestCase):
    
    def test_rev_plot_input(self):
        esales = pd.read_csv('../Arranged_Data/Cost/Sale_CO2_tax.csv', skiprows= 1, names = ['Year', 'Sale', 'CO2_tax']) 
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        capacity = 100000
        label = 'Try'
        e_type = 'conventional'
        # test if there exists nan in input dataframe
        self.assertEqual(esales.isnull().sum().sum(),0)
        # test type of input capacity 
        self.assertIsInstance(capacity,(int,float))
        # test type of input label
        self.assertIsInstance(label,str)
        # test if e_type exists
        e_type_list = ['conventional','clean','total']
        self.assertIn(e_type,e_type_list)
        
if __name__ == '__main__':
    unittest.main()
