graph = {"A": ["D", "F", "B"],
         "B": ["C"],
         "C": [],
         "D": ["E"],
         "E": ["G"],
         "F": [],
         "G": []}


def dfs_non_recursive(graph, source, goal):
    if source is None or source not in graph:
        return "Invalid input"

    path = []  # path to goal
    parent = {} # stores parent of each node

    stack = [source]

    while len(stack) != 0:

        s = stack.pop()

        if s == goal:
            path.append(goal)
            while(s in parent.keys()):
                path.append(parent[s])
                s = parent[s]
            return path[::-1]  # reverse of path

        if s not in graph:
            # leaf node
            continue

        for neighbor in graph[s]:
            stack.append(neighbor)
            parent[neighbor] = s

    return path


DFS_path = dfs_non_recursive(graph, "A", "G")
print(DFS_path)