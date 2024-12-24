import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
#definition of the process clas to be used with its atributes along in the code
class Process:
    def __init__(self, process_id, arrival_time, burst_time, come_back_time, priority):
        self.id = process_id
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.come_back_time = come_back_time
        self.priority = priority
        self.arrival_time_changeable = arrival_time
        self.remaining_time = burst_time
        self.in_queue = False
        self.start_end_pair = []
        self.actual_priority = priority
        self.time_in_queue = 0

    def add_start_end_pair(self, start, end):
        self.start_end_pair.append((start, end))
#retrieve the original data so each algo can do its job unaffected
    def original_data(self):
        self.remaining_time = self.burst_time
        self.arrival_time_changeable = self.arrival_time
        self.in_queue = False
        self.start_end_pair = []
        self.actual_priority = self.priority

#defining the processes
p1 = Process(1, 0, 10, 2, 3)
p2 = Process(2, 1, 8, 4, 2)
p3 = Process(3, 3, 14, 6, 3)
p4 = Process(4, 4, 7, 8, 1)
p5 = Process(5, 6, 5, 3, 0)
p6 = Process(6, 7, 4, 6, 1)
p7 = Process(7, 8, 6, 9, 2)

process_list= [p1, p2, p3, p4, p5, p6, p7]

# FCFS implementation

t = 0
ready_queue = []
waiting_queue = []
turnaround_times = []
waiting_times = []
gantt = []

while t < 200:
    for process in process_list:
        if process.arrival_time <= t and not process.in_queue:
            ready_queue.append(process)
            process.in_queue = True
#arranging the ready queue according to at
    ready_queue.sort(key=lambda x: x.arrival_time_changeable)

    if ready_queue: #checking if the ready queue is not empty to execute processes
        current_process = ready_queue.pop(0)
        start_time = max(t, current_process.arrival_time_changeable)
        end_time = min(start_time + current_process.burst_time, 200)
        current_process.add_start_end_pair(start_time, end_time - start_time)
        gantt.append((current_process.id, start_time, end_time))
        t = end_time
        waiting_times.append(start_time - current_process.arrival_time_changeable)
        current_process.arrival_time_changeable = t + current_process.come_back_time
        waiting_queue.append(current_process) #affter finishing the process it will be appended to the waiting

    for process in waiting_queue: #checking if it's time has come to go to the ready
        if t>= process.come_back_time:
            ready_queue.append(process) # adding it it the condition is satisfied
            waiting_queue.remove(process)

print("FCFS Gantt Chart:")
for finished in gantt:
    print(f"p{finished[0]}: {finished[1]} - {finished[2]}")
for process in process_list:
    completion_time = process.start_end_pair[-1][0] + process.start_end_pair[-1][1]
    turnaround_time = completion_time - process.arrival_time
    turnaround_times.append(turnaround_time)

           
awt = sum(turnaround_times) / len(process_list)
att = sum(waiting_times) /len(process_list)

print(f"\nAverage Turnaround Time(FCFS): {awt}")
print(f"average waiting time: {att}")

# plot FCFS

fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('Processes')

ax.broken_barh(p1.start_end_pair, (10,9), facecolor='tab:blue')
ax.broken_barh(p2.start_end_pair, (20,9), facecolor='red')
ax.broken_barh(p3.start_end_pair, (30,9), facecolor='blue')
ax.broken_barh(p4.start_end_pair, (40,9), facecolor='green')
ax.broken_barh(p5.start_end_pair, (50,9), facecolor='pink')
ax.broken_barh(p6.start_end_pair, (60,9), facecolor='orange')
ax.broken_barh(p7.start_end_pair, (70,9), facecolor='black')


x_values = []
for process in process_list:
    for tup in process.start_end_pair:
        x_values.append(tup[0])
x_values.append(200)
x_values.sort()
x_ticks = x_values
x_labels = x_values
plt.xticks(ticks=x_ticks, labels=x_labels)
plt.figure(figsize=(20, 20))
xs = np.linspace(1, 21, 200)
ax.vlines(x=x_values, ymin=0, ymax=len(xs) * 10, ls='--', lw=1, label='vline_multiple - full height')
ax.set_ylim(0, (len(process_list) + 2) * 10)
ax.set_xlim(0, 200)
plt.show()

for process in process_list:
    process.original_data()
print("end of fcfs :)))))")
    ######################################################################
      #sjf code
t = 0
ready_queue = []
waiting_queue = []
gantt = []

while t< 200:
    for process in process_list:
        if process.arrival_time <= t and not process.in_queue:
            ready_queue.append(process)
            process.in_queue = True
#sort according to bt
    ready_queue.sort(key=lambda x: x.burst_time)

#execute then adding p to the waiting_q
    if ready_queue:
        current_process = ready_queue.pop(0)
        start_time = max(t, current_process.arrival_time_changeable)
        end_time = min(start_time + current_process.burst_time, 200)
        current_process.add_start_end_pair(start_time, end_time - start_time)
        gantt.append((current_process.id, start_time, end_time))
        t= end_time
        current_process.arrival_time_changeable = t+ current_process.come_back_time
        waiting_queue.append(current_process)

    for process in waiting_queue:
        if t >= process.arrival_time_changeable:
            ready_queue.append(process)
            waiting_queue.remove(process)
total_waiting_time = 0
total_turnaround_time = 0
visited_processes = set()

for task in gantt:
    process_id, start_time, end_time = task
    process = process_list[process_id - 1]

    total_waiting_time += start_time - process.arrival_time
    total_turnaround_time += end_time - process.arrival_time
    visited_processes.add(process.id)

# Check whether any  process was not visited
for process in process_list:
    if process.id not in visited_processes:
        total_waiting_time = float('inf')
        total_turnaround_time = float('inf')
        break

# Calculate averages
average_waiting_time = total_waiting_time / len(process_list)
average_turnaround_time = total_turnaround_time / len(process_list)


print("\n gantt chart for shortest job first:")
for task in gantt:
    print(f"p{task[0]}: {task[1]} - {task[2]}")
print(f"Average Waiting Time: {average_waiting_time}")
print(f"Average Turnaround Time: {average_turnaround_time}")
print("end of shortest job first :))))))))))")
fig, sjf_sketch = plt.subplots()
sjf_sketch.set_xlabel('Time')
sjf_sketch.set_ylabel('Processes')
sjf_sketch.broken_barh(p1.start_end_pair, (10,9), facecolor='tab:blue')
sjf_sketch.broken_barh(p2.start_end_pair, (20,9), facecolor='red')
sjf_sketch.broken_barh(p3.start_end_pair, (30,9), facecolor='blue')
sjf_sketch.broken_barh(p4.start_end_pair, (40,9), facecolor='green')
sjf_sketch.broken_barh(p5.start_end_pair, (50,9), facecolor='pink')
sjf_sketch.broken_barh(p6.start_end_pair, (60,9), facecolor='orange')
sjf_sketch.broken_barh(p7.start_end_pair, (70,9), facecolor='black')


x_values_sjf = []
for process in process_list:
    for tup in process.start_end_pair:
        x_values_sjf.append(tup[0])
x_values_sjf.append(200)
x_values_sjf.sort()
x_ticks_sjf = x_values_sjf
x_labels_sjf = x_values_sjf
plt.xticks(ticks=x_ticks_sjf, labels=x_labels_sjf)
plt.figure(figsize=(20, 20))
sjf_sketch.vlines(x=x_values_sjf, ymin=0, ymax=len(xs) * 10, ls='--', lw=1, label='vline_multiple - full height')
sjf_sketch.set_ylim(0, (len(process_list) + 2) * 10)
sjf_sketch.set_xlim(0, 200)
plt.show()

for process in process_list:
    process.original_data()
#######################################################################3
 #round robin
t = 0
ready_queue = []
waiting_queue = []
gantt= []
time_quantum = 5
waiting_times = []
turnaround_times = []
while t < 200:
    # print(current_time)
    for process in process_list:
        if process.arrival_time <= t and not process.in_queue:
            ready_queue.append(process)
            process.in_queue = True

    ready_queue.sort(key=lambda x: x.arrival_time_changeable)

    if ready_queue:
        current_process = ready_queue[0]
        ready_queue.remove(current_process)
        start_time = max(t, current_process.arrival_time_changeable)
        end_time = min(start_time + time_quantum, start_time + current_process.remaining_time, 200)
        current_process.remaining_time -= (end_time - start_time)
        current_process.add_start_end_pair(start_time, end_time - start_time)
        gantt.append((current_process.id, start_time, end_time))
        t = end_time
        waiting_times.append(start_time - current_process.arrival_time_changeable)

        if current_process.remaining_time == 0:
            current_process.arrival_time_changeable = t + current_process.come_back_time
            current_process.remaining_time = current_process.burst_time
            waiting_queue.append(current_process)
        else:
            ready_queue.append(current_process)
            current_process.arrival_time_changeable = t
    for process in waiting_queue:
        if t >= process.arrival_time_changeable:
            ready_queue.append(process)
            waiting_queue.remove(process)
waiting_time = 0
turnaround_time = 0
# Calculate tt, wt
for process in process_list:
    completion_time = process.start_end_pair[-1][0] + process.start_end_pair[-1][1]
    turnaround_time = completion_time - process.arrival_time
    #waiting_time = turnaround_time - process.burst_time
    turnaround_times.append(turnaround_time)
    #waiting_times.append(waiting_time)
current_process.arrival_time_changeable = t + current_process.come_back_time


print("\n the Gantt Chart of round robin:")
for task in gantt:
    print(f"p{task[0]}: {task[1]} - {task[2]}")
awt = sum(turnaround_times) / len(process_list)
att = sum(waiting_times) /len(process_list)

print(f"\nAverage Turnaround Time(round robin): {awt}")
print(f"average waiting time: {att}")
# Plot RR
fig, rr_sketch = plt.subplots()
rr_sketch.set_xlabel('Time')
rr_sketch.set_ylabel('Processes')
rr_sketch.broken_barh(p1.start_end_pair, (10,9), facecolor='tab:blue')
rr_sketch.broken_barh(p2.start_end_pair, (20,9), facecolor='red')
rr_sketch.broken_barh(p3.start_end_pair, (30,9), facecolor='blue')
rr_sketch.broken_barh(p4.start_end_pair, (40,9), facecolor='green')
rr_sketch.broken_barh(p5.start_end_pair, (50,9), facecolor='pink')
rr_sketch.broken_barh(p6.start_end_pair, (60,9), facecolor='orange')
rr_sketch.broken_barh(p7.start_end_pair, (70,9), facecolor='black')


x_values_sjf = []
for process in process_list:
    for tup in process.start_end_pair:
        x_values_sjf.append(tup[0])
x_values_sjf.append(200)
x_values_sjf.sort()
x_ticks_sjf = x_values_sjf
x_labels_sjf = x_values_sjf
plt.xticks(ticks=x_ticks_sjf, labels=x_labels_sjf)
plt.figure(figsize=(100, 100))
rr_sketch.vlines(x=x_values_sjf, ymin=0, ymax=len(xs) * 10, ls='--', lw=1, label='vline_multiple - full height')
rr_sketch.set_ylim(0, (len(process_list) + 2) * 10)
rr_sketch.set_xlim(0, 200)
plt.show()

for process in process_list:
    process.original_data()
print("end of rr :)))))))))))")
    ############################################################################
#srjf
t = 0
ready_queue = []
waiting_queue = []
gantt = []
start_time = 0
proc_ps = None

while t <= 200:
    for process in process_list:
        if process.arrival_time <= t and not process.in_queue:
            ready_queue.append(process)
            process.in_queue = True

    ready_queue.sort(key=lambda x: x.remaining_time)

    if ready_queue:
        current_process = ready_queue[0]
        if proc_ps and proc_ps != current_process or t == 200:
            end_time = t
            gantt.append((proc_ps.id, start_time, end_time))
            start_time = max(t, current_process.arrival_time_changeable)
            proc_ps.add_start_end_pair(start_time, end_time - start_time)

        current_process.remaining_time -= 1
        t += 1
        proc_ps = current_process

        if current_process.remaining_time == 0:
            current_process.arrival_time_changeable= t + current_process.come_back_time
            current_process.remaining_time = current_process.burst_time
            waiting_queue.append(current_process)
            ready_queue.remove(current_process)

    for process in waiting_queue:
        if t >= process.arrival_time_changeable:
            ready_queue.append(process)
            waiting_queue.remove(process)
total_waiting_time = 0
total_turnaround_time = 0
visited_processes = set()

for task in gantt:
    process_id, start_time, end_time = task
    process = process_list[process_id - 1]

    total_waiting_time += start_time - process.arrival_time
    total_turnaround_time += end_time - process.arrival_time
    visited_processes.add(process.id)

# Check whether any  process was not visited
for process in process_list:
    if process.id not in visited_processes:
        total_waiting_time = float('inf')
        total_turnaround_time = float('inf')
        break

# Calculate averages
average_waiting_time = total_waiting_time / len(process_list)
average_turnaround_time = total_turnaround_time / len(process_list)

print("\n gantt chart of shortest remainign job first:")
for task in gantt:
    print(f"p{task[0]}: {task[1]} - {task[2]}")
print(f"Average Waiting Time: {average_waiting_time}")
print(f"Average Turnaround Time: {average_turnaround_time}")

# Plot SRTF
fig, srjb_sketch= plt.subplots()
srjb_sketch.set_xlabel('Time')
srjb_sketch.set_ylabel('Processes')
srjb_sketch.broken_barh(p1.start_end_pair, (10,9), facecolor='tab:blue')
srjb_sketch.broken_barh(p2.start_end_pair, (20,9), facecolor='red')
srjb_sketch.broken_barh(p3.start_end_pair, (30,9), facecolor='blue')
srjb_sketch.broken_barh(p4.start_end_pair, (40,9), facecolor='green')
srjb_sketch.broken_barh(p5.start_end_pair, (50,9), facecolor='pink')
srjb_sketch.broken_barh(p6.start_end_pair, (60,9), facecolor='orange')
srjb_sketch.broken_barh(p7.start_end_pair, (70,9), facecolor='black')


x_values_sjf = []
for process in process_list:
    for tup in process.start_end_pair:
        x_values_sjf.append(tup[0])
x_values_sjf.append(200)
x_values_sjf.sort()
x_ticks_sjf = x_values_sjf
x_labels_sjf = x_values_sjf
plt.xticks(ticks=x_ticks_sjf, labels=x_labels_sjf)
plt.figure(figsize=(20, 20))
xs = np.linspace(1, 21, 200)
srjb_sketch.vlines(x=x_values_sjf, ymin=0, ymax=len(xs) * 10, ls='--', lw=1, label='vline_multiple - full height')
srjb_sketch.set_ylim(0, (len(process_list) + 2) * 10)
srjb_sketch.set_xlim(0, 200)
plt.show()


for process in process_list:
    process.original_data()
print("end of shortest remaing job :))))")
##########################################################################################
#priority non preemptive
t = 0
last_computed = 0
ready_queue = []
waiting_queue = []
gantt_chart = []
waiting_times = []
turnaround_times = []

while t < 200:
    for process in process_list: #adding processes to the ready_Q
        if process.arrival_time <= t and not process.in_queue:
            ready_queue.append(process)
            process.in_queue = True
    for process in ready_queue: #decrement p if it's been there for 5 units
        process.actual_priority = max(0, process.priority-(t-process.arrival_time_changeable)//5)
#arrange based on priority
    ready_queue.sort(key=lambda x: (x.actual_priority, x.arrival_time_changeable))
    if ready_queue:
        current_process = ready_queue.pop(0)
        start_time = max(t, current_process.arrival_time_changeable)
        end_time = min(200, start_time + current_process.burst_time)
        current_process.add_start_end_pair(start_time, end_time - start_time)
        gantt_chart.append((current_process.id, start_time, end_time))
        waiting_times.append(start_time - current_process.arrival_time_changeable)
        last_computed = t
        t = end_time
        current_process.arrival_time_changeable = t + current_process.come_back_time
        waiting_queue.append(current_process)
    for process in waiting_queue:
        if t >= process.arrival_time_changeable:
            ready_queue.append(process)
            waiting_queue.remove(process)
for process in process_list:
    completion_time = process.start_end_pair[-1][0] + process.start_end_pair[-1][1]
    turnaround_time = completion_time - process.arrival_time
    #waiting_time = turnaround_time - process.burst_time
    turnaround_times.append(turnaround_time)
    #waiting_times.append(waiting_time)
awt = sum(turnaround_times) / len(process_list)
att = sum(waiting_times) /len(process_list)

print("\nNon-Preemptive Priority Gantt Chart:")
for task in gantt_chart:
    print(f"p{task[0]}: {task[1]} - {task[2]}")
print(f"Average Waiting Time: {att}")
print(f"Average Turnaround Time: {awt}")

fig, pp_sketch = plt.subplots()
pp_sketch.set_xlabel('Time')
pp_sketch.set_ylabel('Processes')
pp_sketch.broken_barh(p1.start_end_pair, (10,9), facecolor='tab:blue')
pp_sketch.broken_barh(p2.start_end_pair, (20,9), facecolor='red')
pp_sketch.broken_barh(p3.start_end_pair, (30,9), facecolor='blue')
pp_sketch.broken_barh(p4.start_end_pair, (40,9), facecolor='green')
pp_sketch.broken_barh(p5.start_end_pair, (50,9), facecolor='pink')
pp_sketch.broken_barh(p6.start_end_pair, (60,9), facecolor='orange')
pp_sketch.broken_barh(p7.start_end_pair, (70,9), facecolor='black')


x_values_sjf = []
for process in process_list:
    for tup in process.start_end_pair:
        x_values_sjf.append(tup[0])
x_values_sjf.append(200)
x_values_sjf.sort()
x_ticks_sjf = x_values_sjf
x_labels_sjf = x_values_sjf
plt.xticks(ticks=x_ticks_sjf, labels=x_labels_sjf)
plt.figure(figsize=(20, 20))
xs = np.linspace(1, 21, 200)
pp_sketch.vlines(x=x_values_sjf, ymin=0, ymax=len(xs) * 10, ls='--', lw=1, label='vline_multiple - full height')
pp_sketch.set_ylim(0, (len(process_list) + 2) * 10)
pp_sketch.set_xlim(0, 200)
plt.show()


for process in process_list:
    process.original_data()
print("end of priority :)))))))))))")
#############################################################################################3
#preemprive priority:
t = 0
ready_queue = []
waiting_queue = []
gantt = []
start_time = 0
waiting_times = []
turnaround_times = []
previous_process = None
current_process = None


while t <= 200:
    for process in process_list: #adding processes to the ready queue based on at
        if process.arrival_time <= t and not process.in_queue:
            ready_queue.append(process)
            process.in_queue = True

    for process in ready_queue: #handles the aging 
        if process != current_process:
            process.time_in_queue += 1
            if process.time_in_queue == 5 and process.actual_priority > 0:
                process.actual_priority = process.actual_priority - 1
                process.time_in_queue = 0
#sorts the ready queue based on the priority factor
    ready_queue.sort(key=lambda x: x.actual_priority)
    if current_process and current_process.actual_priority != 0:
        ready_queue.sort(key=lambda x: (x.actual_priority, x.arrival_time_changeable))
    if ready_queue: #handles the current process by the cpu
        current_process = ready_queue[0]
        if previous_process and previous_process != current_process or t == 200:
            end_time = t
            previous_process.add_start_end_pair(start_time, end_time - start_time)
            previous_process.arrival_time_changeable = t
            previous_process.actual_priority = previous_process.priority
            previous_process.time_in_queue = 0
            gantt.append((previous_process.id, start_time, end_time))
            start_time = max(t, current_process.arrival_time_changeable)
        current_process.remaining_time -= 1
        t += 1 #increment time to reach 200
        previous_process = current_process
#move the current process from the ready queue to the waiting
        if current_process.remaining_time == 0:
            current_process.remaining_time = current_process.burst_time
            current_process.actual_priority = current_process.priority
            current_process.arrival_time_changeable= t + current_process.come_back_time
            current_process.time_in_queue = 0
            waiting_queue.append(current_process)
            ready_queue.remove(current_process)

    for process in waiting_queue:
        if t >= process.arrival_time_changeable:
            ready_queue.append(process)
            waiting_queue.remove(process)
for process in process_list:
    completion_time = process.start_end_pair[-1][0] + process.start_end_pair[-1][1]
    turnaround_time = completion_time - process.arrival_time
    waiting_time = turnaround_time - process.burst_time
    turnaround_times.append(turnaround_time)
    waiting_times.append(waiting_time)
awt = sum(turnaround_times) / len(process_list)
att = sum(waiting_times) /len(process_list)

print("\n gant chat for preemptive priority:")
for task in gantt:
    print(f"p{task[0]}: {task[1]} - {task[2]}")
print(f"Average Waiting Time: {att}")
print(f"Average Turnaround Time: {awt}")

#plot 
fig, ax = plt.subplots()
ax.set_xlabel('Time')
ax.set_ylabel('Processes')

ax.broken_barh(p1.start_end_pair, (10,9), facecolor='tab:blue')
ax.broken_barh(p2.start_end_pair, (20,9), facecolor='red')
ax.broken_barh(p3.start_end_pair, (30,9), facecolor='blue')
ax.broken_barh(p4.start_end_pair, (40,9), facecolor='green')
ax.broken_barh(p5.start_end_pair, (50,9), facecolor='pink')
ax.broken_barh(p6.start_end_pair, (60,9), facecolor='orange')
ax.broken_barh(p7.start_end_pair, (70,9), facecolor='black')


x_values_sjf = []
for process in process_list:
    for tup in process.start_end_pair:
        x_values_sjf.append(tup[0])
x_values_sjf.append(200)
x_values_sjf.sort()
x_ticks_sjf = x_values_sjf
x_labels_sjf = x_values_sjf
plt.xticks(ticks=x_ticks_sjf, labels=x_labels_sjf)
plt.figure(figsize=(100, 100))
ax.vlines(x=x_values_sjf, ymin=0, ymax=len(xs) * 10, ls='--', lw=1, label='vline_multiple - full height')
ax.set_ylim(0, (len(process_list) + 2) * 10)
ax.set_xlim(0, 200)
plt.show()
for process in process_list:
    process.original_data()
print("end of priority preempritve :)))))))))))")
print("end of project :))))))))))))))))")