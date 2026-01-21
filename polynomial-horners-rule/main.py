import re
from collections import defaultdict

# 解析多項式字串成係數列表（高次在前）
def parse_polynomial(expr):
    expr = expr.replace(' ', '').replace('-', '+-')
    terms = expr.split('+')
    poly = defaultdict(int)
    for term in terms:
        if not term:
            continue
        if 'x^' in term:
            coef, exp = term.split('x^')
            coef = int(coef) if coef not in ('', '+') else 1
            coef = -1 if coef == '-' else coef
            exp = int(exp)
        elif 'x' in term:
            coef = term.replace('x', '')
            coef = int(coef) if coef not in ('', '+') else 1
            coef = -1 if coef == '-' else coef
            exp = 1
        else:
            coef = int(term)
            exp = 0
        poly[exp] += coef
    max_exp = max(poly.keys()) if poly else 0
    result = [0] * (max_exp + 1)
    for exp, coef in poly.items():
        result[-(exp + 1)] = coef
    return result


# 加法
def add_poly(p1, p2):
    diff = len(p1) - len(p2)
    if diff > 0:
        p2 = [0]*diff + p2
    elif diff < 0:
        p1 = [0]*(-diff) + p1
    return [a + b for a, b in zip(p1, p2)]


# 乘法
def multiply_poly(p1, p2):
    result = [0]*(len(p1) + len(p2) - 1)
    for i in range(len(p1)):
        for j in range(len(p2)):
            result[i + j] += p1[i] * p2[j]
    return result


# 代入
def evaluate_poly(poly, x):
    result = 0
    for coef in poly:
        result = result * x + coef
    return result


# 格式化
def format_poly(poly):
    result = []
    degree = len(poly) - 1
    for i, coef in enumerate(poly):
        if coef == 0:
            degree -= 1
            continue
        if degree == 0:
            term = f"{coef}"
        elif degree == 1:
            term = f"{'' if coef == 1 else '-' if coef == -1 else coef}x"
        else:
            term = f"{'' if coef == 1 else '-' if coef == -1 else coef}x^{degree}"
        result.append(term)
        degree -= 1
    return ' + '.join(result).replace('+ -', '- ') if result else '0'


def main():
    polys = {}
    commands = []

    print("請輸入多項式定義與運算（輸入 0 結束）：")
    while True:
        line = input().strip()
        if line == '0':
            break
        if line:
            commands.append(line)

    for line in commands:
        try:
            if '=' in line:
                name, expr = line.split('=')
                name = name.strip()
                if name.endswith('(x)'):
                    name = name[:-3]
                expr = expr.strip()
                polys[name] = parse_polynomial(expr)

            elif '(' in line and ')' in line:
                match = re.findall(r'(\w+)\(([^)]+)\)', line)
                if not match:
                    print(f"{line} -> 輸入格式錯誤")
                    continue
                name, val = match[0]
                if val == 'x':
                    if '+' in line:
                        p1, p2 = line.split('+')
                        p1_name, p2_name = p1.strip()[:-3], p2.strip()[:-3]
                        result = add_poly(polys[p1_name], polys[p2_name])
                        print(f"{line} = {format_poly(result)}")
                    elif '*' in line:
                        p1, p2 = line.split('*')
                        p1_name, p2_name = p1.strip()[:-3], p2.strip()[:-3]
                        result = multiply_poly(polys[p1_name], polys[p2_name])
                        print(f"{line} = {format_poly(result)}")
                else:
                    x = int(val)
                    result = evaluate_poly(polys[name], x)
                    print(f"{line} = {result}")
        except Exception as e:
            print(f"{line} -> 錯誤：{e}")

if __name__ == "__main__":
    main()
