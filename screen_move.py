import pyautogui
import pygetwindow as pgw
import os





def get_action_num(old_cx, old_cy, new_cx, new_cy, width, height, num_fingers):
	MOVE_LEFT = 1
	MOVE_RIGHT = 2
	MOVE_DOWN = 4
	MOVE_UP = 5
	MOVE_FINGER = 6
	hori_tol = 150
	vert_tol = 120
	action = -1

	if(num_fingers < 2):
		action = (MOVE_FINGER, new_cx, new_cy)
	else:
		if(abs(new_cx - old_cx) > hori_tol):
			if(new_cx > old_cx):
				action = MOVE_RIGHT
			else:
				action = MOVE_LEFT
		elif(abs(new_cy - old_cy) > vert_tol):
			if(new_cy > old_cy):
				action = MOVE_DOWN
			else:
				action = MOVE_UP
		else:
			pass
	return action








def execute_action(action_num, center_x, center_y, prev_window):
	"""
	Executes an action given an action number and the coordinates
	of the hand. 
	"""
	SHUT_DOWN = 0
	LOCK = 1
	CLOSE = 2
	ACTIVATE = 3
	MINIMIZE = 4
	MAXIMIZE = 5
	MOVE = 6
	RESTORE = 7

	width = 650
	height = 400

	screen_width = 1920
	screen_height = 1080

	window_list = pgw.getAllWindows()
	curr_window = pgw.getActiveWindow()
	target_list = pgw.getWindowsAt(round(center_x/width*screen_width), round(center_y/height * screen_height))
	target_window = curr_window
	if(len(target_list) != 0):
		target_window = target_list[0]

	if(action_num == SHUT_DOWN):
		os.system("shutdown /p")
	elif(action_num == LOCK):
		winpath = os.environ["windir"]
		os.system(winpath + r'\system32\rundll32 user32.dll, LockWorkStation')
	elif(action_num == CLOSE):
		curr_window.close()
	elif(action_num == ACTIVATE):
		target_window.activate()
	elif(action_num == MINIMIZE):
		curr_window.minimize()
	elif(action_num == MAXIMIZE):
		curr_window.maximize()
	elif(action_num == MOVE):
		curr_window.moveTo(center_x, center_y)
	elif(action_num == RESTORE):
		prev_window.restore()
	else:
		pass
	prev_window = pgw.getActiveWindow()
	return prev_window

