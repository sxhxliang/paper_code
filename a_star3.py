class node:
    def __init__(self):
        self.H = None
        self.G = 0
        self.F = None
        self.parent = None
        self.is_blocked = False
        self.is_target = False
        self.is_start = False
        self.walked_on = False
    def __str__(self):
        if self.is_blocked:
            return "B"
        elif self.is_target:
            return "X"
        elif self.is_start:
            return "O"
        elif self.walked_on:
            return "*"
        else:
            return " "

def create_map():

    from random import randint
    matrix =[]

    for y in xrange(18):
        matrix.append([])
        for x in xrange(30):
            matrix[y].append(node())
            coin = randint(1,11)
            if coin > 8:
                matrix[y][x].is_blocked = True

    start = (randint(0,9),randint(0,29))
    finish = (randint(0,9),randint(0,29))

    while start == finish:
        finish = (randint(0,10),randint(0,30))

    matrix[start[0]][start[1]].is_start = True
    matrix[start[0]][start[1]].is_blocked = False
    matrix[finish[0]][finish[1]].is_target = True
    matrix[finish[0]][finish[1]].is_blocked = False
    
    return matrix,start,finish

def print_map(matrix):
    temp = [" "+"="*61]
    for row in matrix:
        row_copy = row[:]
        row_copy.insert(0,"|")
        row_copy.append("|")
        temp.append(" ".join(str(i) for i in row_copy))
    temp.append(" "+"="*61)
    info_bar = "|              Start: (%d,%d)  Target: (%d,%d)                    |" % \
           (start_node[0],start_node[1],target_node[0],target_node[1])
    temp.append(info_bar)
    temp.append(" "+"="*61)
    return "\n".join(temp)

def get_neighbors(cur_node):
    y,x = cur_node
    for neighbor in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,-1),(-1,1),(1,1)]:
        ny,nx = neighbor
        yield (ny+y,nx+x)


def get_G(next_node,cur_node):
    cy,cx = cur_node
    ny,nx = next_node
    for dy,dx in [(0,1),(1,0),(-1,0),(0,-1)]:
        if cy+dy == ny and cx+dx == nx:
            return 10
    for dy,dx in [(-1,-1),(-1,1),(1,-1),(1,1)]:
        if cy+dy == ny and cx+dx == nx:
            return 14

def get_H(node,target_node):
    cy,cx = node
    ty,tx = target_node
    if ty > cy:
        y_diff = ty-cy
    else:
        y_diff = cy-ty
    if tx > cx:
        x_diff = tx-cx
    else:
        x_diff = cx-tx
    return (abs(y_diff)+abs(x_diff)) * 10

def get_parent_G(parent):
    py,px = parent
    return new_map[py][px].G

def blocked_corner(neighbor,cur_node):
    y,x = cur_node
    if get_G(neighbor,cur_node) == 14:
        if (y-1,x-1) == neighbor:
            if new_map[y-1][x].is_blocked and new_map[y][x-1].is_blocked:
                return True
        if (y+1,x-1) == neighbor:
            if new_map[y+1][x].is_blocked and new_map[y][x-1].is_blocked:
                return True
        if (y-1,x+1) == neighbor:
            if new_map[y-1][x].is_blocked and new_map[y][x+1].is_blocked:
                return True
        if (y+1,x+1) == neighbor:
            if new_map[y+1][x].is_blocked and new_map[y][x+1].is_blocked:
                return True
    return False

def astar(matrix):
    sy,sx = start_node
    open_list = {start_node:matrix[sy][sx].G}
    closed_list = []

    while True:

        if len(open_list) == 0:
            return False

        cur_node = min(open_list, key=open_list.get)
        
        del open_list[cur_node]
        closed_list.append(cur_node)

        if target_node in closed_list:
            return True

        for neighbor in get_neighbors(cur_node):
            if neighbor not in closed_list:
                y,x = neighbor
                if neighbor in open_list:
                    if get_G(neighbor,cur_node) + get_parent_G(cur_node) < new_map[y][x].G:
                        new_map[y][x].parent = cur_node
                        new_map[y][x].G = get_G(neighbor,cur_node) + get_parent_G(cur_node)
                        new_map[y][x].H = get_H(neighbor,target_node)
                        new_map[y][x].F = new_map[y][x].G + new_map[y][x].H
                    else:
                        pass
                else:                                     
                    new_map[y][x].G = get_G(neighbor,cur_node) + get_parent_G(cur_node)
                    new_map[y][x].H = get_H(neighbor,target_node)
                    new_map[y][x].F = new_map[y][x].G + new_map[y][x].H
                    new_map[y][x].parent = cur_node
                if blocked_corner(neighbor,cur_node):
                    if neighbor == target_node:
                        pass
                    else:
                        closed_list.append(neighbor)
                else:
                    open_list[neighbor] = new_map[y][x].F
                
def setup_failed(matrix):
    for y in xrange(len(matrix)-1):
        for x in xrange(len(matrix[y])-1):
            if matrix[y][x].parent != None:
                matrix[y][x].walked_on = True

if __name__ == "__main__":
    import sys
    import time
    new_map,start_node,target_node = create_map()
    if astar(new_map):

        sys.stdout.write("\n"*20+print_map(new_map))
        sys.stdout.flush()

        cur_node = target_node
        while cur_node != start_node:
            y,x = cur_node
            cur_node = new_map[y][x].parent
            y,x = cur_node
            new_map[y][x].walked_on = True
            sys.stdout.write("\n"*17+print_map(new_map))
            sys.stdout.flush()
            time.sleep(.3)
        print ""
    else:
        setup_failed(new_map)
        print print_map(new_map)
        print "No dice, better luck next time."