import threading
import time
import queue
import multiprocessing
import numpy as np


def BubbleSort(data_ls, q):
    list_len = len(data_ls)
    for i in range(list_len):
        for j in range(list_len-1-i):
            if data_ls[j] > data_ls[j+1]:
                data_ls[j], data_ls[j+1] = data_ls[j+1], data_ls[j]

    if q is not None:
        q.put(data_ls)


def MergeSort(list1, list2, q):
    l1_i, l2_i = 0, 0
    l1_len, l2_len = len(list1), len(list2)
    sorted_ls = []
    
    while l1_i < l1_len and l2_i < l2_len:
        if list1[l1_i] < list2[l2_i]:
            sorted_ls.append(list1[l1_i])
            l1_i += 1
        else: 
            sorted_ls.append(list2[l2_i])
            l2_i += 1

    if l1_i < l1_len:
        sorted_ls.extend(list1[l1_i:l1_len])
    else: 
        sorted_ls.extend(list2[l2_i:l2_len])

    q.put(sorted_ls)


def mathod1(data_ls):
    start = time.perf_counter()
    BubbleSort(data_ls, None)
    process_time = time.perf_counter() - start
    return data_ls, process_time


def method2(data_ls, K):
    sep_arrls = np.array_split(data_ls, K)
    sep_ls = [list(arr) for arr in sep_arrls]

    q = queue.Queue(K)

    start = time.perf_counter()
    for l in sep_ls:
        BubbleSort(l, q)

    while q.qsize() != 1:
        list_to_merge1, list_to_merge2 = q.get(), q.get()
        MergeSort(list_to_merge1, list_to_merge2, q)

    process_time = time.perf_counter() - start
    return q.get(), process_time

    
def method3(data_ls, K):
    sep_arrls = np.array_split(data_ls, K)
    sep_ls = [list(arr) for arr in sep_arrls]

    q = multiprocessing.Manager().Queue(K)
    bbs_processes = []
    ms_processes = []

    start = time.perf_counter()
    for i in range(K):
        p = multiprocessing.Process(name=f'bbs_p{i}', target=BubbleSort, args=(sep_ls[i], q))
        p.start()
        bbs_processes.append(p)

    for p in bbs_processes:
        p.join()

    for i in range(K - 1):
        list_to_merge1, list_to_merge2 = q.get(), q.get()
        p = multiprocessing.Process(name=f'ms_p{i}', target=MergeSort, args=(list_to_merge1, list_to_merge2, q))
        p.start()
        ms_processes.append(p)

    for p in ms_processes:
        p.join()

    process_time = time.perf_counter() - start
    return q.get(), process_time


def method4(data_ls, K):
    sep_arrls = np.array_split(data_ls, K)
    sep_ls = [list(arr) for arr in sep_arrls]

    q = queue.Queue(K)
    bbs_threads = []
    ms_threads = []

    start = time.perf_counter()
    for i in range(K):
        t = threading.Thread(name=f'bbs_t{i}', target=BubbleSort, args=(sep_ls[i], q))
        t.start()
        bbs_threads.append(t)

    for t in bbs_threads:
        t.join()

    for i in range(K - 1):
        list_to_merge1, list_to_merge2 = q.get(), q.get()
        t = threading.Thread(name=f'ms_t{i}', target=MergeSort, args=(list_to_merge1, list_to_merge2, q))
        t.start()
        ms_threads.append(t)

    for t in ms_threads:
        t.join()
    
    process_time = time.perf_counter() - start
    return q.get(), process_time

    
def ReadData(inputFile):
    with open(inputFile, 'r') as f:
        data_ls = list(map(int, f.read().splitlines()))
        
    return data_ls


def WriteData(outputFile, data_sorted, cpuTime):
    with open(outputFile, 'w') as f:
        f.write('Sort :\n')
        for num in data_sorted:
            f.write(f'{num}\n')

        cpuTime = cpuTime * 1000
        print(f'\nCPU Time : {cpuTime:.16f}')
        f.write(f'CPU Time : {cpuTime:.16f}\n')

        now = time.localtime()
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        ms = int((time.time() % 1) * 1000)
        f.write(f"Output Time : {current_time}.{ms:06d}+08:00\n")


def main():
    fileName = input('Enter file name: ')
    inputFile = fileName + '.txt'
    data_ls = ReadData(inputFile)
    method = input('Enter method number: ')
    outputFile = ''

    match method:
        case '1':
            data_sorted, cpuTime = mathod1(data_ls)
        case '2':
            K = int(input('Enter number of segments (K): '))
            data_sorted, cpuTime = method2(data_ls, K)
        case '3':
            K = int(input('Enter number of segments (K): '))
            data_sorted, cpuTime = method3(data_ls, K)
        case '4':
            K = int(input('Enter number of segments (K): '))
            data_sorted, cpuTime = method4(data_ls, K)
        case _:
            print('Invalid method')

    outputFile = f'{fileName}_output{method}.txt'
    WriteData(outputFile, data_sorted, cpuTime)
    print(f'### The results are in {outputFile} ###\n')


if __name__ == '__main__':
    main()
    
