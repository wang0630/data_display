from display.display import Display

my_display = None
while(1):
  mode = input('Enter a mode(0~1) or -1 to exit this program: ')
  mode = int(mode)
  
  if mode == 0:
    pos = input('Enter a position(0~8) or -1 to exit this program: ')
    # Enter a number?
    try:
      pos = int(pos)
      if pos >= 0 and pos <= 8:
        pos_list = [pos]
        if my_display:
          my_display.reset()
        my_display = Display(pos_list)
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
    while True:
      pos = input('Enter a position(0~8) one by one until you enter -1 to plot the graph: ')
      pos = int(pos)
      if pos >= 0 and pos <= 8:
        pos_list.append(pos)
      if pos == -1:
        if my_display:
          my_display.reset()
        my_display = Display(pos_list)
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
