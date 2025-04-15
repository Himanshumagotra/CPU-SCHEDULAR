Intelligent CPU Scheduler Simulator
This project is a Python-based simulator that demonstrates and compares different CPU scheduling algorithms, including FCFS, SJF, Round Robin, Priority Scheduling, and an AI-powered adaptive scheduler. It provides a hands-on way to analyze algorithm efficiency through Gantt charts and performance metrics.

🚀 Key Features
✅ Supports 6 Scheduling Algorithms

First-Come-First-Serve (FCFS)

Shortest Job First (SJF) – Preemptive & Non-Preemptive

Priority Scheduling – Preemptive & Non-Preemptive

Round Robin (RR) with adjustable time quantum

Multilevel Feedback Queue (MLFQ) – Advanced scheduling

AI Auto-Mode – Dynamically selects the best algorithm

✅ Interactive GUI

Input process details manually or generate random processes

Adjust time quantum for Round Robin

Visualize scheduling with Gantt charts

✅ Performance Metrics

Waiting Time, Turnaround Time, Response Time

CPU Utilization

Comparative Analysis between algorithms

✅ AI-Powered Enhancements

Quantum Optimizer (ML-based) for Round Robin

Priority Predictor for adaptive scheduling

⚙️ Installation & Setup
Prerequisites
Python 3.6+

Required libraries: tkinter, matplotlib, scikit-learn, numpy

Steps to Run
Clone the repository:

bash
Copy
git clone https://github.com/your-repo/Intelligent-CPU-Scheduler.git
cd Intelligent-CPU-Scheduler
Install dependencies:

bash
Copy
pip install numpy scikit-learn matplotlib
Run the simulator:


python main.py
🎮 How to Use
Add Processes

Enter PID, Arrival Time, Burst Time, Priority, Type

Or click "Generate Random" for quick testing

Select Algorithm

Choose from FCFS, SJF, Round Robin, etc.

Enable Auto Mode for AI-based selection

Run Simulation

View Gantt Chart (timeline of process execution)

Check Performance Metrics (waiting time, CPU utilization)

Compare Results

Switch algorithms to see efficiency differences

📊 Performance Metrics Explained
Metric	Description	Ideal Goal
Waiting Time	Time a process waits in the ready queue	Minimize
Turnaround Time	Total time from arrival to completion	Minimize
Response Time	Time until first CPU response	Minimize
CPU Utilization	Percentage of CPU busy time	Maximize
🛠️ Technologies Used
Category	Tools/Libraries
Core Language	Python 3
GUI Framework	Tkinter
Visualization	Matplotlib
Machine Learning	scikit-learn (Quantum Optimizer)
Data Handling	NumPy, Pandas
📜 Project Structure
Copy
📂 Intelligent-CPU-Scheduler  
├── main.py            # Main GUI & simulation logic  
├── algorithms.py      # Scheduling algorithm implementations  
├── ml_optimizer.py    # AI-based quantum optimization  
├── README.md          # Project documentation  
└── requirements.txt   # Dependencies  
🤝 Contributing & Feedback
Found a bug? Open an issue.

Want to improve something? Submit a pull request.

Suggestions? Let’s discuss!

Built   by [Himanshu magotra ]

📌 Quick Start Command

git clone https://github.com/your-repo/Intelligent-CPU-Scheduler.git && cd Intelligent-CPU-Scheduler && pip install -r requirements.txt && python main.py
