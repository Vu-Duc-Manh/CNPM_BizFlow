import numpy as np

def is_safe_state(available, allocation, max_need): 
    n_processes, n_resources = allocation.shape
    available = np.array(available, dtype=int)
    allocation = np.array(allocation, dtype=int)
    max_need = np.array(max_need, dtype=int)
    
    need = max_need - allocation
    unfinished = list(range(n_processes))
    safe_sequence = []
    
    while unfinished:
        found = False
        for i in unfinished:
            if np.all(need[i] <= available):
                available += allocation[i]
                safe_sequence.append(i)
                unfinished.remove(i)
                found = True
                break
        if not found:
            return False, []
    
    return True, safe_sequence


def round_robin(processes, burst_times, quantum):
    n = len(processes)
    remaining_times = burst_times.copy()
    waiting_times = [0] * n
    completion_times = [0] * n
    time = 0

    while True:
        done = True
        for i in range(n):
            if remaining_times[i] > 0:
                done = False
                if remaining_times[i] > quantum:
                    time += quantum
                    remaining_times[i] -= quantum
                else:
                    time += remaining_times[i]
                    waiting_times[i] = time - burst_times[i]
                    remaining_times[i] = 0
                    completion_times[i] = time
        if done:
            break

    average_waiting_time = sum(waiting_times) / n

    return {
        "completion_times": completion_times,
        "waiting_times": waiting_times,
        "average_waiting_time": average_waiting_time
    }


# --- Kiểm tra Banker's Algorithm ---
# available = [2, 2, 1]
#allocation = np.array([
    [1, 0, 1],
    [0, 2, 2],
    [3, 0, 2]
#])
#max_need = np.array([
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2]
#])
available = [6, 3, 2]
allocation = np.array([
    [0, 1, 0],
    [2, 0, 0],
    [3, 1, 2]
])
max_need = np.array([
    [5, 3, 2],
    [3, 2, 2],
    [9, 0, 2]
])

is_safe, sequence = is_safe_state(available, allocation, max_need)
print("Trạng thái an toàn:", is_safe)
if is_safe:
    print("Thứ tự hoàn thành:", [f"P{i}" for i in sequence])
else:
    print("Không an toàn - Nguy cơ deadlock!")

# --- Kiểm tra Round Robin ---
processes = ["P1", "P2", "P3"]
burst_times = [10, 5, 8]
quantum = 3
result = round_robin(processes, burst_times, quantum)

print("\nThời gian hoàn thành:", result["completion_times"])
print("Thời gian chờ:", result["waiting_times"])
print("Thời gian chờ trung bình:", result["average_waiting_time"])
