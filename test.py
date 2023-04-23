from tkinter import *

root = Tk()
root.title("Traffic Light")

light_status = StringVar()
light_status.set("off")
unregulated = False
current_id = -1
stage = 0

timings = [
    [1500, lambda: yellow_label.config(bg="yellow")],
    [1500, lambda: red_label.config(bg="black")],
    [0, lambda: yellow_label.config(bg="black")],
    [0, lambda: green_label.config(bg="green")],
    [1500, lambda: green_label.config(bg="black")],
    [0, lambda: yellow_label.config(bg="yellow")],
    [1500, lambda: yellow_label.config(bg="black")],
    [0, lambda: red_label.config(bg="red")]
]

def if_light_status_on():
    if light_status.get() == "on":
        global stage
        root.after_cancel(current_id)
        timings[stage][1]()
        stage += 1
        stage %= len(timings)
        change_traffic_light()

def change_traffic_light():
    if light_status.get() == "on":
        global current_id
        current_id = root.after(timings[stage][0], if_light_status_on)


def toggle_traffic_light():
    red_label.config(bg="black")
    yellow_label.config(bg="black")
    green_label.config(bg="black")
    root.after_cancel(current_id)
    global stage
    stage = 0

    if light_status.get() == "on":
        light_status.set("off")
    else:
        light_status.set("on")
        red_label.config(bg="red")
        change_traffic_light()


def toggle_unregulated():
    global unregulated
    global current_id
    global stage
    if light_status.get() == "off":
        return

    root.after_cancel(current_id)
    if unregulated:
        unregulated = False
        yellow_label.config(bg="yellow")
        stage = 1
        change_traffic_light()
    else:
        unregulated = True
        red_label.config(bg="black")
        yellow_label.config(bg="black")
        green_label.config(bg="black")
        current_id = root.after(1000, blink_yellow)


def blink_yellow():
    if light_status.get() == "on" and unregulated:
        yellow_label.config(bg="yellow")
        root.after(500, lambda: yellow_label.config(bg="black"))
        root.after(1000, blink_yellow)


# create GUI
traffic_frame = Frame(root, bd=5, relief=RIDGE)
traffic_frame.pack(side=TOP)

red_label = Label(traffic_frame, bg="black", width=10, height=5)
red_label.pack(side=LEFT, padx=5, pady=5)

yellow_label = Label(traffic_frame, bg="black", width=10, height=5)
yellow_label.pack(side=LEFT, padx=5, pady=5)

green_label = Label(traffic_frame, bg="black", width=10, height=5)
green_label.pack(side=LEFT, padx=5, pady=5)

control_frame = Frame(root)
control_frame.pack(side=TOP)

toggle_button = Button(control_frame, text="On/Off", command=toggle_traffic_light)
toggle_button.pack(side=LEFT, padx=5, pady=5)

unregulated_button = Button(control_frame, text="Unregulated", command=toggle_unregulated)
unregulated_button.pack(side=LEFT, padx=5, pady=5)

root.mainloop()