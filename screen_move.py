import pyautogui
import pygetwindow as pgw
import os


### Using os ###
#os.system("shutdown /p")



### Using pyauto gui ###

pyautogui.FAILSAFE = False
# Top left corner
# pyautogui.moveTo(0, 0, duration = 0)

# Top right corner
pyautogui.moveTo(1780, 10, duration = 0)

(width, height) = pyautogui.size()
print(width, height)
minimize_ratio_w = 140/1920
minimize_ratio_h = 10/1080

min_margin_w = minimize_ratio_w * width
min_margin_h = minimize_ratio_h * height


# pyautogui.click(width - min_margin_w, min_margin_h)





### Using pygetwindow ###


window_list = pgw.getAllWindows()
window_titles = pgw.getAllTitles()
print(window_titles)


window = window_list[9]

# desktopWindow = gw.getWindowsWithTitle('Between')[0]

# for window in window_list:
#     window.minimize()

# for window in window_list:
#     window.maximize()