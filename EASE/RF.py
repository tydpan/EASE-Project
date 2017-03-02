def RF(prec, ts, tw, ws):
    """
    This function is RandomForest classifier to intake user input temperature, precipitation, and windespeed to classify the possible states the user will be in, and returns a
    dictionary with states as the keys and the frequency or count as the values of each key.

       input = user input values, integer or float based.
       vote = dictionary based output that contains the RF classified states, and each states frequency.
       """
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import itertools as it
    import warnings

    train = pd.read_csv('../Arranged_Data/final_weater.csv')[[
            'State', 'TotalMonthlyPrecip', 'TempSummer', 
            'TempWinter', 'Avgwindspeed']]
    
    warnings.filterwarnings('ignore')
    
    input_ = [prec, ts, tw, ws]
    tree_num = 100
    pred_list = []
    vote = {}
    rf = RandomForestClassifier(n_estimators = tree_num)
    rf.fit(train.iloc[:,1:5], train.State)
    
    for i in range(tree_num):
        dt = rf.estimators_[i]
        dt.fit(train.iloc[:,1:5], train.State)
        pred = dt.predict(input_)
        pred_list.append(pred[0])

    pred_key = []
    pred_key_count = []
    for key, group in it.groupby(sorted(pred_list)):
        pred_key.append(key)
        pred_key_count.append(len(list(group)))

    for i in range(len(pred_key)):
        vote[pred_key[i]] = pred_key_count[i]/tree_num
    return vote
