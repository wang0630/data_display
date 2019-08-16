import json
import datetime as dt
import pytz
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

class Display():
  def __init__(self, pos, time):
    self.pos = pos
    taipei_tz = pytz.timezone('Asia/Taipei')
    self.start_time = dt.datetime.strptime(time[0], '%Y %m %d').replace(tzinfo=taipei_tz)
    self.end_time = dt.datetime.strptime(time[1], '%Y %m %d').replace(tzinfo=taipei_tz)
    self.index = 0

  def reset(self):
    self.pos = -1
    self.data = []
    plt.close()
  
  # Common functions
  def get_data_by_pos(self):
    r = requests.get(f'http://140.116.82.93:6800/campus/display/{ self.pos[self.index] }')
    # date field in self.data is the str of datetime
    # We need to convert it to timezone aware object first
    self.data = json.loads(r.text)
    for index, value in enumerate(self.data):
      # strptime() parse str of date according to the format given behind
      # It is still naive datetime object, meaning that it is unaware of timezone
      unaware = dt.datetime.strptime(value.get('date'),  '%a, %d %b %Y %H:%M:%S %Z')
      # Create a utc timezone
      utc_timezone = pytz.timezone('UTC')
      # make utc_unaware obj aware of timezone
      # Convert the given time directly to literally the same time with different timezone
      # For example: Change from 2019-05-19 07:41:13(unaware) to 2019-05-19 07:41:13+00:00(aware, tzinfo=UTC)
      utc_aware = utc_timezone.localize(unaware)
      # This can also do the same thing
      # Replace the tzinfo of an unaware datetime object to a given tzinfo
      # utc_aware = unaware.replace(tzinfo=pytz.utc)

      # Transform utc timezone to +8 GMT timezone
      # Convert the given time to the same moment of time just like performing timezone calculation
      # For example: Change from 2019-05-19 07:41:13+00:00(aware, tzinfo=UTC) to 2019-05-19 15:41:13+08:00(aware, tzinfo=Asiz/Taipei)
      taiwan_aware = utc_aware.astimezone(pytz.timezone('Asia/Taipei'))
      # print(f"{ index }: {unaware} {utc_aware} {taiwan_aware}")
      value['date'] = taiwan_aware
  
  def get_all_data(self):
    r = requests.get(f'http://140.116.82.93:6800/training')
    # date field in self.data is the str of datetime
    # We need to convert it to timezone aware object first
    self.data = json.loads(r.text)
    for index, value in enumerate(self.data):
      # strptime() parse str of date according to the format given behind
      # It is still naive datetime object, meaning that it is unaware of timezone
      unaware = dt.datetime.strptime(value.get('date'),  '%a, %d %b %Y %H:%M:%S %Z')
      # Create a utc timezone
      utc_timezone = pytz.timezone('UTC')
      # make utc_unaware obj aware of timezone
      # Convert the given time directly to literally the same time with different timezone
      # For example: Change from 2019-05-19 07:41:13(unaware) to 2019-05-19 07:41:13+00:00(aware, tzinfo=UTC)
      utc_aware = utc_timezone.localize(unaware)
      # This can also do the same thing
      # Replace the tzinfo of an unaware datetime object to a given tzinfo
      # utc_aware = unaware.replace(tzinfo=pytz.utc)

      # Transform utc timezone to +8 GMT timezone
      # Convert the given time to the same moment of time just like performing timezone calculation
      # For example: Change from 2019-05-19 07:41:13+00:00(aware, tzinfo=UTC) to 2019-05-19 15:41:13+08:00(aware, tzinfo=Asiz/Taipei)
      taiwan_aware = utc_aware.astimezone(pytz.timezone('Asia/Taipei'))
      # print(f"{ index }: {unaware} {utc_aware} {taiwan_aware}")
      value['date'] = taiwan_aware

  def set_data_cleaning(self):
    ans = input('Do you want to do data cleaning ? (y/n) ')
    if ans == 'y':
      self.data_cleaning = True
    else:
      self.data_cleaning = False

  # Mode 0  
  def print_recent_data(self):
    # Convert data to dataframe
    df = pd.DataFrame(self.data)
    # set the order of the columns
    df = df[['date', 'pm10', 'pm25', 'pm100', 'temp', 'humidity', 'position']]
    # set that display at most 300 rows in the dataframe
    pd.set_option('display.max_rows', 300)
    print(df.tail(300))

  def combine_df(self):
    df = pd.DataFrame(self.data)
    df = df.tail(15)
    # add position column in the dataframe
    df['pos'] = self.pos[self.index]
    if self.index == 0:
      self.df = df
    else:
      self.df = pd.concat([self.df, df])
    # increment the index value
    self.index = self.index + 1

  # Mode 1
  def plt_scatter_time(self):
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
    # Convert data to dataframe
    df = pd.DataFrame(self.data)
    color_arr = []
    for item in df['date']:
      if item.hour >= 6 and item.hour < 12:
        color_arr.append(1)
      elif item.hour >= 12 and item.hour < 18:
        color_arr.append(2)
      elif item.hour >= 18 and item.hour < 24:
        color_arr.append(3)
      else: # 00 ~ 06 early in the morning
        color_arr.append(0)
    # Set color_arr to the third column of df for colouring
    df['color'] = color_arr
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # plot scatter plot of which colors varying with time
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(12, 7))
    labels = ['0~6', '6~12', '12~18', '18~24']
    colors = ['navy', 'turquoise', 'darkorange', 'y']
    for i, dff in df.groupby('color'):
      ax.scatter(dff['date'], dff['pm25'], c=colors[i], label=labels[i])
    ax.set_xlim([self.start_time, self.end_time])
    plt.title('pm2.5 vs time at Position %d' % self.pos[0])
    plt.xlabel('time', fontsize=10)
    plt.xticks(rotation=45)
    plt.ylabel('pm2.5 (μg/m^3)')
    plt.legend(title='hour')
    plt.show()

  # Mode 2
  def plt_figure(self):
    plt.figure(figsize=(12, 7))
    plt.style.use('ggplot')

  def plt_multiple_pos(self):
    # convert data to dataframe
    df = pd.DataFrame(self.data)
    # Rename the names of columns
    df = df.rename(columns = {'pm10': 'pm1.0', 'pm25': 'pm2.5', 'pm100': 'pm10.0'})
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # Data cleaning
    if self.data_cleaning:
      df = df.loc[ df['pm2.5'] < 120 ]
      df = df.loc[ df['humidity'] <= 100 ]
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
    # Plot y versus x(time)
    colors = ['navy', 'turquoise', 'darkorange', 'olive', 'lightgray', 'pink', 'lightgreen', 'black']
    plt.plot(df['date'], df[self.y_name], label=self.pos[self.index], lw=1, ls='-') # marker = '.' , alpha=0.8
    self.index = self.index + 1

  def create_graph(self):
    if self.data_cleaning:
      plt.title('%s plot (after data cleaning)' % self.y_name)
    else:
      plt.title('%s plot' % self.y_name)
    plt.xlabel('Time', fontsize=10)
    plt.xticks(rotation=45)
    plt.ylabel('%s %s' % (self.y_name, self.y_unit))
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), title='position')
    plt.show()

  def choose_y(self):
    feature_dict = {0: 'pm1.0', 1: 'pm2.5', 2: 'pm10.0', 3: 'temp', 4: 'humidity'}
    unit_dict = {0: '(μg/m^3)', 1: '(μg/m^3)', 2: '(μg/m^3)', 3: '(°C)', 4: '(%)'}
    print(feature_dict)
    y_index = int(input('To choose y, input an integer(0~4): '))
    self.y_name = feature_dict[y_index]
    self.y_unit = unit_dict[y_index]
  
  # Mode 3
  def plt_multiple_features(self):
    # convert data to dataframe
    df = pd.DataFrame(self.data)
    # Rename the names of columns
    df = df.rename(columns = {'pm10': 'pm1.0', 'pm25': 'pm2.5', 'pm100': 'pm10.0'})
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # Data cleaning
    if self.data_cleaning:
      df = df.loc[ df['pm2.5'] < 120 ]
      df = df.loc[ df['humidity'] <= 100 ]
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
    # Plot y versus x(time)
    label = ['pm1.0', 'pm2.5', 'pm10.0', 'temp', 'humidity']
    # plot three subplots
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(20, 8))
    # subplot 1
    axes[0].plot(df['date'], df[label[0]], label=label[0], lw=1, ls='-')
    axes[0].plot(df['date'], df[label[1]], label=label[1], lw=1, ls='-')
    axes[0].plot(df['date'], df[label[2]], label=label[2], lw=1, ls='-')
    axes[0].set_ylabel('(μg/m^3)')
    axes[0].legend(loc='upper left', bbox_to_anchor=(1,1))
    # subplot 2
    axes[1].plot(df['date'], df[label[3]], label=label[3], lw=1, ls='-')
    axes[1].set_ylabel('temperature (°C)')
    # subplot 3
    axes[2].plot(df['date'], df[label[4]], label=label[4], lw=1, ls='-')
    axes[2].set_ylabel('humidity (%)')
    axes[2].set_xlabel('Time', fontsize=10)
    plt.xticks(rotation=45)
    # Fig
    fig.suptitle('Position %d data display' % self.pos[self.index])
    fig.show()

  # Mode 4
  def plt_corr(self):
    # convert data to dataframe
    df = pd.DataFrame(self.data)
    # Select position 0~7
    df = df.loc[ df['position'] <= 7 ]
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # rename the names of columns
    df = df.rename(columns = {'pm10': 'pm1.0', 'pm25': 'pm2.5', 'pm100': 'pm10.0'})
    # Data cleaning
    df = df.loc[ df['pm2.5'] < 120 ]
    df = df.loc[ df['humidity'] <= 100 ]
    # Add columns for month, day, weekday, hour_minute
    df['month'] = df['date'].apply(lambda x: x.month)
    df['day'] = df['date'].apply(lambda x: x.day)
    df['weekday'] = df['date'].apply(lambda x: x.weekday)
    df['hour_minute'] = df['date'].apply(lambda x: x.hour+x.minute/60)
    # Add a column that equals to hour_minute-shift_value
    shift_value = 11
    plus_value = 24 + shift_value
    column_name = 'hour_minute_minus%d' % shift_value
    df[column_name] = df['hour_minute'].apply(lambda x: x-shift_value)
    df[column_name] = df[column_name].apply(lambda x: x+plus_value if x<0 else x)
    # set the order of the columns
    df = df[['month', 'day', 'weekday', 'hour_minute', column_name, 'pm1.0', 'pm2.5', 'pm10.0', 'temp', 'humidity', 'position']]
    # compute the correlation
    corr = df.corr()
    # plot correlation matrix
    fig, ax = plt.subplots(figsize=(7, 7))
    sns.heatmap(corr, 
                xticklabels=corr.columns.values,
                yticklabels=corr.columns.values,
                vmax=0.9,
                square=True,
                annot=True,
                ax=ax,
                cmap='Spectral',
                linewidths=0.5)
    plt.title('Correlation between each feature (from %s/%s/%s to %s/%s/%s) (after data cleaning)' 
              % (self.start_time.year, self.start_time.month, self.start_time.day,
                 self.end_time.year, self.end_time.month, self.end_time.day))
    plt.show()

  # Mode 5
  def plt_boxplot(self):
    # convert data to dataframe
    df = pd.DataFrame(self.data)
    # Select position 0~7
    df = df.loc[ df['position'] <= 7 ]
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # rename the names of columns
    df = df.rename(columns = {'pm10': 'pm1.0', 'pm25': 'pm2.5', 'pm100': 'pm10.0'})
    # construct a new dataframe used to plot boxplot 1
    df_melt = pd.melt(df, id_vars=['position'], value_vars=['pm1.0', 'pm2.5', 'pm10.0'], var_name='Particulate Matter (PM)')
    # plot three boxplots
    fig, axes = plt.subplots(3, 1, sharex=True, figsize=(20, 8))
    # Boxplot 1
    ax = sns.boxplot(x='position', y='value', data=df_melt, hue='Particulate Matter (PM)', palette='Set3', ax=axes[0])
    ax.axis(ymin=0, ymax=50)
    ax.set_xlabel('')
    ax.set_ylabel('(μg/m^3)')
    ax.legend(loc='upper left', bbox_to_anchor=(1,1))
    # Boxplot 2
    ax = sns.boxplot(x='position', y='temp', data=df, color='orange', ax=axes[1])
    ax.axis(ymin=20, ymax=40)
    ax.set_xlabel('')
    ax.set_ylabel('temp(°C)')
    # Boxplot 3
    ax = sns.boxplot(x='position', y='humidity', data=df, color='cyan', ax=axes[2])
    ax.axis(ymin=15, ymax=100)
    ax.set_ylabel('humidity(%)')
    # Fig
    fig.suptitle('Boxplot (from %s/%s/%s to %s/%s/%s)' 
                 % (self.start_time.year, self.start_time.month, self.start_time.day,
                    self.end_time.year, self.end_time.month, self.end_time.day))
    fig.show()

  # Mode 6
  def plt_scatter(self):
    # convert data to dataframe
    df = pd.DataFrame(self.data)
    # Select position 0~7
    df = df.loc[ df['position'] <= 7 ]
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # rename the names of columns
    df = df.rename(columns = {'pm10': 'pm1.0', 'pm25': 'pm2.5', 'pm100': 'pm10.0'})
    # Add columns for hour_minute, weekday
    df['hour_minute'] = df['date'].apply(lambda x: x.hour+x.minute/60)
    df['weekday'] = df['date'].apply(lambda x: x.weekday)
    # set the order of the columns & discard some columns
    df = df[['hour_minute', 'pm1.0', 'pm2.5', 'pm10.0', 'temp', 'humidity', 'position', 'weekday']]
    # Data cleaning
    # want_cols = ['hour_minute', 'pm1.0', 'pm2.5', 'pm10.0', 'temp', 'humidity', 'weekday']
    # df = df[(np.abs(stats.zscore(df.loc[:, want_cols])) < 3).all(axis=1)]
    df = df.loc[ df['pm2.5'] < 120 ]
    df = df.loc[ df['humidity'] <= 100 ]
    # choose x, y
    feature_dict = {0: 'hour_minute', 1: 'pm1.0', 2: 'pm2.5', 3: 'pm10.0', 4: 'temp', 5: 'humidity', 6: 'position', 7: 'weekday'}
    unit_dict = {0: '(hr)', 1: '(μg/m^3)', 2: '(μg/m^3)', 3: '(μg/m^3)', 4: '(°C)', 5: '(%)', 6: '(position)', 7: ''}
    print(feature_dict)
    x_index = int(input('To choose x, input an integer: '))
    y_index = int(input('To choose y, input an integer: '))
    x_name = feature_dict[x_index]
    y_name = feature_dict[y_index]
    x_unit = unit_dict[x_index]
    y_unit = unit_dict[y_index]
    x = np.array(df[x_name])
    y = np.array(df[y_name])
    # plot scatter plot
    plt.figure(figsize=(12, 7))
    plt.style.use('ggplot')
    colors = np.array(df['position'])
    scatter = plt.scatter(x, y, c=colors, cmap='Spectral')
    plt.legend(*scatter.legend_elements(num=8), loc='upper left', bbox_to_anchor=(1,1), title='position')
    plt.xlabel('%s %s' % (x_name, x_unit))
    plt.ylabel('%s %s' % (y_name, y_unit))
    plt.title('Scatter plot (from %s/%s/%s to %s/%s/%s) (after data cleaning)' 
              % (self.start_time.year, self.start_time.month, self.start_time.day,
                 self.end_time.year, self.end_time.month, self.end_time.day))
    plt.show()

  # Mode 7
  def plt_scatter_one_pos(self):
    # convert data to dataframe
    df = pd.DataFrame(self.data)
    # Select the duration
    df = df.loc[ df['date'] >= self.start_time ]
    df = df.loc[ df['date'] <= self.end_time ]
    # rename the names of columns
    df = df.rename(columns = {'pm10': 'pm1.0', 'pm25': 'pm2.5', 'pm100': 'pm10.0'})
    # Add columns for hour_minute, weekday
    df['hour_minute'] = df['date'].apply(lambda x: x.hour+x.minute/60)
    df['weekday'] = df['date'].apply(lambda x: x.weekday)
    # set the order of the columns & discard some columns
    df = df[['hour_minute', 'pm1.0', 'pm2.5', 'pm10.0', 'temp', 'humidity', 'weekday']]
    # Data cleaning
    df = df.loc[df['pm2.5'] < 120]
    df = df.loc[df['humidity'] <= 100]
    # choose x, y
    feature_dict = {0: 'hour_minute', 1: 'pm1.0', 2: 'pm2.5', 3: 'pm10.0', 4: 'temp', 5: 'humidity', 6: 'position', 7: 'weekday'}
    unit_dict = {0: '(hr)', 1: '(μg/m^3)', 2: '(μg/m^3)', 3: '(μg/m^3)', 4: '(°C)', 5: '(%)', 6: '(position)', 7: ''}
    print(feature_dict)
    x_index = int(input('To choose x, input an integer: '))
    y_index = int(input('To choose y, input an integer: '))
    x_name = feature_dict[x_index]
    y_name = feature_dict[y_index]
    x_unit = unit_dict[x_index]
    y_unit = unit_dict[y_index]
    label = self.pos[0]
    x = np.array(df[x_name])
    y = np.array(df[y_name])
    # plot scatter plot
    plt.figure(figsize=(12, 7))
    plt.style.use('ggplot')
    scatter = plt.scatter(x, y, label=label)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), title='position')
    plt.xlabel('%s %s' % (x_name, x_unit))
    plt.ylabel('%s %s' % (y_name, y_unit))
    plt.title('Scatter plot (from %s/%s/%s to %s/%s/%s) (after data cleaning)' 
              % (self.start_time.year, self.start_time.month, self.start_time.day,
                 self.end_time.year, self.end_time.month, self.end_time.day))
    plt.show()
