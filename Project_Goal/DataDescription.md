
**Data Sets:**

*CO2 emission*

Size - use years from 1990 to 2015

subcolumns are type of sources produce CO2 (3)

demensionalities are States, years, and type of sources generate CO2

rows are years, columns are states, and subcolumns are types including coal, petroleum products, and natural gas

*Weather*

size - use years from 1996 to 2015

For weather dataset, dimensionalities are states, year, wind speed, temperature, and precipitation

rows are year, columns are states, wind speed, temperature, and precipitation.

Financial Part:

[**1 Cost**]

**For conventional energy (coal/petroleum/natural gas)**

l  Main cost of generators (including installation, operation & maintenance)

2  Cost of fuel

**For clean energy (solar/wind/hydro)**

l  Solar (including main cost, tax,  per year: 2007-2015/per state/)

2  Wind (including average main cost of a specific state)

3  Hydro (including average main cost of a specific state)



[**2  Revenue**]

l  Numbers of customers 

2  Electricity Prices

3  Revenue



**Data Model**

Columns: Year, Type, CO2_Emission, Wind, Temperature, Precipitation, Main_Cost, Revenue, State, Zipcode

60% data for training random forest model;

20% data for testing;

20% data for validating

![alt tag](https://github.com/danielfather7/EASE-Project/blob/master/Project_Goal/initial%20matrix.png)


