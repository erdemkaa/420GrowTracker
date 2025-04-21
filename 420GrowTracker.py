import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
import json
import os

class GrowApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cannabis Grow Tracker")
        self.geometry("800x700")
        self.week_index = 0

        self.base_schedule = [
            {"Stage": "Sprout / Cotyledons", "EC": "0.6", "PPFD": "200", "VPD": "0.4 – 0.6", "Supplements": "Great White mist/gentle feed, Voodoo Juice", "pH": "5.8 – 6.0"},
            {"Stage": "2nd Set of Leaves", "EC": "0.8", "PPFD": "280", "VPD": "0.6 – 0.8", "Supplements": "Silica, Sensi Grow A+B, Great White, Cal-Mag, Voodoo Juice", "pH": "5.8 – 6.1"},
            {"Stage": "Veg Growth Begins", "EC": "1.0", "PPFD": "350", "VPD": "0.7 – 0.9", "Supplements": "Silica, Sensi Grow A+B, Bud Candy, Cal-Mag, Voodoo Juice" , "pH": "5.8 – 6.1"},
            {"Stage": "Late Veg / Pre-Flip", "EC": "1.3", "PPFD": "450", "VPD": "0.8 – 1.0", "Supplements": "Silica, Sensi Grow A+B, Bud Candy, Cal-Mag, Voodoo Juice", "pH": "5.8 – 6.1"},
            {"Stage": "Transition (Flip 12/12)", "EC": "1.5", "PPFD": "500", "VPD": "1.0 – 1.2", "Supplements": "Silica, Sensi Bloom A+B, Bud Candy, Great White, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Stretch Begins", "EC": "1.7", "PPFD": "600", "VPD": "1.1 – 1.3", "Supplements": "Silica, Sensi Bloom A+B, Big Bud, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Stretch Mid", "EC": "1.9", "PPFD": "650", "VPD": "1.2 – 1.4", "Supplements": "Sensi Bloom A+B, Big Bud, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Stretch Ends / Bud Set", "EC": "2.0", "PPFD": "700", "VPD": "1.2 – 1.4", "Supplements": "Sensi Bloom A+B, Big Bud, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Early Bud Build", "EC": "2.2", "PPFD": "750", "VPD": "1.3 – 1.5", "Supplements": "Sensi Bloom A+B, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Mid Bloom", "EC": "2.3", "PPFD": "800", "VPD": "1.3 – 1.5", "Supplements": "Sensi Bloom A+B, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Late Bloom (Swelling)", "EC": "2.4", "PPFD": "800", "VPD": "1.4 – 1.5", "Supplements": "Sensi Bloom A+B, Overdrive, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Final Feed Week", "EC": "2.4", "PPFD": "800", "VPD": "1.4 – 1.5", "Supplements": "Sensi Bloom A+B, Overdrive, Bud Candy, Cal-Mag", "pH": "5.8 – 6.2"},
            {"Stage": "Final Feed / Flush", "EC": "0.3", "PPFD": "0", "VPD": "0.8 – 1.2", "Supplements": "Water or Flush Solution (optional Flawless Finish)", "pH": "5.8 – 6.0"},
        ]

        self.actual_data = []
        if not self.load_data():
            self.create_setup_screen()
        else:
            self.show_week(self.week_index)

    def create_setup_screen(self):
        self.clear_window()
        ttk.Label(self, text="Strain Name:").pack()
        self.strain_entry = ttk.Entry(self)
        self.strain_entry.pack()

        ttk.Label(self, text="Sprouting Date (YYYY-MM-DD):").pack()
        self.sprout_entry = ttk.Entry(self)
        self.sprout_entry.pack()

        ttk.Label(self, text="Growing Medium:").pack()
        self.medium_var = tk.StringVar()
        self.medium_dropdown = ttk.Combobox(self, textvariable=self.medium_var, state="readonly")
        self.medium_dropdown["values"] = ["Coco", "Soil"]
        self.medium_dropdown.current(0)
        self.medium_dropdown.pack()

        ttk.Label(self, text="Veg Time (weeks):").pack()
        self.veg_time_var = tk.IntVar()
        self.veg_dropdown = ttk.Combobox(self, textvariable=self.veg_time_var, state="readonly")
        self.veg_dropdown["values"] = list(range(4, 9))
        self.veg_dropdown.current(2)
        self.veg_dropdown.pack()

        ttk.Label(self, text="Flower Time (days):").pack()
        self.flower_time_var = tk.IntVar()
        self.flower_dropdown = ttk.Combobox(self, textvariable=self.flower_time_var, state="readonly")
        self.flower_dropdown["values"] = [42, 49, 56, 63, 70, 77]
        self.flower_dropdown.current(3)
        self.flower_dropdown.pack()

        ttk.Button(self, text="Start Tracking", command=self.start_tracking).pack(pady=10)

    def start_tracking(self):
        try:
            self.strain = self.strain_entry.get()
            self.sprout_date = datetime.strptime(self.sprout_entry.get(), "%Y-%m-%d")
            self.medium = self.medium_var.get()
            self.veg_time = self.veg_time_var.get()
            self.flower_time = self.flower_time_var.get()
            self.build_schedule()
            self.actual_data = [{} for _ in range(len(self.weekly_schedule))]
            self.save_data()
            self.show_week(self.week_index)
        except ValueError:
            print("Please enter valid data.")

    def build_schedule(self):
        veg_weeks = self.veg_time
        flower_weeks = round(self.flower_time / 7)

        schedule = []
        schedule += self.base_schedule[:4]
        additional_veg = veg_weeks - 4
        schedule += [self.base_schedule[3]] * additional_veg
        schedule += self.base_schedule[4:10]
        additional_flower = flower_weeks - (len(self.base_schedule[4:10]))
        schedule += [self.base_schedule[9]] * max(0, additional_flower - 3)
        schedule += self.base_schedule[10:]
        self.weekly_schedule = schedule

    def show_week(self, index):
        self.clear_window()
        week_data = self.weekly_schedule[index]
        week_start = self.sprout_date + timedelta(weeks=index)
        week_end = week_start + timedelta(days=6)

        ttk.Label(self, text=f"Strain: {self.strain}", font=("Helvetica", 14, "bold")).pack(pady=5)
        ttk.Label(self, text=f"Medium: {self.medium} | Veg: {self.veg_time} weeks | Flower: {self.flower_time} days").pack()
        ttk.Label(self, text=f"Week {index} ({week_start.strftime('%b %d')} – {week_end.strftime('%b %d')})").pack(pady=10)
        ttk.Label(self, text=f"Stage: {week_data['Stage']}").pack()

        self.inputs = {}

        input_frame = ttk.LabelFrame(self, text="Recommended Values")
        input_frame.pack(pady=10)

        def get_ec_for_medium(ec_str):
            try:
                ec = float(ec_str)
                return f"{ec * 0.7:.1f}" if self.medium == "Soil" else ec_str
            except:
                return ec_str

        def get_ph_for_medium(ph_str):
            return "6.2 – 6.8" if self.medium == "Soil" else ph_str

        fields = [
            ("PPFD", week_data["PPFD"]),
            ("VPD", week_data["VPD"]),
            ("EC In", get_ec_for_medium(week_data["EC"])),
            ("EC Out", get_ec_for_medium(week_data["EC"])),
            ("pH In", get_ph_for_medium(week_data["pH"])),
            ("pH Out", get_ph_for_medium(week_data["pH"])),
        ]

        for i, (field, recommended) in enumerate(fields):
            label = ttk.Label(input_frame, text=f"{field} (Rec: {recommended}):", width=25, anchor="e")
            label.grid(row=i, column=0, padx=5, pady=3)
            entry = ttk.Entry(input_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=3)
            entry.insert(0, self.actual_data[index].get(field, ""))
            self.inputs[field] = entry

        supplements_frame = ttk.LabelFrame(self, text=f"Supplements (Recommended: {week_data['Supplements']})")
        supplements_frame.pack(pady=5)
        self.supplement_vars = {}
        supplements = [s.strip() for s in week_data["Supplements"].split(",")]
        actual_selected = self.actual_data[index].get("Supplements", [])

        for supp in supplements:
            var = tk.BooleanVar(value=supp in actual_selected)
            chk = ttk.Checkbutton(supplements_frame, text=supp, variable=var)
            chk.pack(anchor='w')
            self.supplement_vars[supp] = var

        notes_frame = ttk.LabelFrame(self, text="Notes")
        notes_frame.pack(pady=5, fill="x")
        self.notes_text = tk.Text(notes_frame, height=4, wrap=tk.WORD)
        self.notes_text.pack(fill="x")
        self.notes_text.insert("1.0", self.actual_data[index].get("Notes", ""))

        nav_frame = ttk.Frame(self)
        nav_frame.pack(side="bottom", fill="x", pady=10)

        ttk.Button(nav_frame, text="<< Previous Week", command=self.previous_week).pack(side=tk.LEFT, padx=10)
        if index < len(self.weekly_schedule) - 1:
            ttk.Button(nav_frame, text="Next Week >>", command=self.next_week).pack(side=tk.RIGHT, padx=10)

    def save_inputs(self):
        for key, entry in self.inputs.items():
            self.actual_data[self.week_index][key] = entry.get()

        selected_supps = [supp for supp, var in self.supplement_vars.items() if var.get()]
        self.actual_data[self.week_index]["Supplements"] = selected_supps
        self.actual_data[self.week_index]["Notes"] = self.notes_text.get("1.0", tk.END).strip()

    def next_week(self):
        self.save_inputs()
        if self.week_index < len(self.weekly_schedule) - 1:
            self.week_index += 1
            self.save_data()
            self.show_week(self.week_index)

    def previous_week(self):
        self.save_inputs()
        if self.week_index > 0:
            self.week_index -= 1
            self.save_data()
            self.show_week(self.week_index)

    def save_data(self):
        os.makedirs("data", exist_ok=True)
        data = {
            "strain": self.strain,
            "sprout_date": self.sprout_date.strftime("%Y-%m-%d"),
            "week_index": self.week_index,
            "medium": self.medium,
            "veg_time": self.veg_time,
            "flower_time": self.flower_time,
            "actual_data": self.actual_data,
        }
        with open(os.path.join("data", "grow_data.json"), "w") as f:
            json.dump(data, f, indent=2)

    def load_data(self):
        path = os.path.join("data", "grow_data.json")
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                self.strain = data["strain"]
                self.sprout_date = datetime.strptime(data["sprout_date"], "%Y-%m-%d")
                self.week_index = data["week_index"]
                self.medium = data.get("medium", "Coco")
                self.veg_time = data.get("veg_time", 6)
                self.flower_time = data.get("flower_time", 63)
                self.build_schedule()
                self.actual_data = data["actual_data"]
                if len(self.actual_data) < len(self.weekly_schedule):
                    self.actual_data += [{} for _ in range(len(self.weekly_schedule) - len(self.actual_data))]
                return True
        return False

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    app = GrowApp()
    app.mainloop()
    