from display.display import Display

my_display = None
while(1):
  pos = input('Enter a position(0~7) or -1 to exit this program: ')
  # Enter a number?
  try:
    pos = int(pos)
    if pos >= 0 and pos <= 7:
      if my_display:
        my_display.reset()
      my_display = Display(pos)
      my_display.get_data()
      my_display.create_graph()
    elif pos == -1:
      if my_display:
        my_display.reset()
      break
    else:
      print('Invalid position, try again!')
  except ValueError as err:
    print('Invalid input, try again!')
