# 演算法分析機測
# 學號: 11127224 / 11127229
# 姓名: 許宥騏 / 廖翊崴
# 中原大學資訊工程系

def find_around(already_passed, image, height, width, i, j, area):
    if i < 0 or i >= height or j < 0 or j >= width:
        return
    
    if i != 0 and image[i - 1][j] == 1 and (i - 1, j) not in already_passed:  # 上
        already_passed.add((i - 1, j))
        area[0] += 1
        find_around(already_passed, image, height, width, i - 1, j, area)
    if i != height - 1 and image[i + 1][j] == 1 and (i + 1, j) not in already_passed:  # 下
        already_passed.add((i + 1, j))
        area[0] += 1
        find_around(already_passed, image, height, width, i + 1, j, area)
    if j != 0 and image[i][j - 1] == 1 and (i, j - 1) not in already_passed:  # 左
        already_passed.add((i, j - 1))
        area[0] += 1
        find_around(already_passed, image, height, width, i, j - 1, area)
    if j != width - 1 and image[i][j + 1] == 1 and (i, j + 1) not in already_passed:  # 右
        already_passed.add((i, j + 1))
        area[0] += 1
        find_around(already_passed, image, height, width, i, j + 1, area)
    if i != 0 and j != 0 and image[i - 1][j - 1] == 1 and (i - 1, j - 1) not in already_passed:  # 左上
        already_passed.add((i - 1, j - 1))
        area[0] += 1
        find_around(already_passed, image, height, width, i - 1, j - 1, area)
    if i != 0 and j != width - 1 and image[i - 1][j + 1] == 1 and (i - 1, j + 1) not in already_passed:  # 右上
        already_passed.add((i - 1, j + 1))
        area[0] += 1
        find_around(already_passed, image, height, width, i - 1, j + 1, area)
    if i != height - 1 and j != 0 and image[i + 1][j - 1] == 1 and (i + 1, j - 1) not in already_passed:  # 左下
        already_passed.add((i + 1, j - 1))
        area[0] += 1
        find_around(already_passed, image, height, width, i + 1, j - 1, area)
    if i != height - 1 and j != width - 1 and image[i + 1][j + 1] == 1 and (i + 1, j + 1) not in already_passed:  # 右下
        already_passed.add((i + 1, j + 1))
        area[0] += 1
        find_around(already_passed, image, height, width, i + 1, j + 1, area)

    return

def connected_components(image, height, width, output_info, image_num):
    already_passed = set()
    for i in range(height):
        for j in range(width):
            if (i, j) not in already_passed and image[i][j] == 1:
                already_passed.add((i, j))
                area = [1]  # 整數不可變型別，函式呼叫時會 call by value
                find_around(already_passed, image, height, width, i, j, area)
                output_info[image_num].append(area[0])

def main():
    image_num = 1
    output_info = {}
    while True:
        height, width = map(int, input().split())  # 讀取大小
        if height == 0 and width == 0:
            break
            
        image = []  # 二元陣列
        for _ in range(height):
            row = list(map(int, input().strip()))
            image.append(row)
        
        output_info.setdefault(image_num, [])
        connected_components(image, height, width, output_info, image_num)
        image_num += 1

    # 格式化印出 output_info
    for image_num, areas in output_info.items():
        print(f"Image #{image_num}")
        print(f"Number of Connected Components = {len(areas)}")
        for idx, area in enumerate(areas, start=1):
            print(f"Connected Component #{idx} Area = {area}")

        if image_num != list(output_info.keys())[-1]:
            print()

if __name__ == "__main__":
    main()
