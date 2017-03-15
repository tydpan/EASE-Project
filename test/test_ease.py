import unittest
import pandas as pd

"""
import sys
sys.path.append('../EASE')
"""
import EASE.ease as ease

import os


class TEST_RF(unittest.TestCase):
    def test_rf_inputtrain(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'final_weater.csv')
        train = pd.read_csv(path)[[
            'State', 'TotalMonthlyPrecip', 'TempSummer',
            'TempWinter', 'Avgwindspeed']]
        # test if DC exists
        self.assertIn('DC', list(train.State))
        # test if there is nan in input data
        self.assertEqual(train.isnull().sum().sum(), 0)

    def test_rf_inputpara(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        # test the type of input data
        self.assertIsInstance(prec, (int, float))
        self.assertIsInstance(ts, (int, float))
        self.assertIsInstance(tw, (int, float))
        self.assertIsInstance(ws, (int, float))
        # test the limitation of input temperature
        self.assertGreater(110, ts)
        self.assertGreater(ts, tw)
        self.assertGreater(tw, -10)
        # test the limitation of input precipitation
        self.assertGreater(prec, 0)
        # test the limitation of input windspeed
        self.assertGreater(ws, 0)

    def test_rf_output(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        output = ease.rf(prec, ts, tw, ws)
        # test the type of output dataset
        self.assertIsInstance(output, dict)
        # test the output values
        for i in list(output.values()):
            self.assertTrue(i <= 1)
            self.assertTrue(i > 0)


class TEST_avg_capacity(unittest.TestCase):
    def test_avg_cap_input(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'average_plant_capacity.csv')
        average_plant_capacity = pd.read_csv(path)
        # test if there is nan in input dataframe
        self.assertEqual(average_plant_capacity.isnull().sum().sum(), 0)

    def test_avg_cap_output(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'average_plant_capacity.csv')
        average_plant_capacity = pd.read_csv(path)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        vote = ease.rf(prec, ts, tw, ws)
        output = ease.avg_capacity(vote)
        # test the type of output dataset
        self.assertIsInstance(output, list)
        # test the length of output dataset
        self.assertEqual(len(output), 6)


class TEST_possible_type(unittest.TestCase):
    def test_possible_type_input(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'average_plant_capacity.csv')
        cap_pop = pd.read_csv(path)
        # test if there is nan in input capacity dataframe
        self.assertEqual(cap_pop.isnull().sum().sum(), 0)

    def test_possible_type_output(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'average_plant_capacity.csv')
        average_plant_capacity = pd.read_csv(path)
        path = os.path.dirname(__file__)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        vote = ease.rf(prec, ts, tw, ws)
        avg_cap_list = ease.avg_capacity(vote)
        output = ease.possible_type(avg_cap_list)

        # test the type of output dataset
        self.assertIsInstance(output, list)

        # calculate how many conventional energy resource have been filtered
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

        # test if all the clean resources have been filtered out
        self.assertLess(len(filtered), 3)


class TEST_rf_fluctuation(unittest.TestCase):
    def test_rf_fluctuation_output(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        output = ease.rf_fluctuation(prec, ts, tw, ws)

        # test the type of output
        self.assertIsInstance(output, list)
        # test the length of output
        self.assertEqual(len(output), 3)
        # test fluctuation level
        std = output[1]
        self.assertLess(std, 0.01)


class TEST_rev_plot(unittest.TestCase):
    def test_rev_plot_input(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'Cost', 'Sale_CO2_tax.csv')
        esales = pd.read_csv(path, skiprows=1, names=['Year', 'Sale', 'CO2_tax'])
        path = os.path.dirname(__file__)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        capacity = 100000
        label = 'Try'
        e_type = 'conventional'
        # test if there exists nan in input dataframe
        self.assertEqual(esales.isnull().sum().sum(), 0)
        # test type of input capacity
        self.assertIsInstance(capacity, (int, float))
        # test type of input label
        self.assertIsInstance(label, str)
        # test if e_type exists
        e_type_list = ['conventional', 'clean', 'total']
        self.assertIn(e_type, e_type_list)


class TEST_avg_cost(unittest.TestCase):
    def test_avg_cost_input(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'Cost', 'df_cost.csv')
        cost = pd.read_csv(path)
        # test if there is nan in input dataframe
        self.assertEqual(cost.isnull().sum().sum(), 0)

    def test_avg_cost_output(self):
        path = os.path.dirname(__file__)
        path = os.path.join(path, 'Arranged_Data', 'Cost', 'df_cost.csv')
        cost = pd.read_csv(path)
        path = os.path.dirname(__file__)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        vote = ease.rf(prec, ts, tw, ws)
        output = ease.avg_cost(vote)
        # test the type of output
        self.assertIsInstance(output, dict)
        # test the output length
        self.assertLessEqual(len(output), 6)


class TEST_clean_or_conv(unittest.TestCase):
    def test_clean_or_conv(self):
        path = os.path.dirname(__file__)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[22, 1]
        ts = test.iloc[22, 2]
        tw = test.iloc[22, 3]
        ws = test.iloc[22, 4]
        vote = ease.rf(prec, ts, tw, ws)
        avg_capacity = ease.avg_capacity(vote)
        possible_type = ease.possible_type(avg_capacity)
        conv, clean = ease.clean_or_conv(possible_type)

        # test the type of input
        self.assertIsInstance(possible_type, list)
        # test the type of output
        self.assertIsInstance(conv, list)
        self.assertIsInstance(clean, list)
        # test the element type inside of clean list
        for i in range(len(clean)):
            self.assertIsInstance(clean[i][2], str)


class TEST_sort_and_pick(unittest.TestCase):
    def test_sort_and_pick_output(self):
        path = os.path.dirname(__file__)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[3, 1]
        ts = test.iloc[3, 2]
        tw = test.iloc[3, 3]
        ws = test.iloc[3, 4]
        vote = ease.rf(prec, ts, tw, ws)
        avg_cap = ease.avg_capacity(vote)
        possible_type = ease.possible_type(avg_cap)
        conv, clean = ease.clean_or_conv(possible_type)
        output_conv = ease.sort_and_pick(conv)
        output_clean = ease.sort_and_pick(clean)

        # test the type of output
        self.assertIsInstance(output_conv, list)
        self.assertIsInstance(output_clean, list)
        # test if output clean energy is in output convetional list
        conventional_list = ['Coal', 'NG', 'Petro']
        self.assertNotIn(output_clean[-1], conventional_list)
        # test the length of output
        self.assertEqual(len(output_conv), 3)
        self.assertEqual(len(output_clean), 3)


class TEST_suggest(unittest.TestCase):
    def test_suggest_output(self):
        path = os.path.dirname(__file__)
        path_test = os.path.join(path, 'Arranged_Data', 'test_dataset.csv')
        test = pd.read_csv(path_test)
        prec = test.iloc[0, 1]
        ts = test.iloc[0, 2]
        tw = test.iloc[0, 3]
        ws = test.iloc[0, 4]
        capacity = 5000
        vote = ease.rf(prec, ts, tw, ws)
        avg_cap = ease.avg_capacity(vote)
        possible_type_list = ease.possible_type(avg_cap)
        conventional, clean = ease.clean_or_conv(possible_type_list)
        conventional = ease.sort_and_pick(conventional)
        clean = ease.sort_and_pick(clean)

        source_co2 = {'Coal': 2133, 'Petro': 1700, 'NG': 1220}
        # test whether conventional type in source dictionary
        self.assertIn(conventional[-1], source_co2.keys())


if __name__ == '__main__':
    unittest.main()