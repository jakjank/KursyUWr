from collections import deque

maze = [['X','X','X','X','X','X','X'],
        ['X',' ',' ',' ','X',' ','X'],
        ['X','X','X',' ',' ',' ','X'],
        ['X',' ',' ',' ','X',' ','X'],
        ['X',' ','X',' ',' ',' ','X'],
        ['X',' ','X','X','X',' ','X'],
        ['X',' ','X',' ',' ',' ','X'],
        ['X','X','X','X',' ','X','X']]

# pierwotnie chcialem aby to_visit i visited byly typu deque,
# ale niestety wyrzucalo mi blad 'deque mutated during iteration'.
# i juz nie mialem ochoty na deque :(

def solve_maze(maze, start):
    directions = [(1,0),(-1,0),(0,-1),(0,1)]
    to_visit = []
    visited = []
    paths = {start : [start]}
    to_visit.append(start)

    for cur in to_visit:
        visited.append(cur)

        if cur[0] == 0 or cur[0] == len(maze)-1 or cur[1] == 0 or cur[1] == len(maze[0])-1:
            return paths[cur]
        
        for d in directions:
            x = cur[0]+d[0]
            y = cur[1]+d[1]
            if maze[x][y] == ' ':
                if (x,y) not in visited:
                    to_visit.append((x,y))
                    paths[(x,y)] = paths[cur]+[(x,y)]
 
        
print(solve_maze(maze,(3,1)))