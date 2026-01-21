def find_hamiltonian_cycle(graph, path, visited, n):
    if len(path) == n:
        if path[0] in graph[path[-1]]:
            path.append(path[0])
            return True
        return False

    current = path[-1]
    for neighbor in graph[current]:
        if visited[neighbor] == False:
            visited[neighbor] = True
            path.append(neighbor)

            if find_hamiltonian_cycle(graph, path, visited, n):
                return True

            path.pop()
            visited[neighbor] = False

    return False


def main():
    vertex, edge = map(int, input().split())
    data = []
    while True:
        line = input()
        if line == '0 0':
            break
        data.append(line)

    graph = {i: [] for i in range(1, vertex + 1)}
    for s in data:
        u, v = map(int, s.split())
        graph[u].append(v)
        graph[v].append(u)
    
    path = [1]
    visited = {i: False for i in range(1, vertex + 1)}
    visited[1] = True
    if find_hamiltonian_cycle(graph, path, visited, vertex):
        print(" ".join(map(str, path)))
    else:
        print("No Hamiltonian Cycle found")

if __name__ == "__main__":
    main()