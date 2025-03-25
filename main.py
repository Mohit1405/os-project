import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class CPUScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        
        self.process_label = tk.Label(root, text="Enter Process Burst Times (Space-Separated):")
        self.process_label.pack()

        self.input_entry = tk.Entry(root, width=50)
        self.input_entry.pack()

        self.algorithm_label = tk.Label(root, text="Choose Scheduling Algorithm:")
        self.algorithm_label.pack()

        self.algorithm = tk.StringVar()
        self.algorithm.set("FCFS")

        self.fcfs_radio = tk.Radiobutton(root, text="FCFS", variable=self.algorithm, value="FCFS")
        self.fcfs_radio.pack()

        self.sjf_radio = tk.Radiobutton(root, text="SJF", variable=self.algorithm, value="SJF")
        self.sjf_radio.pack()

        self.rr_radio = tk.Radiobutton(root, text="Round Robin", variable=self.algorithm, value="RR")
        self.rr_radio.pack()

        self.run_button = tk.Button(root, text="Run Simulation", command=self.run_simulation)
        self.run_button.pack()

        self.output_text = tk.Text(root, width=60, height=10)
        self.output_text.pack()

    def run_simulation(self):
        try:
            processes = list(map(int, self.input_entry.get().split()))
            
            if not processes:
                raise ValueError("Please enter valid process burst times.")

            if self.algorithm.get() == "FCFS":
                self.fcfs(processes)
            elif self.algorithm.get() == "SJF":
                self.sjf(processes)
            elif self.algorithm.get() == "RR":
                self.rr(processes)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def fcfs(self, processes):
        n = len(processes)
        waiting_time = [0] * n
        turnaround_time = [0] * n
        start_time = [0] * n
        end_time = [0] * n

        for i in range(1, n):
            waiting_time[i] = processes[i-1] + waiting_time[i-1]
        for i in range(n):
            turnaround_time[i] = processes[i] + waiting_time[i]
            start_time[i] = waiting_time[i]
            end_time[i] = turnaround_time[i]

        self.display_output(processes, waiting_time, turnaround_time)
        self.plot_gantt_chart(start_time, end_time, n)

    def sjf(self, processes):
        processes_sorted = sorted(processes)
        self.fcfs(processes_sorted)

    def rr(self, processes, quantum=2):
        n = len(processes)
        queue = processes[:]
        waiting_time = [0] * n
        turnaround_time = [0] * n
        current_time = 0

        start_time = []
        end_time = []
        process_order = []

        while queue:
            process = queue.pop(0)
            if process > quantum:
                queue.append(process - quantum)
                start_time.append(current_time)
                current_time += quantum
                end_time.append(current_time)
                process_order.append(f"P{len(process_order) + 1}")
            else:
                start_time.append(current_time)
                current_time += process
                end_time.append(current_time)
                process_order.append(f"P{len(process_order) + 1}")

        self.display_output(processes, waiting_time, turnaround_time)
        self.plot_gantt_chart(start_time, end_time, len(processes), process_order)

    def display_output(self, processes, waiting_time, turnaround_time):
        output = "Process\tBurst Time\tWaiting Time\tTurnaround Time\n"
        for i in range(len(processes)):
            output += f"{i+1}\t{processes[i]}\t\t{waiting_time[i]}\t\t{turnaround_time[i]}\n"
        
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)

    def plot_gantt_chart(self, start, end, n, process_order=None):
        fig, ax = plt.subplots()
        for i in range(n):
            ax.barh("Processes", end[i] - start[i], left=start[i], color="blue", edgecolor="black")
            ax.text(start[i] + (end[i] - start[i]) / 2, 0, f"P{i+1}", ha='center', va='center', color='white', fontsize=12, fontweight='bold')

        ax.set_xlabel("Time")
        ax.set_title("Gantt Chart for CPU Scheduling")
        plt.show()

root = tk.Tk()
scheduler = CPUScheduler(root)
root.mainloop()
