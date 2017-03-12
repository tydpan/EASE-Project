#!/usr/bin/pythons
#-*- coding: utf-8 -*-


def rf(prec, ts, tw, ws):
    """
    This function is RandomForest classifier to intake user input temperature,
    precipitation, and windespeed to classify the possible states the user
    will be in, and returns a dictionary with states as the keys and
    the frequency or count as the values of each key.

       input = user input values, integer or float based.
       vote  = dictionary based output that contains the RF classified states,
               and each states frequency.
    """
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import itertools as it
    import warnings

    train = pd.read_csv('../Arranged_Data/final_weater.csv')[[
            'State', 'TotalMonthlyPrecip', 'TempSummer',
            'TempWinter', 'Avgwindspeed']]
    train = train[train.State != 'DC']

    warnings.filterwarnings('ignore')

    input_ = [prec, ts, tw, ws]
    tree_num = 5000
    pred_list = []
    vote = {}
    rfc = RandomForestClassifier(n_estimators=tree_num)
    rfc.fit(train.iloc[:, 1:5], train.State)

    for i in range(tree_num):
        dt = rfc.estimators_[i]
        dt.fit(train.iloc[:, 1:5], train.State)
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


def avg_capacity(vote):
    """
    This function is to do weighted average of
    capacity per plant in each state based on our
    RandomForest classifier's result.
    """
    import pandas as pd

    average_plant_capacity = pd.read_csv(
            '../Arranged_Data/average_plant_capacity.csv')
    coal_sum = 0
    ng_sum = 0
    petro_sum = 0
    hydro_sum = 0
    solar_sum = 0
    wind_sum = 0
    for i in vote.keys():
        coal_sum += int(average_plant_capacity.Coal[
            average_plant_capacity.State == i]) * vote[i]
        ng_sum += int(average_plant_capacity.NG[
            average_plant_capacity.State == i]) * vote[i]
        petro_sum += int(average_plant_capacity.Petro[
            average_plant_capacity.State == i]) * vote[i]
        hydro_sum += int(average_plant_capacity.Hydro[
            average_plant_capacity.State == i]) * vote[i]
        solar_sum += int(average_plant_capacity.Solar[
            average_plant_capacity.State == i]) * vote[i]
        wind_sum += int(average_plant_capacity.Wind[
            average_plant_capacity.State == i]) * vote[i]
    return [coal_sum, ng_sum, petro_sum, hydro_sum, solar_sum, wind_sum]


def possible_type(avg_cap_list):
    """
    This function is to choose possible source type base on
    p value calculation, comparing to USA average and
    significance level (alpha) = 0.05.
    """
    import pandas as pd
    import numpy as np
    from scipy import stats

    cap_pop = pd.read_csv('../Arranged_Data/average_plant_capacity.csv')
    e_type = ['Coal', 'NG', 'Petro', 'Hydro', 'Solar', 'Wind']
    possible_type_list = []
    for i in range(len(e_type)):
        p_value = stats.ttest_1samp(
                cap_pop[cap_pop[e_type[i]] != 0][
                    e_type[i]], avg_cap_list[i])[1]
        alpha = 0.05  # confidence
        if avg_cap_list[i] < cap_pop[cap_pop[e_type[i]] != 0][
                e_type[i]].mean():
            if p_value < alpha:
                pass
            else:
                p_value = -(1 - p_value)
                possible_type_list.append(
                        [p_value, avg_cap_list[i], e_type[i]])
        else:
            p_value = (1 - p_value)
            possible_type_list.append(
                    [p_value, avg_cap_list[i], e_type[i]])
    if 'Coal' in list(np.array(possible_type_list)[:, 2]) or \
                    'NG' in list(np.array(possible_type_list)[:, 2]) or \
                    'Petro' in list(np.array(possible_type_list)[:, 2]):
        pass
    else:
        possible_type_list.append(
            [-1, avg_cap_list[0:3].max(), e_type[avg_cap_list.index(avg_cap_list[0:3].max())]])

    return possible_type_list


def rf_fluctuation(prec, ts, tw, ws):
    """
    creat a null list to store keys have maximun wt%
    creat a null list to store maximum wt% of corresponding keys
    for i in total run times
        select key which has maximum wt% and append key and its value to seperate null list
    return max wt%, std, keys
    """
    import numpy as np

    max_keys = []
    max_values = []
    for i in range(10):
        i = rf(prec, ts, tw, ws)
        max_i_value = max(i.values())
        max_key = max(i.keys(), key=(lambda k: i[k]))
        max_values.append(max_i_value)
        max_keys.append(max_key)
    return [max_values, np.std(max_values), max_keys]


def rev_plot(avg_cost, capacity, e_type, label, avg_cost_conv=0, capacity_conv=0):
    """
    if resource type is conventional, conventional revenue equals (sale - carbon dioxide tax - average cost) * capacity
    elseif resource type is clean, clean revenue equals (sale - average cost) * capacity
    elseif total revenue equals conventional revenue + clean revenue
    return plot
    """
    import pandas as pd
    import matplotlib.pyplot as plt
    import numpy as np

    revenue = 0
    esales = pd.read_csv('../Arranged_Data/Cost/Sale_CO2_tax.csv', skiprows=1, names=['Year', 'Sale', 'CO2_tax'])
    if e_type == 'conventional':
        revenue = (esales.Sale - esales.CO2_tax - avg_cost) * capacity / 1e6
    elif e_type == 'clean':
        revenue = (esales.Sale - avg_cost) * capacity / 1e6
    elif e_type == 'total':
        revenue = ((esales.Sale - avg_cost) * capacity + (
            esales.Sale - esales.CO2_tax - avg_cost_conv) * capacity_conv) / 1e6

    plt.plot(np.arange(2018, 2051), revenue[3:], label=label)
    plt.xlabel('Year')
    plt.ylabel('Money Save (million dollars / year)')
    plt.legend()
    plt.grid()
    return plt


def avg_cost(vote):
    """
    set original resources cost euqal to zero
    for state in vote keys
        average cost of resource =
                                average cost of particular resource in specific state * vote results of specific state
    creat a dictionary to store average cost for each type of resource
    return average cost dictionary
    """
    import pandas as pd

    cost = pd.read_csv('../Arranged_Data/Cost/df_cost.csv')
    coal_sum = 0
    ng_sum = 0
    petro_sum = 0
    hydro_sum = 0
    solar_sum = 0
    wind_sum = 0
    for i in vote.keys():
        coal_sum += int(cost.Coal[cost.State == i]) * vote[i]
        ng_sum += int(cost.NG[cost.State == i]) * vote[i]
        petro_sum += int(cost.Petro[cost.State == i]) * vote[i]
        hydro_sum += int(cost.Hydro[cost.State == i]) * vote[i]
        solar_sum += int(cost.solar[cost.State == i]) * vote[i]
        wind_sum += int(cost.WindCost[cost.State == i]) * vote[i]
    avg_cost_dict = {'Coal': coal_sum, 'NG': ng_sum, 'Petro': petro_sum, 'Hydro': hydro_sum, 'Solar': solar_sum,
                     'Wind': wind_sum}
    return avg_cost_dict


def clean_or_conv(possible_type_list):
    """
    initialize a null list to store conventional resource
    initialize a null list to store clean resource
    for some type in all types
        if type equals coal, natural gas, or petroleum, append it to conventional list
        elseif type equals hydro, soalr, or wind, append it to clean list
    retun conventional list, clean list
    """
    clean_list = []
    conventional_list = []
    for i in possible_type_list:
        if i[2] == 'Coal' or i[2] == 'NG' or i[2] == 'Petro':
            conventional_list.append(i)
        elif i[2] == 'Hydro' or i[2] == 'Solar' or i[2] == 'Wind':
            clean_list.append(i)
    return conventional_list, clean_list


def sort_and_pick(source_list):
    """"""
    source_list.sort()
    if len(source_list) == 3:
        ref = source_list[2]
        if abs(source_list[2][0] - source_list[1][0]) < 0.05 and abs(source_list[1][0] - source_list[0][0]) < 0.05:
            for i in source_list:
                if i[1] > ref[1]:
                    ref = i
        elif abs(source_list[2][0] - source_list[1][0]) < 0.05 and abs(source_list[1][0] - source_list[0][0]) >= 0.05:
            if source_list[1][1] > ref[1]:
                ref = source_list[1]
    elif len(source_list) == 2:
        ref = source_list[1]
        if abs(source_list[1][0] - source_list[0][0]) < 0.05:
            if source_list[0][1] > ref[1]:
                ref = source_list[0]
    elif len(source_list) == 1:
        ref = source_list[0]
    else:
        ref = []
    return ref


def suggest(prec, ts, tw, ws, capacity):
    """
    if no clean resource, clean revenue equals zero, calculate conventional capacity and plot revenue from conventional
    resource,
    else, electricity generated by clean resource greater or equal than client input capacity, plot revenue from clean
    resource.
        electricity generated by clean resource less than client input capacity, plot conventional revenue,
        clean revenue, and total revenue
    return clean revenue, conventional revenue, total revenue
    """
    import pandas as pd
    import matplotlib.pyplot as plt

    source_co2 = {'Coal': 2133, 'Petro': 1700, 'NG': 1220}
    state_vote = rf(prec, ts, tw, ws)
    cap = avg_capacity(state_vote)
    cost = avg_cost(state_vote)
    source_list = possible_type(cap)
    conventional, clean = clean_or_conv(source_list)
    conventional = sort_and_pick(conventional)
    clean = sort_and_pick(clean)
    df = pd.DataFrame()
    if len(conventional) == 0:

    if len(clean) == 0:
        capacity = min([conventional[1], capacity])
        revenue_clean = None
        revenue_conv = rev_plot(cost[conventional[2]], capacity, 'conventional', conventional[2])
        revenue_conv.title('Money Save using ' + conventional[2] + ' (capacity = ' + str(capacity) + ' Mwh)')
        revenue_total = None
    else:
        if clean[1] >= capacity:
            revenue_clean = rev_plot(cost[clean[2]], capacity, 'clean', clean[2])
            revenue_clean.title('Money Save using ' + clean[2] + ' (capacity = ' + str(capacity) + ' Mwh)')
            revenue_conv = None
            revenue_total = None
        else:
            plt.figure(1, figsize=(15, 8))
            plt.subplot(121)
            revenue_clean = rev_plot(cost[clean[2]], clean[1], 'clean',
                                     clean[2] + ' (capacity = ' + str(int(clean[1])) + ' Mwh)')
            revenue_conv = rev_plot(cost[conventional[2]], (capacity - clean[1]), 'conventional',
                                    conventional[2] + ' (capacity = ' + str(int(capacity - clean[1])) + ' Mwh)')
            revenue_total = rev_plot(cost[clean[2]], clean[1], 'total', 'Total (capacity = ' + str(capacity) + ' Mwh)',
                                     avg_cost_conv=cost[conventional[2]], capacity_conv=(capacity - clean[1]))
            revenue_total.title('Money Save using ' + clean[2] + ' Combined with ' + conventional[2])

            conversion_to_co2 = 0
            for k in conventional:
                if k in source_co2:
                    conversion_to_co2 = source_co2[k]

            print('Emitted Co2 using', conventional[2], 'is:',
                  int(capacity - clean[1]) * conversion_to_co2 * 0.000453592, 'metric tons')

            df['Year'] = [2016, 2050]
            df['CO2_emission'] = [3587231, capacity - clean[1] * conversion_to_co2 * 0.000453592]
            plt.subplot(122)
            co2_plot = plt.bar(df.Year, df.CO2_emission, width=12, color='#778899')
            plt.xticks(df.Year, ('2016', '2050'))
            plt.xlabel('Year')
            plt.ylabel('CO2 Emission (Metric Tons)')
            plt.grid(linestyle='dotted')
            plt.title('CO2 Emission with ' + conventional[2])
    return plt
