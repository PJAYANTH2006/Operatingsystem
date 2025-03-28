import matplotlib.pyplot as plt

class Process:
    def _init_(self, pid, arrival_time, burst_time, priority=None):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time
        self.completion_time = 0
        self.turnaround_time = 0
        self.waiting_time = 0
        self.priority = priority

def fcfs(processes):
    time = 0
    gantt_chart = []
    for process in sorted(processes, key=lambda x: x.arrival_time):
        if time < process.arrival_time:
            time = process.arrival_time
        gantt_chart.append((process.pid, time, time + process.burst_time))
        time += process.burst_time
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    return gantt_chart

def sjf(processes):
    time = 0
    gantt_chart = []
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= time]
        if not available_processes:
            time += 1
            continue
        process = min(available_processes, key=lambda x: x.burst_time)
        gantt_chart.append((process.pid, time, time + process.burst_time))
        time += process.burst_time
        processes.remove(process)
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    return gantt_chart

def round_robin(processes, quantum):
    time = 0
    gantt_chart = []
    queue = processes[:]
    while queue:
        process = queue.pop(0)
        if process.remaining_time > quantum:
            gantt_chart.append((process.pid, time, time + quantum))
            time += quantum
            process.remaining_time -= quantum
            queue.append(process)
        else:
            gantt_chart.append((process.pid, time, time + process.remaining_time))
            time += process.remaining_time
            process.remaining_time = 0
            process.completion_time = time
            process.turnaround_time = process.completion_time - process.arrival_time
            process.waiting_time = process.turnaround_time - process.burst_time
    return gantt_chart

def priority_scheduling(processes):
    time = 0
    gantt_chart = []
    while processes:
        available_processes = [p for p in processes if p.arrival_time <= time]
        if not available_processes:
            time += 1
            continue
        process = min(available_processes, key=lambda x: x.priority)
        gantt_chart.append((process.pid, time, time + process.burst_time))
        time += process.burst_time
        processes.remove(process)
        process.completion_time = time
        process.turnaround_time = process.completion_time - process.arrival_time
        process.waiting_time = process.turnaround_time - process.burst_time
    return gantt_chart

def plot_gantt_chart(gantt_charts, titles, avg_waiting_times, avg_turnaround_times):
    fig, gnt = plt.subplots(len(gantt_charts), 1, figsize=(12, 5 * len(gantt_charts)))
    for i, gantt_chart in enumerate(gantt_charts):
        gnt[i].set_ylim(0, 1)
        gnt[i].set_xlim(0, max(end for _, start, end in gantt_chart) + 5)  # added space for labels
        gnt[i].set_xlabel('Time')
        gnt[i].set_yticks([])
        gnt[i].set_title(titles[i])

        for j, (pid, start, end) in enumerate(gantt_chart):
            gnt[i].broken_barh([(start, end - start)], (0, 1), facecolors=('orange' if j % 2 == 0 else 'lightblue'))
            gnt[i].text((start + end) / 2, 0.5, str(pid), ha='center', va='center')

        # Adjust the position of average times to make it clearer
        gnt[i].text(max(end for _, start, end in gantt_chart) - 4, 0.1, 
                     f'Avg Waiting Time: {avg_waiting_times[i]:.2f}', 
                     ha='right', va='center', fontsize=10)
        
        gnt[i].text(max(end for _, start, end in gantt_chart) - 4, 0.3, 
                     f'Avg Turnaround Time: {avg_turnaround_times[i]:.2f}', 
                     ha='right', va='center', fontsize=10)

    plt.tight_layout()
    plt.show()
def calculate_average_times(processes):
    total_waiting_time = sum(p.waiting_time for p in processes)
    total_turnaround_time = sum(p.turnaround_time for p in processes)
    n = len(processes)
    average_waiting_time = total_waiting_time / n
    average_turnaround_time = total_turnaround_time / n
    return average_waiting_time, average_turnaround_time

def main():
    processes = [
        Process(pid=1, arrival_time=0, burst_time=5, priority=2),
        Process(pid=2, arrival_time=1, burst_time=3, priority=1),
        Process(pid=3, arrival_time=2, burst_time=8, priority=3),
        Process(pid=4, arrival_time=3, burst_time=6, priority=2)
    ]

    gantt_charts = []
    titles = []
    avg_waiting_times = []
    avg_turnaround_times = []

    gantt_charts.append(fcfs(processes.copy()))
    titles.append("FCFS Scheduling")
    avg_waiting_time, avg_turnaround_time = calculate_average_times(processes)
    avg_waiting_times.append(avg_waiting_time)
    avg_turnaround_times.append(avg_turnaround_time)

    gantt_charts.append(sjf(processes.copy()))
    titles.append("SJF Scheduling")
    avg_waiting_time, avg_turnaround_time = calculate_average_times(processes)
    avg_waiting_times.append(avg_waiting_time)
    avg_turnaround_times.append(avg_turnaround_time)

    gantt_charts.append(round_robin(processes.copy(), quantum=2))
    titles.append("Round Robin Scheduling")
    avg_waiting_time, avg_turnaround_time = calculate_average_times(processes)
    avg_waiting_times.append(avg_waiting_time)
    avg_turnaround_times.append(avg_turnaround_time)

    gantt_charts.append(priority_scheduling(processes.copy()))
    titles.append("Priority Scheduling")
    avg_waiting_time, avg_turnaround_time = calculate_average_times(processes)
     avg_waiting_times.append(avg_waiting_time)
    avg_turnaround_times.append(avg_turnaround_time)

    plot_gantt_chart(gantt_charts, titles, avg_waiting_times, avg_turnaround_times)

if _name_ == "_main_":
    main()
