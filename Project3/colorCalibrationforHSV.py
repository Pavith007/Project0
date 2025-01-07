import tkinter as tk
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import time,cv2

import numpy as np
from subprocess import check_output
import pyautogui
from threading import Thread, Lock
once = True
img_screenshot = None
cam = cv2.VideoCapture(0)
class App:
    original_image = None
    hsv_image = None
    # switch to make sure screenshot not taken while already pressed
    taking_screenshot = False
    
    def __init__(self, master):
        self.img_path = None
        frame = tk.Frame(master)
        frame.grid()
        root.title("Sliders")
        
        self.hue_lbl = tk.Label(text="Hue", fg='red')
        self.hue_lbl.grid(row=2)

        self.low_hue = tk.Scale(master, label='Low',from_=0, to=179, length=500,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_hue.grid(row=3)

        self.high_hue = tk.Scale(master,label='High', from_=0, to=179, length=500,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_hue.set(179)
        self.high_hue.grid(row=4)
###########################################################################################################
        self.sat_lbl = tk.Label(text="Saturation", fg='green')
        self.sat_lbl.grid(row=5)

        self.low_sat = tk.Scale(master, label='Low',from_=0, to=255, length=500,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_sat.set(100)
        self.low_sat.grid(row=6)

        self.high_sat = tk.Scale(master, label="High", from_=0, to=255, length=500,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_sat.set(255)
        self.high_sat.grid(row=7)
###########################################################################################################
        self.val_lbl = tk.Label(text="Value", fg='Blue')
        self.val_lbl.grid(row=8)

        self.low_val = tk.Scale(master, label="Low",from_=0, to=255, length=500,orient=tk.HORIZONTAL, command=self.show_changes)
        self.low_val.set(100)
        self.low_val.grid(row=9)

        self.high_val = tk.Scale(master, label="High",from_=0, to=255, length=500,orient=tk.HORIZONTAL, command=self.show_changes)
        self.high_val.set(255)
        self.high_val.grid(row=10)

###########################################################################################################
# buttons
        #self.reset_btn = tk.Button(text='Reset', command=self.reset_values)
        #self.reset_btn.grid(row=1,column=1)

        self.print_btn = tk.Button(text='Print', command=self.print_values)
        self.print_btn.grid(row=2, column=1)

        self.reds = tk.Button(text="Reds", fg='red', command=self.preset_r)
        self.reds.grid(row=3, column=1)

        self.reds = tk.Button(text="Greens", fg='green', command=self.preset_g)
        self.reds.grid(row=4, column=1)

        self.reds = tk.Button(text="Blues", fg='blue', command=self.preset_b)
        self.reds.grid(row=5, column=1)

        # Open
        self.open_btn = tk.Button(text="Open", command=self.open_file)
        self.open_btn.grid(row=6, column=1)

        # Screenshot
        self.screenshot_btn = tk.Button(text="Screenshot", command=self.screenshot_standby)
        self.screenshot_btn.grid(row=7, column=1)
        # print mask array
        #self.print_mask_array_btn = tk.Button(text="Print Array", command=self.print_img_array)
        #self.print_mask_array_btn.grid(row=9, column=1)
###########################################################################################################
        # timer label
        self.screenshot_timer_lbl = tk.Label(text="Timer", fg='Red')
        self.screenshot_timer_lbl.grid(row=8, column=1)

########################################################################################################## Images
        # images
        self.hsv_img_lbl = tk.Label(text="HSV", image=None)
        self.hsv_img_lbl.grid(row=0, column=0)

        self.original_img_lbl = tk.Label(text='Original',image=None)
        self.original_img_lbl.grid(row=0, column=1)
##########################################################################################################
    def open_file(self):
        global once
        once = True
        #img_file = filedialog.askopenfilename()
        img_file = "input.jpg"
        print(img_file)
        # this makes sure you select a file
        # otherwise program crashes if not
        if img_file  != '':
            self.img_path = img_file 
            # this just makes sure the image shows up after opening it
            self.low_hue.set(self.low_hue.get()+1)
            self.low_hue.set(self.low_hue.get()-1)
        else:
            print('picked nothing')
            return 0

    def preset_r(self, *args):
        self.low_hue.set(0)
        self.high_hue.set(13)

        self.low_sat.set(100)
        self.high_sat.set(255)
        
        self.low_val.set(50)
        self.high_val.set(255)

    def preset_g(self, *args):
        self.low_hue.set(36)
        self.high_hue.set(90)

        self.low_sat.set(100)
        self.high_sat.set(255)

        self.low_val.set(50)
        self.high_val.set(255)

    def preset_b(self, *args):
        self.low_hue.set(80)
        self.high_hue.set(125)

        self.low_sat.set(100)
        self.high_sat.set(255)

        self.low_val.set(75)
        self.high_val.set(255)

    def show_changes(self, *args):
        global once, img_screenshot

        if self.img_path is None:
            print("Error: No image path provided.")
            return

    # Retrieve values from sliders
        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()
        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()

    # Ensure low values do not exceed high values
        if low_val > high_val or low_sat > high_sat or low_hue > high_hue:
            print("Error: Low values cannot exceed high values.")
            return

    # Set the original image once, manipulate the copy in subsequent iterations
        if once:
            if self.img_path != 'screenshot':
            # Capture image from the camera
                s, im = cam.read()
                if not s or im is None:
                    print("Error: Failed to read from the camera.")
                    return

                self.original_image = self.resize_image(im)
                if self.original_image is None:
                    print("Error: Failed to resize the image.")
                    return

                self.hsv_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)
            else:
            # Use the screenshot image
                if img_screenshot is None:
                    print("Error: No screenshot available.")
                    return

                self.original_image = img_screenshot
                self.hsv_image = cv2.cvtColor(img_screenshot, cv2.COLOR_BGR2HSV)

        # Convert original image to RGB and prepare it for display
            self.original_image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
            self.original_image = Image.fromarray(self.original_image)
            self.original_image = ImageTk.PhotoImage(self.original_image)
        
        # Update the original image label
            self.original_img_lbl.configure(image=self.original_image)
            self.original_img_lbl.image = self.original_image

        # Mark initialization complete
            once = False

    # Define the lower and upper HSV bounds for the mask
        lower_color = np.array([low_hue, low_sat, low_val])
        upper_color = np.array([high_hue, high_sat, high_val])

    # Create the mask
        mask = cv2.inRange(self.hsv_image, lower_color, upper_color)

    # Convert the mask to a PIL format image
        mask = Image.fromarray(mask)
        mask = ImageTk.PhotoImage(mask)

    # Update the HSV image label
        self.hsv_img_lbl.configure(image=mask)
        self.hsv_img_lbl.image = mask

    def reset_values(self,*args):
        self.low_hue.set(0)
        self.low_sat.set(100)
        self.low_val.set(100)

        self.high_hue.set(179)
        self.high_sat.set(255)
        self.high_val.set(255)

    def print_values(self,*args):
        """Does NOT actually save, just prints, for now"""
        print("Low = [{},{},{}]".format(self.low_hue.get(), self.low_sat.get(), self.low_val.get()))
        print("High= [{},{},{}]".format(self.high_hue.get(), self.high_sat.get(), self.high_val.get()))

    def screenshot_standby(self,*args):
        if not self.taking_screenshot:
            take_screenshot_thread = Thread(target=self.take_screenshot)
            take_screenshot_thread.start()
        else:
            return 0

    def take_screenshot(self,*args):
        global img_screenshot, once
        # switch to stop screenshot button from snaping a shot while snapping a shot
        self.taking_screenshot = True

        # switch to always display the screenshot as original everytime
        once = True

        # makes sure method 'show_changes' takes screenshot instead of img file
        self.img_path = 'screenshot'
        
        # starts a cound down timer of 3 seconds, parallel to the for loop
        screenshot_timer_thread = Thread(target=self.screenshot_timer_lbl_update)
        screenshot_timer_thread.start()
        for i in range(2):
            for _ in range(3):
                time.sleep(1)
            try:
               # sets the first point of screenshot 
                if i == 0:
                    x1,y1 = pyautogui.position()
               # sets the second point of screenshot 
                else:
                    x2,y2 = pyautogui.position()

            except Exception as e:
                print("ERROR: {}".format(e))
                print("{}{} {}{}\n".format(x1,y1,x2,y2))
                continue
        # exits if width and height are not greater than 0
        if x2 - x1 < 1 or y2 - y1 < 1:
            print("Retake Screenshot")
            print("Width={} Height={}".format(x2 - x1, y2 - y1))
            return
        # screenshot taken here with the grabbed coordinates
        try:
            #                                                top-leftpt, w & h   
            
            screenshoted_image = pyautogui.screenshot(region=(x1,y1,x2-x1,y2-y1))
            screenshoted_image = np.array(screenshoted_image)
        except Exception as e:
            print(e)
            print("Could not capture image")
            print("...coords passed pt1({},{}) pt2({},{})".format(x1,y1,x2,y2))
            return
        # converts the PIL image format to opencv2 image format
        img_screenshot = cv2.cvtColor(screenshoted_image, cv2.COLOR_RGB2BGR)
        # printing image array, by taking another screenshot and processing, effects will now show
        try:
            if args[0] == 'array':
                self.taking_screenshot = False
                return img_screenshot
        except:
            pass

        # resizes image if higher than 300px in width or height
        img_screenshot = self.resize_image(img_screenshot)

        # this just makes sure the image shows up after opening it
        self.low_hue.set(self.low_hue.get()+1)
        self.low_hue.set(self.low_hue.get()-1)
        # switch to allow for next screenshot
        self.taking_screenshot = False

    def screenshot_timer_lbl_update(self,*args):
        for _ in range(2):
            for i in range(3):
                self.screenshot_timer_lbl.config(text="{}".format(i+1))
                time.sleep(1)
        self.screenshot_timer_lbl.config(text="{}".format(" "))

    def resize_image(self,img,*args):
        # unpacks width, height
        height, width,_ = img.shape
        print("Original size: {} {}".format(width, height))
        count_times_resized = 0
        while width > 500 or height > 500:
        #if width > 300 or height > 300:
            # divides images WxH by half
            width = width / 2
            height = height /2
            count_times_resized += 1
        # prints x times resized to console
        if count_times_resized != 0:
            print("Resized {}x smaller, to: {} {}".format(count_times_resized*2,width, height))
        # makes sures image is not TOO small
        if width < 300 and height < 300:
            width = width * 2
            height = height * 2

        img = cv2.resize(img,(int(width),int(height)))

        return img

    def print_img_array(self):
        img = self.take_screenshot('array')
        #converts image to HSV 
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # gets the values from the sliders
        low_hue = self.low_hue.get()
        low_sat = self.low_sat.get()
        low_val = self.low_val.get()
        # gets upper values from sliders
        high_hue = self.high_hue.get()
        high_sat = self.high_sat.get()
        high_val = self.high_val.get()
        lower_color = np.array([low_hue,low_sat,low_val]) 
        upper_color= np.array([high_hue,high_sat,high_val])
        #creates the mask and result
        mask = cv2.inRange(self.hsv_image, lower_color, upper_color)
        mask = np.array(mask)
        mask.view


# Instance of Tkinter
root = tk.Tk()
# New tkinter instnace of app
app = App(root)
# loops over to keep window active
root.mainloop()
