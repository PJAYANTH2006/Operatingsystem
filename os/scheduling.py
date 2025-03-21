import matplotlib.pyplot as plt
import numpy as np
import copy

class Process:
    def __init__(self, id, arrival_time, burst_time, priority):
        self.id = id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.start_time = 0
        self.finish_time = 0
        self.waiting_time = 0
        self.turnaround_time = 0

def calculate_metrics(processes):
    total_waiting_time = 0
    total_turnaround_time = 0
    for process in processes:
        process.waiting_time = process.start_time - process.arrival_time
        process.turnaround_time = process.finish_time - process.arrival_time
        total_waiting_time += process.waiting_time
        total_turnaround_time += process.turnaround_time
    avg_waiting_time = total_waiting_time / len(processes)
    avg_turnaround_time = total_turnaround_time / len(processes)
    return avg_waiting_time, avg_turnaround_time

def fcfs_scheduling(processes):
    processes.sort(key=lambda x: x.arrival_time)
    current_time = 0
    for process in processes:
        process.start_time = max(current_time, process.arrival_time)
        process.finish_time = process.start_time + process.burst_time
        current_time = process.finish_time
    return processes

def sjf_scheduling(processes):
    processes.sort(key=lambda x: (x.arrival_time, x.burst_time))
    current_time = 0
    ready_queue = []
    completed_processes = []
    while len(completed_processes) < len(processes):
        for process in processes:
            if process.arrival_time <= current_time and process not in ready_queue and process not in completed_processes:
                ready_queue.append(process)
        if ready_queue:
            ready_queue.sort(key=lambda x: x.burst_time)
            process = ready_queue.pop(0)
            process.start_time = current_time
            process.finish_time = process.start_time + process.burst_time
            current_time = process.finish_time
            completed_processes.append(process)
        else:
            current_time += 1
    return completed_processes
