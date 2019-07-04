from display.display import Display

def input_time():
  time = []
  start_time = input('Enter the start time, according to the format\nYYYY MM DD\n')
  time.append(start_time)
  end_time = input('Enter the end time, according to the format\nYYYY MM DD\n')
  time.append(end_time)
  return time

def input_pos(multiple):
  if multiple == True:
    pos_list = []
    while True:
      pos = input('Enter a position(0~8) one by one until you enter -1 to plot the graph: ')
      # Enter a number?
      try:
        pos = int(pos)
        if pos >= 0 and pos <= 8:
          pos_list.append(pos)
        elif pos == -1:
          return pos_list
        else:
          print('Invalid number, try again!')
      except ValueError as err:
        print('Invalid input, try again!')
  # if `multiple` is not True
  while True:
    pos = input('Enter a position(0~8): ')
    # Enter a number?
    try:
      pos = int(pos)
      if pos >= 0 and pos <= 8:
        return [pos]
      else:
        print('Invalid number, try again!')
    except ValueError as err:
      print('Invalid input, try again!')

my_display = None
while(1):
  print('--------------------------------------')
  print('| mode 0: see recent data            |')
  print('| mode 1: colors depend on time      |')
  print('| mode 2: show multiple positions    |')
  print('| mode 3: show multiple features     |')
  print('| mode 4: show correlation           |')
  print('| mode 5: show boxplot               |')
  print('| mode 6: show scatter               |')
  print('--------------------------------------')
  mode = input('Enter a mode(0~6) or -1 to exit this program: ')
  mode = int(mode)
  
  if mode == 0:
    if my_display:
      my_display.reset()
    # Unused position
    pos_list = []
    # Unused time
    time = ['2020 02 02', '2020 02 03']
    # create a Display object
    my_display = Display(pos_list, time)
    # get and print recent data
    my_display.get_all_data()
    my_display.print_recent_data()
    break

  elif mode == 1:
    if my_display:
      my_display.reset()
    # input time & a position
    time = input_time()
    pos_list = input_pos(multiple=False)
    # create a Display object
    my_display = Display(pos_list, time)
    # plt
    my_display.get_data()
    my_display.plt_scatter_time()
    my_display.create_graph()

  elif mode == 2:
    if my_display:
      my_display.reset()
    # input time & multiple positions
    time = input_time()
    pos_list = input_pos(multiple=True)
    # create a Display object
    my_display = Display(pos_list, time)
    # plt
    my_display.plt_figure()
    for i in range(len(pos_list)):
      my_display.get_data()
      my_display.plt_multiple_pos()
    my_display.create_graph()
    
  elif mode == 3:
    if my_display:
      my_display.reset()
    # input time & a position
    time = input_time()
    pos_list = input_pos(multiple=False)
    # create a Display object
    my_display = Display(pos_list, time)
    # plt
    my_display.get_data()
    my_display.plt_multiple_features()
    my_display.create_graph()

  elif mode == 4:
    if my_display:
      my_display.reset()
    # Unused postion
    pos_list = []
    # Unused time
    time = ['2020 02 02', '2020 02 03']
    # create a Display object
    my_display = Display(pos_list, time)
    # plt
    my_display.get_all_data()
    my_display.plt_corr()

  elif mode == 5:
    if my_display:
      my_display.reset()
    # Unused postion
    pos_list = []
    # Unused time
    time = ['2020 02 02', '2020 02 03']
    # create a Display object
    my_display = Display(pos_list, time)
    # plt
    my_display.get_all_data()
    my_display.plt_boxplot()

  elif mode == 6:
    if my_display:
      my_display.reset()
    # Unused postion
    pos_list = []
    # Unused time
    time = ['2019 06 13', '2020 02 03']
    # create a Display object
    my_display = Display(pos_list, time)
    # plt
    my_display.get_all_data()
    my_display.plt_scatter()

  elif mode == -1:
    if my_display:
      my_display.reset()
    break
