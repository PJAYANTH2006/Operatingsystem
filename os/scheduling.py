import matplotlib.pyplot as plt

class Process:
    def __init__(self, pid, arrival_time, burst_time, priority=None):
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
    
