import tkinter as tk
import math
import time

class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Analog Clock")
        self.canvas = tk.Canvas(root, width=400, height=450, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.clock_radius = 150
        self.hour_hand_length = 60
        self.minute_hand_length = 90
        self.second_hand_length = 100
        self.hour_hand = None
        self.minute_hand = None
        self.second_hand = None
        self.digital_time_display = None
        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.create_clock()
        self.update_clock()

        self.setup_controls()

    def setup_controls(self):
        control_frame = tk.Frame(self.root)
        control_frame.pack()

        self.start_stop_button = tk.Button(control_frame, text="Start", command=self.start_stop_stopwatch)
        self.start_stop_button.pack(side=tk.LEFT)
        tk.Button(control_frame, text="Reset Stopwatch", command=self.reset_stopwatch).pack(side=tk.LEFT)
        tk.Button(control_frame, text="Toggle Fullscreen", command=self.toggle_fullscreen).pack(side=tk.LEFT)

    def create_clock(self):
        self.canvas.create_oval(200 - self.clock_radius, 200 - self.clock_radius,
                                200 + self.clock_radius, 200 + self.clock_radius, outline="black", width=2)
        for i in range(1, 13):
            angle = math.radians(i * 30)
            x = 200 + self.clock_radius * math.sin(angle)
            y = 200 - self.clock_radius * math.cos(angle)
            self.canvas.create_text(x, y, text=str(i), font=("Helvetica", 12, "bold"), fill="black")

    def update_clock(self):
        self.canvas.delete("all")
        self.create_clock()

        current_time = time.localtime()
        second_angle = math.radians((current_time.tm_sec / 60) * 360 - 90)
        minute_angle = math.radians((current_time.tm_min / 60) * 360 - 90)
        hour_angle = math.radians(((current_time.tm_hour % 12) / 12) * 360 - 90) + \
                     math.radians(current_time.tm_min / 60 * 30)
        self.update_hand(self.second_hand, second_angle, self.second_hand_length, "red")
        self.update_hand(self.minute_hand, minute_angle, self.minute_hand_length, "blue")
        self.update_hand(self.hour_hand, hour_angle, self.hour_hand_length, "black")
        self.update_digital_time(current_time)
        if self.stopwatch_running:
            self.update_stopwatch()
        self.root.after(1000, self.update_clock)

    def update_hand(self, hand, angle, length, color):
        if hand is not None:
            self.canvas.delete(hand)
        x = 200 + length * math.sin(angle)
        y = 200 - length * math.cos(angle)
        hand = self.canvas.create_line(200, 200, x, y, width=2, fill=color)
        return hand

    def update_digital_time(self, current_time):
        if self.digital_time_display:
            self.canvas.delete(self.digital_time_display)
        time_str = time.strftime("%I:%M:%S %p", current_time)
        self.digital_time_display = self.canvas.create_text(200, 370, text=time_str, font=("Helvetica", 14), fill="black")

    def start_stop_stopwatch(self):
        if self.stopwatch_running:
            self.stopwatch_running = False
            self.start_stop_button.config(text="Start")
        else:
            self.stopwatch_running = True
            self.stopwatch_start_time = time.time()
            self.start_stop_button.config(text="Stop")

    def update_stopwatch(self):
        elapsed_time = time.time() - self.stopwatch_start_time
        stopwatch_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))
        self.canvas.delete("stopwatch_display")
        self.canvas.create_text(200, 420, text="Stopwatch: " + stopwatch_time_str, font=("Helvetica", 14), fill="black", tags="stopwatch_display")

    def reset_stopwatch(self):
        self.stopwatch_running = False
        self.stopwatch_start_time = None
        self.canvas.delete("stopwatch_display")
        self.start_stop_button.config(text="Start")

    def toggle_fullscreen(self):
        self.root.attributes("-fullscreen", not self.root.attributes("-fullscreen"))

if __name__ == "__main__":
    root = tk.Tk()
    analog_clock = AnalogClock(root)
    root.mainloop()
