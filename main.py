import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import heapq
import random
# import pandas as pd
import numpy as np
from collections import deque, defaultdict
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class CPUSchedulerSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Intelligent CPU Scheduler Simulator")
        self.root.geometry("1200x800")
        
        # Variables
        self.processes = []
        self.time_quantum = tk.IntVar(value=3)
        self.selected_algorithm = tk.StringVar(value="FCFS")
        self.auto_mode = tk.BooleanVar(value=False)
        
        # Algorithms
        self.algorithms = [
            "FCFS",
            "SJF (Non-Preemptive)",
            "SJF (Preemptive)",
            "Priority (Non-Preemptive)",
            "Priority (Preemptive)",
            "Round Robin",
            "Multilevel Feedback Queue"
        ]
        
        # ML Model for Quantum Optimization
        self.quantum_model = self.train_quantum_model()
        
        self.setup_ui()
    
    def train_quantum_model(self):
        # Generate synthetic training data
        X = np.random.randint(1, 20, (1000, 3))  # burst1, burst2, burst3
        y = np.random.randint(1, 10, 1000)        # optimal quantum
        
        model = RandomForestRegressor(n_estimators=10)
        model.fit(X, y)
        return model
    
    def setup_ui(self):
        # Main frames
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Process Input", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Process table
        self.tree = ttk.Treeview(input_frame, columns=("PID", "Arrival", "Burst", "Priority", "Type"), 
                                show="headings", height=5)
        self.tree.heading("PID", text="PID")
        self.tree.heading("Arrival", text="Arrival")
        self.tree.heading("Burst", text="Burst")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Type", text="Type")
        self.tree.pack(fill=tk.X)
        
        # Process input controls
        control_frame = ttk.Frame(input_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(control_frame, text="PID:").grid(row=0, column=0, padx=2)
        self.pid_entry = ttk.Entry(control_frame, width=5)
        self.pid_entry.grid(row=0, column=1, padx=2)
        
        ttk.Label(control_frame, text="Arrival:").grid(row=0, column=2, padx=2)
        self.arrival_entry = ttk.Entry(control_frame, width=5)
        self.arrival_entry.grid(row=0, column=3, padx=2)
        
        ttk.Label(control_frame, text="Burst:").grid(row=0, column=4, padx=2)
        self.burst_entry = ttk.Entry(control_frame, width=5)
        self.burst_entry.grid(row=0, column=5, padx=2)
        
        ttk.Label(control_frame, text="Priority:").grid(row=0, column=6, padx=2)
        self.priority_entry = ttk.Entry(control_frame, width=5)
        self.priority_entry.grid(row=0, column=7, padx=2)
        
        ttk.Label(control_frame, text="Type:").grid(row=0, column=8, padx=2)
        self.type_combobox = ttk.Combobox(control_frame, 
                                         values=["CPU-Bound", "I/O-Bound", "Interactive"], 
                                         width=10)
        self.type_combobox.grid(row=0, column=9, padx=2)
        self.type_combobox.current(0)
        
        ttk.Button(control_frame, text="Add Process", 
                  command=self.add_process).grid(row=0, column=10, padx=5)
        ttk.Button(control_frame, text="Generate Random", 
                  command=self.generate_random).grid(row=0, column=11, padx=5)
        ttk.Button(control_frame, text="Clear All", 
                  command=self.clear_processes).grid(row=0, column=12, padx=5)
        
        # Algorithm selection
        algo_frame = ttk.LabelFrame(main_frame, text="Scheduling Configuration", padding="10")
        algo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(algo_frame, text="Algorithm:").grid(row=0, column=0, sticky=tk.W)
        algo_combobox = ttk.Combobox(algo_frame, textvariable=self.selected_algorithm, 
                                    values=self.algorithms, state="readonly", width=20)
        algo_combobox.grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(algo_frame, text="Time Quantum (RR/MLFQ):").grid(row=0, column=2, padx=5)
        ttk.Entry(algo_frame, textvariable=self.time_quantum, width=5).grid(row=0, column=3)
        
        ttk.Checkbutton(algo_frame, text="Auto Mode (AI Selects Best Algorithm)", 
                       variable=self.auto_mode).grid(row=0, column=4, padx=10)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Run Simulation", 
                  command=self.run_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Gantt Chart", 
                  command=self.show_gantt).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Metrics", 
                  command=self.show_metrics).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", 
                  command=self.reset).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(main_frame, text="Simulation Results", padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Output text
        self.output_text = tk.Text(self.results_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Initialize simulation data
        self.simulation_data = None
        self.gantt_data = None
        self.metrics = None
    
    def add_process(self):
        try:
            pid = self.pid_entry.get()
            arrival = int(self.arrival_entry.get())
            burst = int(self.burst_entry.get())
            priority = int(self.priority_entry.get())
            process_type = self.type_combobox.get()
            
            self.tree.insert("", tk.END, values=(pid, arrival, burst, priority, process_type))
            
            # Clear entries
            self.pid_entry.delete(0, tk.END)
            self.arrival_entry.delete(0, tk.END)
            self.burst_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for arrival, burst and priority")
    
    def generate_random(self):
        for i in range(5):  # Generate 5 random processes
            pid = f"P{i+1}"
            arrival = random.randint(0, 5)
            burst = random.randint(1, 10)
            priority = random.randint(1, 5)
            process_type = random.choice(["CPU-Bound", "I/O-Bound", "Interactive"])
            
            self.tree.insert("", tk.END, values=(pid, arrival, burst, priority, process_type))
    
    def clear_processes(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    def run_simulation(self):
        # Get processes from tree
        processes = []
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            processes.append({
                'pid': values[0],
                'arrival': int(values[1]),
                'burst': int(values[2]),
                'priority': int(values[3]),
                'type': values[4]
            })
        
        if not processes:
            messagebox.showwarning("Warning", "No processes to schedule")
            return
        
        # Get algorithm
        algorithm = self.selected_algorithm.get()
        
        # Auto mode - select best algorithm
        if self.auto_mode.get():
            algorithm = self.select_best_algorithm(processes)
            self.output_text.insert(tk.END, f"Auto Mode Selected: {algorithm}\n")
        
        # Run selected algorithm
        if algorithm == "FCFS":
            results = self.fcfs(processes)
        elif algorithm == "SJF (Non-Preemptive)":
            results = self.sjf(processes, preemptive=False)
        elif algorithm == "SJF (Preemptive)":
            results = self.sjf(processes, preemptive=True)
        elif algorithm == "Priority (Non-Preemptive)":
            results = self.priority(processes, preemptive=False)
        elif algorithm == "Priority (Preemptive)":
            results = self.priority(processes, preemptive=True)
        elif algorithm == "Round Robin":
            results = self.round_robin(processes)
        elif algorithm == "Multilevel Feedback Queue":
            results = self.mlfq(processes)
        
        # Store results
        self.simulation_data = results
        self.calculate_metrics(results)
        
        # Display results
        self.display_results(results)
    
    def select_best_algorithm(self, processes):
        # Simple heuristic - in real implementation would use ML model
        avg_burst = sum(p['burst'] for p in processes) / len(processes)
        variance = np.var([p['burst'] for p in processes])
        
        if variance < 2 and avg_burst < 5:
            return "SJF (Non-Preemptive)"
        elif variance > 5 and len(processes) > 5:
            return "Round Robin"
        else:
            return "FCFS"
    
    def fcfs(self, processes):
        # Sort by arrival time
        processes = sorted(processes, key=lambda x: x['arrival'])
        
        current_time = 0
        results = []
        
        for p in processes:
            if current_time < p['arrival']:
                current_time = p['arrival']
            
            results.append({
                'pid': p['pid'],
                'start': current_time,
                'end': current_time + p['burst'],
                'arrival': p['arrival'],
                'burst': p['burst']
            })
            
            current_time += p['burst']
        
        return results
    
    def sjf(self, processes, preemptive=False):
        processes = sorted(processes, key=lambda x: x['arrival'])
        
        current_time = 0
        ready_queue = []
        results = []
        remaining_time = {p['pid']: p['burst'] for p in processes}
        n = len(processes)
        completed = 0
        
        while completed < n:
            # Add arriving processes to ready queue
            for p in processes:
                if p['arrival'] == current_time:
                    heapq.heappush(ready_queue, (p['burst'], p['pid'], p))
            
            if ready_queue:
                burst, pid, p = heapq.heappop(ready_queue)
                
                if preemptive:
                    execute_time = 1
                else:
                    execute_time = burst
                
                # Check if new process arrives with shorter burst during execution
                if preemptive:
                    for new_p in processes:
                        if new_p['arrival'] > current_time and new_p['arrival'] < current_time + execute_time:
                            if new_p['burst'] < remaining_time[pid]:
                                # Preempt current process
                                remaining_time[pid] -= (new_p['arrival'] - current_time)
                                heapq.heappush(ready_queue, (remaining_time[pid], pid, p))
                                execute_time = new_p['arrival'] - current_time
                                break
                
                results.append({
                    'pid': pid,
                    'start': current_time,
                    'end': current_time + execute_time,
                    'arrival': p['arrival'],
                    'burst': p['burst']
                })
                
                remaining_time[pid] -= execute_time
                current_time += execute_time
                
                if remaining_time[pid] > 0:
                    heapq.heappush(ready_queue, (remaining_time[pid], pid, p))
                else:
                    completed += 1
            else:
                current_time += 1
        
        return results
    
    def round_robin(self, processes):
        quantum = self.time_quantum.get()
        processes = sorted(processes, key=lambda x: x['arrival'])
        
        ready_queue = deque()
        current_time = 0
        results = []
        remaining_time = {p['pid']: p['burst'] for p in processes}
        n = len(processes)
        completed = 0
        
        # Initial population of ready queue
        i = 0
        while i < n and processes[i]['arrival'] <= current_time:
            ready_queue.append(processes[i])
            i += 1
        
        while completed < n:
            if ready_queue:
                p = ready_queue.popleft()
                execute_time = min(quantum, remaining_time[p['pid']])
                
                results.append({
                    'pid': p['pid'],
                    'start': current_time,
                    'end': current_time + execute_time,
                    'arrival': p['arrival'],
                    'burst': p['burst']
                })
                
                remaining_time[p['pid']] -= execute_time
                current_time += execute_time
                
                # Add newly arrived processes
                while i < n and processes[i]['arrival'] <= current_time:
                    ready_queue.append(processes[i])
                    i += 1
                
                if remaining_time[p['pid']] > 0:
                    ready_queue.append(p)
                else:
                    completed += 1
            else:
                current_time += 1
                # Check for new arrivals
                while i < n and processes[i]['arrival'] <= current_time:
                    ready_queue.append(processes[i])
                    i += 1
        
        return results
    
    def calculate_metrics(self, results):
        if not results:
            return
        
        # Calculate metrics
        process_data = {}
        for event in results:
            pid = event['pid']
            if pid not in process_data:
                process_data[pid] = {
                    'arrival': event['arrival'],
                    'burst': event['burst'],
                    'start_times': [],
                    'end_times': []
                }
            process_data[pid]['start_times'].append(event['start'])
            process_data[pid]['end_times'].append(event['end'])
        
        metrics = []
        total_waiting = 0
        total_turnaround = 0
        total_response = 0
        
        for pid, data in process_data.items():
            start = min(data['start_times'])
            end = max(data['end_times'])
            arrival = data['arrival']
            burst = data['burst']
            
            turnaround = end - arrival
            waiting = turnaround - burst
            response = start - arrival
            
            total_waiting += waiting
            total_turnaround += turnaround
            total_response += response
            
            metrics.append({
                'PID': pid,
                'Arrival': arrival,
                'Burst': burst,
                'Start': start,
                'Finish': end,
                'Waiting': waiting,
                'Turnaround': turnaround,
                'Response': response
            })
        
        n = len(process_data)
        avg_waiting = total_waiting / n
        avg_turnaround = total_turnaround / n
        avg_response = total_response / n
        
        # Calculate CPU utilization
        total_time = max(event['end'] for event in results)
        busy_time = sum(event['end'] - event['start'] for event in results)
        utilization = (busy_time / total_time) * 100
        
        self.metrics = {
            'per_process': metrics,
            'average': {
                'Waiting': avg_waiting,
                'Turnaround': avg_turnaround,
                'Response': avg_response,
                'Utilization': utilization
            }
        }
    
    def display_results(self, results):
        self.output_text.delete(1.0, tk.END)
        
        # Display Gantt chart
        self.output_text.insert(tk.END, "Gantt Chart:\n")
        self.output_text.insert(tk.END, "Time\tProcess\n")
        
        for event in results:
            self.output_text.insert(tk.END, f"{event['start']}-{event['end']}\t{event['pid']}\n")
        
        # Display metrics if calculated
        if self.metrics:
            self.output_text.insert(tk.END, "\nProcess Metrics:\n")
            self.output_text.insert(tk.END, "PID\tArrival\tBurst\tStart\tFinish\tWaiting\tTurnaround\tResponse\n")
            
            for metric in self.metrics['per_process']:
                self.output_text.insert(tk.END, 
                    f"{metric['PID']}\t{metric['Arrival']}\t{metric['Burst']}\t"
                    f"{metric['Start']}\t{metric['Finish']}\t{metric['Waiting']}\t"
                    f"{metric['Turnaround']}\t{metric['Response']}\n")
            
            self.output_text.insert(tk.END, "\nAverage Metrics:\n")
            self.output_text.insert(tk.END, 
                f"Waiting Time: {self.metrics['average']['Waiting']:.2f}\n")
            self.output_text.insert(tk.END, 
                f"Turnaround Time: {self.metrics['average']['Turnaround']:.2f}\n")
            self.output_text.insert(tk.END, 
                f"Response Time: {self.metrics['average']['Response']:.2f}\n")
            self.output_text.insert(tk.END, 
                f"CPU Utilization: {self.metrics['average']['Utilization']:.2f}%\n")
    
    def show_gantt(self):
        if not self.simulation_data:
            messagebox.showwarning("Warning", "No simulation data to display")
            return
        
        # Create a new window
        gantt_window = tk.Toplevel(self.root)
        gantt_window.title("Gantt Chart")
        gantt_window.geometry("800x400")
        
        # Create figure
        fig, ax = plt.subplots(figsize=(8, 4))
        
        # Process IDs for y-axis
        processes = sorted(list(set(event['pid'] for event in self.simulation_data)))
        y_ticks = range(len(processes))
        y_labels = processes
        
        # Create bars
        for event in self.simulation_data:
            start = event['start']
            duration = event['end'] - event['start']
            pid = event['pid']
            y_pos = processes.index(pid)
            
            ax.broken_barh([(start, duration)], (y_pos-0.4, 0.8), 
                          facecolors=('tab:blue'))
        
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_labels)
        ax.set_xlabel('Time')
        ax.set_ylabel('Processes')
        ax.set_title('CPU Scheduling Gantt Chart')
        ax.grid(True)
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=gantt_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Close button
        ttk.Button(gantt_window, text="Close", 
                  command=gantt_window.destroy).pack(pady=10)
    
    def show_metrics(self):
        if not self.metrics:
            messagebox.showwarning("Warning", "No metrics to display")
            return
        
        # Create a new window
        metrics_window = tk.Toplevel(self.root)
        metrics_window.title("Detailed Metrics")
        metrics_window.geometry("600x400")
        
        # Create treeview
        tree = ttk.Treeview(metrics_window, columns=("PID", "Waiting", "Turnaround", "Response"), 
                           show="headings")
        tree.heading("PID", text="PID")
        tree.heading("Waiting", text="Waiting Time")
        tree.heading("Turnaround", text="Turnaround Time")
        tree.heading("Response", text="Response Time")
        
        for metric in self.metrics['per_process']:
            tree.insert("", tk.END, values=(
                metric['PID'],
                metric['Waiting'],
                metric['Turnaround'],
                metric['Response']
            ))
        
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Add average metrics
        avg_frame = ttk.Frame(metrics_window)
        avg_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(avg_frame, text=f"Average Waiting Time: {self.metrics['average']['Waiting']:.2f}").pack()
        ttk.Label(avg_frame, text=f"Average Turnaround Time: {self.metrics['average']['Turnaround']:.2f}").pack()
        ttk.Label(avg_frame, text=f"Average Response Time: {self.metrics['average']['Response']:.2f}").pack()
        ttk.Label(avg_frame, text=f"CPU Utilization: {self.metrics['average']['Utilization']:.2f}%").pack()
        
        # Close button
        ttk.Button(metrics_window, text="Close", 
                  command=metrics_window.destroy).pack(pady=10)
    
    def reset(self):
        self.clear_processes()
        self.output_text.delete(1.0, tk.END)
        self.simulation_data = None
        self.metrics = None
        self.time_quantum.set(3)
        self.selected_algorithm.set("FCFS")
        self.auto_mode.set(False)

if __name__ == "__main__":
    root = tk.Tk()
    app = CPUSchedulerSimulator(root)
    root.mainloop()
