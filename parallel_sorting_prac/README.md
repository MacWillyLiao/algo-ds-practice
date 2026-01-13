# parallel_sorting_prac
This practice implements four variations of sorting N numbers using BubbleSort and MergeSort, with measurements of CPU execution time under different parallel models.

## 實現以下四種方法
**method 1**：將 N 筆數字直接進行 BubbleSort，並顯示 CPU 執行之時間  
**method 2**：將 N 筆數字切成 K 份，先在一個 process 內對 K 份資料進行 BubbleSort 之後，再用同一個 process 作 MergeSort，並顯示CPU執行之時間  
**method 3**：將 N 筆數字切成 K 份，並由 K 個 processes 各別進行 BubbleSort 之後，再用 K-1 個 process（es）作 MergeSort，並顯示 CPU 執行之時間  
**method 4**：將 N 筆數目字切成 K 份，並由 K 個 threads 各別進行 BubbleSort 之後，再用 K-1 個 thread（s）作 MergeSort，並顯示 CPU 執行之時間

## 讀檔格式
測資放在 [`input/`](input/) 資料夾中，如：
- 一萬筆資料：[input_1w.txt](input/input_1w.txt)
- 十萬筆資料：[input_10w.txt](input/input_10w.txt)
- 五十萬筆資料：[input_50w.txt](input/input_50w.txt)
- 一百萬筆資料：[input_100w.txt](input/input_100w.txt)

## 寫檔格式
Output 檔名格式：{ Input File Name }_output{ Method Number }.txt，如 [`output/`](output/) 資料夾中的檔案，此資料夾有所有資料筆數及方法的輸出。每個檔案有排序完的資料、執行時間和 Output Time，如以下：
```
Sort :
8
12
13
14
... 略 ...
49982
49985
49988
50000
CPU Time : 2526.2702920008450747
Output Time : 2024-11-20 15:16:04.000404+08:00
```

## 程式執行方式
[main.py](main.py) 編譯並執行後會提供輸入
- 範例一：不需要輸入 K  
method: 1
    ```
    Enter file name: input_1w
    Enter method number: 1 
    ```
- 範例二：需要輸入 K  
method: 2, 3, 4
    ```
    Enter file name: input_1w
    Enter method number: 3
    Enter number of segments (K): 10
    ```

## 結果
詳細書面報告在 [report.pdf](report.pdf) 中
