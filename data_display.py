from display.display import Display

my_display = None
while(1):
  print('mode 0: colors depend on time, mode 1: colors depend on positions')
  mode = input('Enter a mode(0~1) or -1 to exit this program: ')
  mode = int(mode)
  
  if mode == 0:
    time = []
    start_time = input('Enter the start time, according to the format\nYYYY MM DD\n')
    time.append(start_time)
    end_time = input('Enter the end time, according to the format\nYYYY MM DD\n')
    time.append(end_time)
    pos = input('Enter a position(0~8) or -1 to exit this program: ')
    # Enter a number?
    try:
      pos = int(pos)
      if pos >= 0 and pos <= 8:
        pos_list = [pos]
        if my_display:
          my_display.reset()
        my_display = Display(pos_list, time)
        my_display.get_data()
        my_display.plt_scatter_time()
      elif pos == -1:
        if my_display:
          my_display.reset()
        break
      else:
        print('Invalid position, try again!')
    except ValueError as err:
      print('Invalid input, try again!')
    my_display.create_graph()

  elif mode == 1:
    pos_list = []
    time = []
    start_time = input('Enter the start time, according to the format\nYYYY MM DD\n')
    time.append(start_time)
    end_time = input('Enter the end time, according to the format\nYYYY MM DD\n')
    time.append(end_time)
    while True:
      pos = input('Enter a position(0~8) one by one until you enter -1 to plot the graph: ')
      pos = int(pos)
      if pos >= 0 and pos <= 8:
        pos_list.append(pos)
      if pos == -1:
        if my_display:
          my_display.reset()
        my_display = Display(pos_list, time)
        my_display.plt_figure()
        for i in range(len(pos_list)):
          my_display.get_data()
          my_display.plt_multiple_pos()
        my_display.create_graph()
        break

  elif mode == -1:
    if my_display:
      my_display.reset()
    break
