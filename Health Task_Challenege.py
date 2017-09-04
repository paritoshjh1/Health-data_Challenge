# Health-data_Challenge
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "src"))

import pandas as pd
import numpy as np
import seaborn as sns
import importlib
import time
import datetime
import matplotlib.pyplot as plt
from scipy import stats as scipystats

from resources import RESOURCE_PATH
from stats import sleepStats
from util import utils
from util import plotting as mplot
from stats import combinedStats

dataFolder = "..\\..\\health task_data\\fitbit_analyzer\\dataDump"
#filepath =  RESOURCE_PATH + "\\unittest\\test_sleepStats.csv"
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.handlers[0].stream = sys.stdout
####### Load and Prepare Data ##############
start = time.time()
sleepData = utils.loadSleepData(dataFolder)
end = time.time()
print("Data loaded in {:.2f}s".format(end - start))
print("Loaded {} dataframes".format(len(sleepData)))
print("{} total entries".format(np.sum([df.size for df in sleepData])))
print("Sample from first dataframe:")
print(sleepData[0].head())
####### Generate and save stats to file #######
start = time.time()
basicAndTimingStats = sleepStats.generateStatsFrom(sleepData, sleepStats.STATS_NAME_BASIC_AND_TIMING)
end = time.time()
print("Computed basicAndTimingStats in {:.2f}s".format(end - start))
start = time.time()
intervalsStats = sleepStats.generateStatsFrom(sleepData, sleepStats.STATS_NAME_INTERVALS)
end = time.time()
print("Computed intervalsStats in {:.2f}s".format(end - start))
start = time.time()
intradayStats = sleepStats.generateStatsFrom(sleepData, sleepStats.STATS_NAME_INTRADAY)
end = time.time()
print("Computed intradayStats in {:.2f}s".format(end - start))
#print(basicAndTimingStats.head())
#print(intervalsStats.head())
#print(intradayStats.head())
today = datetime.date.today().strftime("%Y_%m_%d")
basicAndTimingStatsFilepath = "{}\\..\\basicAndTimingStats_{}.csv".format(dataFolder, today)
intervalsStatsFilepath = "{}\\..\\intervalStats_{}.csv".format(dataFolder, today)
intradayStatsFilepath = "{}\\..\\intradayStats_{}.csv".format(dataFolder, today)

basicAndTimingStats.reset_index().to_csv(basicAndTimingStatsFilepath, index=False)
intervalsStats.reset_index().to_csv(intervalsStatsFilepath, index=False)
intradayStats.reset_index().to_csv(intradayStatsFilepath, index=False)
########## Load previously exported stats and plots ####################
exportedDate = '2016_11_19'
stats = pd.read_csv("{}\\..\\basicAndTimingStats_{}.csv".format(dataFolder, exportedDate), 
                    parse_dates=['date', 'to_bed_time', 'wake_up_time'])
stats.head()
stats['day'] = stats['date'].dt.weekday
stats['month'] = stats['date'].dt.month
stats.groupby([stats['day'], stats['month']])["sleep_efficiency"].mean()
sns.set_context("poster")
#mplot.plotYearAndMonthStatsSleep(stats)
#mplot.plotPreliminaryStats(stats)
mplot.plotWeekdayStatsSleep(stats)
#mplot.plotWeekdayStatsByMonthSleep(stats)
#mplot.plotDailyStatsSleep(stats)
#mplot.plotMonthlyStatsSleep(stats)
intradayStats = pd.read_csv("{}\\..\\intradayStats_{}.csv".format(dataFolder, exportedDate))
intradayStats.drop("date", axis=1, inplace=True)
data = intradayStats.apply(pd.value_counts)
#mplot.plotSleepValueHeatmap(data, sleepValue=1)
normIntradayCountStats = sleepStats.normalizedIntradayCountStats(intradayStats)
centeredIntradayCountStats = sleepStats.centerIntradayCountStats(normIntradayCountStats)
#mplot.plotSleepValueHeatmap(centeredIntradayCountStats, sleepValue=1)
#################### Daily Stats #####################
#stats.set_index('date', inplace=True)
stats['sleep_efficiency_rol_mean'] = stats['sleep_efficiency'].rolling(center=False,window=20).mean()
stats['sleep_efficiency'].plot()
stats['sleep_efficiency_rol_mean'].plot()
sns.plt.show()
testData = stats['restless']
testData.resample('20D').mean().plot()
testData.plot()
sns.plt.show()

