from queue import Queue
from collections import defaultdict

def read_input_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    method = lines[0].split()[0]
    page_frames = int(lines[0].split()[1])
    page_references = [int(digit) for digit in lines[1].split()[0]]
    return method, page_frames, page_references

def write_output_file(outputFile, writeMode, methodName, pageFrameNum, 
                      pageReferList, page_replaces, page_frame_ls, page_fault_ls, paragraph_space):
    with open(outputFile, writeMode) as f:
        f.write('--------------' + methodName + '-----------------------\n')
        n = len(pageReferList)
        for i in range(n):
            f.write(str(pageReferList[i]) + '\t' + page_frame_ls[i])
            if i in page_fault_ls:
                f.write('\tF\n')
            else:
                f.write('\n')
        
        f.write('Page Fault = ' + str(len(page_fault_ls)) + 
                '  Page Replaces = ' + str(page_replaces) +
                '  Page Frames = ' + str(pageFrameNum) + '\n')
        
        if paragraph_space == True:
            f.write('\n')

from queue import Queue

def FIFO(pageFrameNum, pageReferList):
    queue = Queue()

    n = len(pageReferList)
    page_replaces = 0
    page_frame_ls = []
    page_fault_ls = []
    for i in range(n):
        if queue.qsize() < pageFrameNum:
            if pageReferList[i] not in queue.queue:
                queue.put(pageReferList[i])
                page_fault_ls.append(i)
        else:
            if pageReferList[i] not in queue.queue:
                queue.get()
                queue.put(pageReferList[i])
                page_fault_ls.append(i)
                page_replaces += 1
        
        string = ''.join(map(str, reversed(queue.queue)))
        page_frame_ls.append(string)

    return page_replaces, page_frame_ls, page_fault_ls

def LRU(pageFrameNum, pageReferList): 
    page_frame = []
    indexes = {} 
  
    n = len(pageReferList)
    page_replaces = 0
    page_frame_ls = []
    page_fault_ls = []
    for i in range(n): 
        if len(page_frame) < pageFrameNum: 
            if pageReferList[i] not in page_frame: 
                page_fault_ls.append(i)
                page_frame.append(pageReferList[i])

            indexes[pageReferList[i]] = i
        else: 
            if pageReferList[i] not in page_frame: 
                lru = float('inf') 
                for page in page_frame: 
                    if indexes[page] < lru: 
                        lru = indexes[page] 
                        val = page 

                page_fault_ls.append(i)
                page_frame.remove(val)
                page_frame.append(pageReferList[i])
                page_replaces += 1
            else:
                page_frame.remove(pageReferList[i])
                page_frame.append(pageReferList[i])

            indexes[pageReferList[i]] = i
        
        string = ''.join(map(str, reversed(page_frame)))
        page_frame_ls.append(string)
  
    return page_replaces, page_frame_ls, page_fault_ls

def LFUaddFIFO(pageFrameNum, pageReferList):
    mp = defaultdict(int)
    queue = Queue()
    
    n = len(pageReferList)
    page_replaces = 0
    page_frame_ls = []
    page_fault_ls = []
    for i in range(n):
        if queue.qsize() < pageFrameNum: 
            if pageReferList[i] not in queue.queue:
                page_fault_ls.append(i)
                queue.put(pageReferList[i])
            
            mp[pageReferList[i]] += 1
        else:
            if pageReferList[i] not in queue.queue:
                fp_sort = sorted(mp.items(), key=lambda x: x[1])
                fp_sort_get = [item for item in fp_sort if item[0] in queue.queue]
                min_value = min(fp_sort_get, key=lambda x: x[1])[1]
                min_value_items = [item for item in fp_sort_get if item[1] == min_value]
                j = min(min_value_items, key=lambda x: list(queue.queue).index(x[0]))[0]
                queue.queue.remove(j)
                mp[j] = 0
                queue.put(pageReferList[i])
                page_fault_ls.append(i)
                page_replaces += 1
            
            mp[pageReferList[i]] += 1
        
        string = ''.join(map(str, reversed(queue.queue)))
        page_frame_ls.append(string)

    return page_replaces, page_frame_ls, page_fault_ls

def MFUaddFIFO(pageFrameNum, pageReferList):
    mp = defaultdict(int)
    queue = Queue()

    n = len(pageReferList)
    page_replaces = 0
    page_frame_ls = []
    page_fault_ls = []
    for i in range(n):
        if queue.qsize() < pageFrameNum: 
            if pageReferList[i] not in queue.queue:
                page_fault_ls.append(i)
                queue.put(pageReferList[i])
            
            mp[pageReferList[i]] += 1
        else:
            if pageReferList[i] not in queue.queue:
                fp_sort = sorted(mp.items(), key=lambda x: x[1], reverse=True)
                fp_sort_get = [item for item in fp_sort if item[0] in queue.queue]
                max_value = max(fp_sort_get, key=lambda x: x[1])[1]
                max_value_items = [item for item in fp_sort_get if item[1] == max_value]
                j = min(max_value_items, key=lambda x: list(queue.queue).index(x[0]))[0]
                queue.queue.remove(j)
                mp[j] = 0
                queue.put(pageReferList[i])
                page_fault_ls.append(i)
                page_replaces += 1
            
            mp[pageReferList[i]] += 1
        
        string = ''.join(map(str, reversed(queue.queue)))
        page_frame_ls.append(string)

    return page_replaces, page_frame_ls, page_fault_ls

def LFUaddLRU(pageFrameNum, pageReferList):
    page_frame = []
    mp = defaultdict(int)
    indexes = {}
    
    n = len(pageReferList)
    page_replaces = 0
    page_frame_ls = []
    page_fault_ls = []
    for i in range(n):
        if len(page_frame) < pageFrameNum: 
            if pageReferList[i] not in page_frame:
                page_fault_ls.append(i)
                page_frame.append(pageReferList[i])
            
            mp[pageReferList[i]] += 1
            indexes[pageReferList[i]] = i 
        else:
            if pageReferList[i] not in page_frame:
                fp_sort = sorted(mp.items(), key=lambda x: x[1])
                fp_sort_get = [item for item in fp_sort if item[0] in page_frame]
                min_value = min(fp_sort_get, key=lambda x: x[1])[1]
                min_value_items = [item for item in fp_sort_get if item[1] == min_value]
                j = min(min_value_items, key=lambda x: indexes[x[0]])[0]
                page_frame.remove(j)
                mp[j] = 0
                page_frame.append(pageReferList[i])
                page_fault_ls.append(i)
                page_replaces += 1
            else:
                page_frame.remove(pageReferList[i])
                page_frame.append(pageReferList[i])
            
            mp[pageReferList[i]] += 1
            indexes[pageReferList[i]] = i 
        
        string = ''.join(map(str, reversed(page_frame)))
        page_frame_ls.append(string)

    return page_replaces, page_frame_ls, page_fault_ls

def main():
    fileName = input('Enter file name (eg. input1_method1, input2 ...) : ')
    inputFile = fileName + '.txt'
    outputFile = 'out_' + inputFile
    method, pageFrameNum, pageReferList = read_input_file(inputFile)
    
    match method:
        case '1':
            page_replaces, page_frame_ls, page_fault_ls = FIFO(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'w', 'FIFO', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, False)
        case '2':
            page_replaces, page_frame_ls, page_fault_ls = LRU(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'w', 'LRU', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, False)
        case '3':
            page_replaces, page_frame_ls, page_fault_ls = LFUaddFIFO(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'w', 'Least Frequently Used Page Replacement', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, False)
        case '4':
            page_replaces, page_frame_ls, page_fault_ls = MFUaddFIFO(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'w', 'Most Frequently Used Page Replacement ', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, False)
        case '5':
            page_replaces, page_frame_ls, page_fault_ls = LFUaddLRU(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'w', 'Least Frequently Used LRU Page Replacement', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, False)
        case '6':
            page_replaces, page_frame_ls, page_fault_ls = FIFO(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'w', 'FIFO', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, True)
            
            page_replaces, page_frame_ls, page_fault_ls = LRU(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'a', 'LRU', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, True)
            
            page_replaces, page_frame_ls, page_fault_ls = LFUaddFIFO(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'a', 'Least Frequently Used Page Replacement', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, True)
            
            page_replaces, page_frame_ls, page_fault_ls = MFUaddFIFO(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'a', 'Most Frequently Used Page Replacement ', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, True)
            
            page_replaces, page_frame_ls, page_fault_ls = LFUaddLRU(pageFrameNum, pageReferList)
            write_output_file(outputFile, 'a', 'Least Frequently Used LRU Page Replacement', pageFrameNum, 
                              pageReferList, page_replaces, page_frame_ls, page_fault_ls, False)
        case _:
            print('Invalid method')

    print('\n### Results in ' + outputFile + ' ###\n')

if __name__ == "__main__":
    main()
