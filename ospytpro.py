import tkinter as tk
from tkinter import messagebox, ttk

class EnergyEfficientCPUScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Energy-Efficient CPU Scheduling")

        tk.Label(root, text="Number of Processes:").pack()
        self.process_count_entry = tk.Entry(root)
        self.process_count_entry.pack()
        tk.Button(root, text="Set Processes", command=self.create_process_entries).pack()

        self.process_frame = tk.Frame(root)
        self.process_frame.pack()

        tk.Button(root, text="Run Energy-Efficient Scheduling", command=self.run_scheduling).pack()
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        
        self.table_frame = tk.Frame(root)
        self.table_frame.pack()

    def create_process_entries(self):
        for widget in self.process_frame.winfo_children():
            widget.destroy()
        
        try:
            self.num_processes = int(self.process_count_entry.get())
            if self.num_processes <= 0:
                raise ValueError("Number of processes must be positive.")

            tk.Label(self.process_frame, text="Arrival Time").grid(row=0, column=1)
            tk.Label(self.process_frame, text="Burst Time").grid(row=0, column=2)
            tk.Label(self.process_frame, text="Energy Consumption").grid(row=0, column=3)

            self.arrival_entries = []
            self.burst_entries = []
            self.energy_entries = []

            for i in range(self.num_processes):
                tk.Label(self.process_frame, text=f"P{i+1}").grid(row=i+1, column=0)
                at_entry = tk.Entry(self.process_frame, width=5)
                bt_entry = tk.Entry(self.process_frame, width=5)
                energy_entry = tk.Entry(self.process_frame, width=5)
                
                at_entry.grid(row=i+1, column=1)
                bt_entry.grid(row=i+1, column=2)
                energy_entry.grid(row=i+1, column=3)
                
                self.arrival_entries.append(at_entry)
                self.burst_entries.append(bt_entry)
                self.energy_entries.append(energy_entry)
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number of processes.")

    def run_scheduling(self):
        try:
            arrival_times = [int(at.get()) for at in self.arrival_entries]
            burst_times = [int(bt.get()) for bt in self.burst_entries]
            energy_consumption = [int(en.get()) for en in self.energy_entries]
            
            # Sort by energy efficiency (lower energy per burst time first)
            processes = sorted(zip(energy_consumption, arrival_times, burst_times), key=lambda x: x[0] / x[2])
            sorted_energy, sorted_at, sorted_bt = zip(*processes)
            
            waiting_time = [0] * self.num_processes
            turnaround_time = [0] * self.num_processes
            completion_time = [0] * self.num_processes
            
            completion_time[0] = sorted_at[0] + sorted_bt[0]
            for i in range(1, self.num_processes):
                completion_time[i] = max(completion_time[i-1], sorted_at[i]) + sorted_bt[i]
                waiting_time[i] = completion_time[i-1] - sorted_at[i]
                turnaround_time[i] = waiting_time[i] + sorted_bt[i]
            
            avg_wt = sum(waiting_time) / self.num_processes
            avg_tat = sum(turnaround_time) / self.num_processes
            avg_energy = sum(sorted_energy) / self.num_processes
            
            self.result_label.config(text=f"Avg Waiting Time: {avg_wt:.2f}\nAvg Turnaround Time: {avg_tat:.2f}\nAvg Energy Consumption: {avg_energy:.2f}")
            self.display_table(sorted_at, sorted_bt, sorted_energy, waiting_time, turnaround_time)
        except ValueError:
            messagebox.showerror("Error", "Enter valid integer values.")

    def display_table(self, arrival_times, burst_times, energy_consumption, waiting_times, turnaround_times):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        columns = ("Process", "Arrival Time", "Burst Time", "Energy Consumption", "Waiting Time", "Turnaround Time")
        table = ttk.Treeview(self.table_frame, columns=columns, show="headings")

        for col in columns:
            table.heading(col, text=col)
            table.column(col, width=100, anchor="center")

        for i in range(len(arrival_times)):
            table.insert("", "end", values=(f"P{i+1}", arrival_times[i], burst_times[i], energy_consumption[i], waiting_times[i], turnaround_times[i]))

        table.pack()

root = tk.Tk()
app = EnergyEfficientCPUScheduler(root)
root.mainloop()
