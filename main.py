import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import deque, OrderedDict
import heapq

class PageReplacementSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Algorithm Simulator")
        self.root.geometry("1000x700")
        
        # Variables
        self.page_frames = tk.IntVar(value=3)
        self.reference_string = tk.StringVar(value="7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1")
        self.selected_algorithm = tk.StringVar(value="FIFO")
        
        # Algorithms available
        self.algorithms = [
            "FIFO",
            "LRU",
            "Optimal",
            "LFU",
            "Clock",
            "MRU"
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Simulation Parameters", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Page frames input
        ttk.Label(input_frame, text="Number of Page Frames:").grid(row=0, column=0, sticky=tk.W)
        ttk.Spinbox(input_frame, from_=1, to=10, textvariable=self.page_frames, width=5).grid(row=0, column=1, sticky=tk.W)
        
        # Reference string input
        ttk.Label(input_frame, text="Reference String (comma separated):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(input_frame, textvariable=self.reference_string, width=40).grid(row=1, column=1, sticky=tk.W)
        
        # Algorithm selection
        ttk.Label(input_frame, text="Page Replacement Algorithm:").grid(row=2, column=0, sticky=tk.W)
        algo_combobox = ttk.Combobox(input_frame, textvariable=self.selected_algorithm, values=self.algorithms, state="readonly")
        algo_combobox.grid(row=2, column=1, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Run Simulation", command=self.run_simulation).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Show Graph", command=self.show_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        self.results_frame = ttk.LabelFrame(main_frame, text="Simulation Results", padding="10")
        self.results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview for results
        self.tree = ttk.Treeview(self.results_frame, columns=("Step", "Page", "Frames", "Fault", "Action"), show="headings")
        self.tree.heading("Step", text="Step")
        self.tree.heading("Page", text="Page")
        self.tree.heading("Frames", text="Frames")
        self.tree.heading("Fault", text="Fault")
        self.tree.heading("Action", text="Action")
        
        vsb = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.results_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        self.results_frame.grid_rowconfigure(0, weight=1)
        self.results_frame.grid_columnconfigure(0, weight=1)
        
        # Statistics frame
        self.stats_frame = ttk.LabelFrame(main_frame, text="Statistics", padding="10")
        self.stats_frame.pack(fill=tk.X, pady=5)
        
        # Initialize variables to store simulation data
        self.simulation_data = None
        self.page_faults = 0
    
    def run_simulation(self):
        # Clear previous results
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Get input values
        try:
            frames = self.page_frames.get()
            ref_string = [int(x.strip()) for x in self.reference_string.get().split(",")]
            algorithm = self.selected_algorithm.get()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers for reference string")
            return
        
        # Run selected algorithm
        if algorithm == "FIFO":
            results = self.fifo(ref_string, frames)
        elif algorithm == "LRU":
            results = self.lru(ref_string, frames)
        elif algorithm == "Optimal":
            results = self.optimal(ref_string, frames)
        elif algorithm == "LFU":
            results = self.lfu(ref_string, frames)
        elif algorithm == "Clock":
            results = self.clock(ref_string, frames)
        elif algorithm == "MRU":
            results = self.mru(ref_string, frames)
        
        # Store simulation data for graphing
        self.simulation_data = results
        self.page_faults = sum(1 for step in results if step["fault"])
        
        # Display results in treeview
        for step in results:
            fault = "Yes" if step["fault"] else "No"
            action = step.get("action", "")
            self.tree.insert("", tk.END, values=(
                step["step"],
                step["page"],
                " ".join(str(x) if x is not None else "-" for x in step["frames"]),
                fault,
                action
            ))
        
        # Update statistics
        self.update_stats(len(ref_string))
    
    def update_stats(self, total_references):
        # Clear previous stats
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        # Calculate stats
        fault_rate = (self.page_faults / total_references) * 100
        hit_rate = 100 - fault_rate
        
        # Display stats
        ttk.Label(self.stats_frame, text=f"Total References: {total_references}").grid(row=0, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, text=f"Page Faults: {self.page_faults}").grid(row=1, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, text=f"Page Fault Rate: {fault_rate:.2f}%").grid(row=2, column=0, sticky=tk.W)
        ttk.Label(self.stats_frame, text=f"Hit Rate: {hit_rate:.2f}%").grid(row=3, column=0, sticky=tk.W)
    
    def show_graph(self):
        if not self.simulation_data:
            messagebox.showwarning("No Data", "Please run a simulation first")
            return
        
        # Create a new window for the graph
        graph_window = tk.Toplevel(self.root)
        graph_window.title("Page Replacement Algorithm Visualization")
        graph_window.geometry("800x600")
        
        # Prepare data for plotting
        steps = [step["step"] for step in self.simulation_data]
        faults = [1 if step["fault"] else 0 for step in self.simulation_data]
        cumulative_faults = [sum(faults[:i+1]) for i in range(len(faults))]
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        
        # Plot fault occurrences
        ax1.step(steps, faults, where='post', label='Page Fault')
        ax1.set_title('Page Faults at Each Step')
        ax1.set_xlabel('Step')
        ax1.set_ylabel('Fault (1=Yes, 0=No)')
        ax1.grid(True)
        
        # Plot cumulative faults
        ax2.plot(steps, cumulative_faults, 'r-', label='Cumulative Page Faults')
        ax2.set_title('Cumulative Page Faults')
        ax2.set_xlabel('Step')
        ax2.set_ylabel('Total Page Faults')
        ax2.grid(True)
        
        fig.tight_layout()
        
        # Embed the figure in the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add a close button
        ttk.Button(graph_window, text="Close", command=graph_window.destroy).pack(pady=10)
    
    def reset(self):
        self.reference_string.set("7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1")
        self.page_frames.set(3)
        self.selected_algorithm.set("FIFO")
        
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        self.simulation_data = None
        self.page_faults = 0
    
    # Page Replacement Algorithms
    
    def fifo(self, ref_string, frames):
        memory = []
        queue = deque()
        results = []
        page_faults = 0
        
        for i, page in enumerate(ref_string):
            fault = False
            action = ""
            
            if page in memory:
                fault = False
            else:
                fault = True
                page_faults += 1
                
                if len(memory) < frames:
                    memory.append(page)
                    queue.append(page)
                else:
                    replaced = queue.popleft()
                    idx = memory.index(replaced)
                    memory[idx] = page
                    queue.append(page)
                    action = f"Replaced {replaced} with {page}"
            
            results.append({
                "step": i+1,
                "page": page,
                "frames": list(memory) + [None] * (frames - len(memory)),
                "fault": fault,
                "action": action
            })
        
        return results
    
    def lru(self, ref_string, frames):
        memory = OrderedDict()
        results = []
        
        for i, page in enumerate(ref_string):
            fault = False
            action = ""
            
            if page in memory:
                # Move to end to show recently used
                memory.move_to_end(page)
                fault = False
            else:
                fault = True
                
                if len(memory) < frames:
                    memory[page] = None
                else:
                    # Remove least recently used (first item)
                    replaced, _ = memory.popitem(last=False)
                    memory[page] = None
                    action = f"Replaced {replaced} with {page}"
            
            # Record current state
            current_frames = list(memory.keys()) + [None] * (frames - len(memory))
            results.append({
                "step": i+1,
                "page": page,
                "frames": current_frames,
                "fault": fault,
                "action": action
            })
        
        return results
    
    def optimal(self, ref_string, frames):
        memory = []
        results = []
        
        for i, page in enumerate(ref_string):
            fault = False
            action = ""
            
            if page in memory:
                fault = False
            else:
                fault = True
                
                if len(memory) < frames:
                    memory.append(page)
                else:
                    # Find page not used for longest time in future
                    farthest = -1
                    replaced = None
                    
                    for m in memory:
                        # Check if page appears in future
                        try:
                            idx = ref_string[i+1:].index(m)
                        except ValueError:
                            # Page not found in future - perfect candidate
                            replaced = m
                            break
                        
                        if idx > farthest:
                            farthest = idx
                            replaced = m
                    
                    # Replace the selected page
                    idx = memory.index(replaced)
                    memory[idx] = page
                    action = f"Replaced {replaced} with {page}"
            
            results.append({
                "step": i+1,
                "page": page,
                "frames": list(memory) + [None] * (frames - len(memory)),
                "fault": fault,
                "action": action
            })
        
        return results
    
    def lfu(self, ref_string, frames):
        memory = {}  # {page: [frequency, last_used_step]}
        results = []
        
        for i, page in enumerate(ref_string):
            fault = False
            action = ""
            
            if page in memory:
                # Update frequency
                memory[page][0] += 1
                memory[page][1] = i
                fault = False
            else:
                fault = True
                
                if len(memory) < frames:
                    memory[page] = [1, i]
                else:
                    # Find page with least frequency, then least recently used if tie
                    lfu_page = min(memory.items(), key=lambda x: (x[1][0], x[1][1]))[0]
                    del memory[lfu_page]
                    memory[page] = [1, i]
                    action = f"Replaced {lfu_page} with {page}"
            
            # Prepare current frames for display
            current_frames = list(memory.keys()) + [None] * (frames - len(memory))
            results.append({
                "step": i+1,
                "page": page,
                "frames": current_frames,
                "fault": fault,
                "action": action
            })
        
        return results
    
    def clock(self, ref_string, frames):
        memory = [None] * frames
        use_bits = [0] * frames
        pointer = 0
        results = []
        
        for i, page in enumerate(ref_string):
            fault = False
            action = ""
            
            if page in memory:
                # Set use bit to 1
                idx = memory.index(page)
                use_bits[idx] = 1
                fault = False
            else:
                fault = True
                
                while True:
                    if use_bits[pointer] == 0:
                        # Replace this page
                        replaced = memory[pointer]
                        memory[pointer] = page
                        use_bits[pointer] = 1
                        pointer = (pointer + 1) % frames
                        
                        if replaced is not None:
                            action = f"Replaced {replaced} with {page}"
                        break
                    else:
                        # Give second chance
                        use_bits[pointer] = 0
                        pointer = (pointer + 1) % frames
            
            results.append({
                "step": i+1,
                "page": page,
                "frames": list(memory),
                "fault": fault,
                "action": action
            })
        
        return results
    
    def mru(self, ref_string, frames):
        memory = []
        last_used = {}  # {page: last_used_step}
        results = []
        
        for i, page in enumerate(ref_string):
            fault = False
            action = ""
            
            if page in memory:
                last_used[page] = i
                fault = False
            else:
                fault = True
                
                if len(memory) < frames:
                    memory.append(page)
                    last_used[page] = i
                else:
                    # Find most recently used page (highest last_used value)
                    mru_page = max(last_used.items(), key=lambda x: x[1])[0]
                    idx = memory.index(mru_page)
                    replaced = memory[idx]
                    memory[idx] = page
                    del last_used[replaced]
                    last_used[page] = i
                    action = f"Replaced {replaced} with {page}"
            
            results.append({
                "step": i+1,
                "page": page,
                "frames": list(memory) + [None] * (frames - len(memory)),
                "fault": fault,
                "action": action
            })
        
        return results

if __name__ == "__main__":
    root = tk.Tk()
    app = PageReplacementSimulator(root)
    root.mainloop()
