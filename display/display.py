import json
import datetime as dt
import pytz
import requests
import matplotlib.pyplot as plt
import pandas as pd

class Display():
  def __init__(self, pos, time):
    self.pos = pos
    taipei_tz = pytz.timezone('Asia/Taipei')
    self.start_time = dt.datetime.strptime(time[0], '%Y %m %d').replace(tzinfo=taipei_tz)
    self.end_time = dt.datetime.strptime(time[1], '%Y %m %d').replace(tzinfo=taipei_tz)
    self.index = 0
  def get_data(self):
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
  def plt_scatter_time(self):
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
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
    df = df.loc[ df['date'] > self.start_time ]
    df = df.loc[ df['date'] < self.end_time ]
    plt.figure(figsize=(400, 10))
    labels = ['0~6', '6~12', '12~18', '18~24']
    colors = ['navy', 'turquoise', 'darkorange', 'y']
    for i, dff in df.groupby('color'):
      plt.scatter(dff['date'], dff['pm25'], c=colors[i], label=labels[i])
  def create_graph(self):
    plt.title('pm2.5 plot')
    plt.xlabel('Date', fontsize=10)
    plt.xticks(rotation=45)
    plt.ylabel('pm2.5 (μg/m^3)')
    plt.legend()
    plt.show()
  def reset(self):
    self.pos = -1
    self.data = []
    plt.close()

  def plt_figure(self):
    plt.figure(figsize=(400, 10))

  def plt_multiple_pos(self):
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
    df = pd.DataFrame(self.data)
    # Select the duration
    df = df.loc[ df['date'] > self.start_time ]
    df = df.loc[ df['date'] < self.end_time ]
    # Plot y versus x(time)
    colors = ['navy', 'turquoise', 'darkorange', 'olive', 'lightgray', 'pink', 'lightgreen']
    label = 'position %d' % self.pos[self.index]
    plt.plot(df['date'], df['pm25'], c=colors[self.index], label=label, lw=1, ls='-', marker = '.', alpha=0.8)
    self.index = self.index + 1
  def plt_same_pos(self):
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
    df = pd.DataFrame(self.data)
    # Select the duration
    df = df.loc[ df['date'] > self.start_time ]
    df = df.loc[ df['date'] < self.end_time ]
    # Plot y versus x(time)
    colors = ['navy', 'turquoise', 'darkorange', 'olive', 'lightgray', 'pink', 'lightgreen']
    label = ['pm10', 'pm25', 'pm100', 'temp', 'humidity']
    label_display = ['pm1.0', 'pm2.5', 'pm10.0', 'temperature', 'humidity']
    plt.plot(df['date'], df[label[0]], c=colors[0], label=label_display[0], lw=1, ls='-', marker = '.', alpha=0.8)
    plt.plot(df['date'], df[label[1]], c=colors[1], label=label_display[1], lw=1, ls='-', marker = '.', alpha=0.8)
    plt.plot(df['date'], df[label[2]], c=colors[2], label=label_display[2], lw=1, ls='-', marker = '.', alpha=0.8)
    plt.plot(df['date'], df[label[3]], c=colors[3], label=label_display[3], lw=1, ls='-', marker = '.', alpha=0.8)
    plt.plot(df['date'], df[label[4]], c=colors[4], label=label_display[4], lw=1, ls='-', marker = '.', alpha=0.8)
    self.index = self.index + 1

  def plt_multiple_pos_10(self):
    # Add explicitly converter
    pd.plotting.register_matplotlib_converters()
    df = pd.DataFrame(self.data)
    # Select the duration
    df = df.loc[ df['date'] > self.start_time ]
    df = df.loc[ df['date'] < self.end_time ]

    print(df)
    # Plot y versus x(time)
    colors = ['navy', 'turquoise', 'darkorange', 'olive', 'lightgray', 'pink', 'lightgreen']
    label = 'position %d' % self.pos[self.index]
    plt.plot(df['date'], df['pm25'], c=colors[self.index], label=label, lw=1, ls='-', marker = '.', alpha=0.8)
    self.index = self.index + 1

  def combine_df(self):
    df = pd.DataFrame(self.data)
    df = df.tail(10)
    df['pos'] = self.index
    if self.index == 0:
      self.df = df
    else:
      self.df = pd.concat([self.df, df])
    self.index = self.index + 1
    
  def print_recent_data(self):
    self.df.sort_values(by='date', inplace=True)
    print(self.df.tail(60))
    