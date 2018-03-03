# How Fast is Automation Reducing Available Jobs

##### I purposed this ^ question for my Python Data Visualization project. 
## What the data revealed is worth sharing.

According to the Bureau Labor of Statistics and Job Opening and Labor Turnover in 2016, of the 7,729,000 unemployed, 2,176,500<sup id="a1">[1](#f1)</sup> **did not** have an open position available to them. 
This 2016 estimate is less than the previous annual estimate. In 2015 2,981,834 unemployed people **did not** have a job available to them.

![BLS JOLTS Bar Chart](https://raw.githubusercontent.com/eclecticexistential/USPopulationNoJobAvailable/master/IMG/BLS.PNG)

BLS stats<sup id="a2">[2](#f2)</sup> only provide an age restriction of 16 and older. 
To identify the possible retirement age restriction, the Census population by age and state was analyzed.

Removing the BLS Employed and Institutionalized<sup id="a3">[3](#f3)</sup> population from the Census estimates reveals a much larger portion of the population without a job available to them. 
According to Census, BLS, and JOLTS data, 27,638,691 people **did not** have an open position available to them in 2016. 

![Census BLS JOLTS Bar Chart](https://raw.githubusercontent.com/eclecticexistential/USPopulationNoJobAvailable/master/IMG/Census.PNG)

Jupyter notebook pages reveal a regional breakdown of the BLS and Census stats on a map for both years. To-date, I am unable to discern whether or not the job shortage is directly related to automation.

*Manual steps to recreate results:*
1. Download the [Census](https://www.census.gov/data/datasets/2017/demo/popest/state-detail.html) dataset [here](https://www2.census.gov/programs-surveys/popest/datasets/2010-2016/state/asrh/sc-est2016-agesex-civ.csv) or look for the data named "Annual Estimates of the Civilian Population by Single Year of Age and Sex for the United States and States: April 1, 2010 to July 1, 2016".
2. Filter Census data by state and ages 16-67.
3. Grab table one from the Bureau Labor of Statistics Data [website](https://www.bls.gov/news.release/archives/srgune_02282017.htm).
4. Filter by regions: Northeast, West, South, Midwest
5. Get the Job Opening and Labor Turnover stats [here](https://download.bls.gov/pub/time.series/jt/jt.data.2.JobOpenings).
6. Filter by seasonally adjusted and all job categories, data comes in regions
7. Download cphalpert's handy census-regions [algorithm](https://github.com/cphalpert/census-regions/blob/master/us%20census%20bureau%20regions%20and%20divisions.csv)


## Data Guide


### <b id="f1">JOLTS</b> [data](https://download.bls.gov/pub/time.series/jt/jt.data.2.JobOpenings)

Information collected from 16,000 randomly selected nonfarm establishments, *drawn from a universe of approximately 8 million establishments* compiled as part of the Quarterly Census of Employment and Wages, or ES-202, program.

This code JTS000000NEJOL is used in the JOLTS dataset to seperate stats by region, industry, and seasonal.
* JT = series_id
* S = seasonally adjusted (compensates for seasonal employment/taking job elsewhere due to weather, taking additional job for holidays, etc.)
* 000000 = industry_code (all non-farm including private sector)
* NE = region_code (Northeast)
* JO =  dataelement_code (Job Openings)
* L = ratelevel_code (L is level meaning data is in a four digit number representing thousands)

### <b id="f2">BLS</b> stats Population, CLF, Emp, Unemp Inst [Data](https://www.bls.gov/news.release/archives/srgune_02282017.htm)

* Official national estimates obtained from Current Population Survey (CPS)
* Sample survey of households conducted for Bureau of Labor Statistics (BLS) by U.S. Census Bureau
* LAUS measures employed and unemployed based on place-of-residence basis
#### Employed regards any of the following: 
1. Did any work for pay/profit
2. Worked 15+ hours w/o pay
3. Not working currently on temporary or absent condition, regardless of whether or not paid

#### Unemployed regards any of the following:
1. Not working looking for work/available for work
2. Currently laid off

### <b id="f3">Civilian Non-Institutional</b>
* Population 16 years of age and older
* Not an inmate of an institution (penal, mental facilities, home for the aged, or not on active duty.
* Includes 10,827,000 disabled population unable to work between the [ages of 16-64](https://www.bls.gov/news.release/disabl.t01.htm).
