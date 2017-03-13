import unittest
import pandas as pd
import numpy as np
import ease

class TEST_RF(unittest.TestCase):
    
    def test_rf_inputtrain(self):
        train = pd.read_csv('../Arranged_Data/final_weater.csv')[[
            'State', 'TotalMonthlyPrecip', 'TempSummer',
            'TempWinter', 'Avgwindspeed']]
        #test if DC exists
        self.assertIn('DC',list(train.State))
        #test if there is nan in input data
        self.assertEqual(train.isnull().sum().sum(),0)
        
    def test_rf_inputpara(self):
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        #test the type of input data
        self.assertIsInstance(prec,np.float64)
        self.assertIsInstance(ts,np.float64)
        self.assertIsInstance(tw,np.float64)
        self.assertIsInstance(ws,np.float64)
        #test the limitation of input temperature
        self.assertGreater(110, ts)
        self.assertGreater(ts, tw)
        self.assertGreater(tw,-10)
        #test the limitation of input precipitation
        self.assertGreater(prec, 0)
        #test the limitation of input windspeed
        self.assertGreater(ws, 0)
    
    def test_rf_output(self):
        test = pd.read_csv('../Arranged_Data/test_dataset.csv')
        prec = test.iloc[0,1]
        ts = test.iloc[0,2]
        tw = test.iloc[0,3]
        ws = test.iloc[0,4]
        output = ease.rf(prec, ts, tw, ws)
        #test the type of output dataset
        self.assertIsInstance(output,dict)
        #test the output values
        for i in list(output.values()):
            self.assertTrue(i < 1)
            self.assertTrue(i > 0)
                
if __name__ == '__main__':
    unittest.main()
