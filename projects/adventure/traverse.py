from world import World
from util import Queue, Stack

from ast import literal_eval


def traverse(world):
    '''this returns a traversal path to move the player through all the rooms
    in world'''

    unvisited = set(world.rooms)
    traversal = []
    current = world.starting_room
    while len(unvisited) > 0:
        print('big loop')
        # go until all exits have been visited using DFS
        visited = set()
        while unvisited_neighbors(visited, current):
            if current != world.starting_room:
                current = next_room(current, visited, traversal)
            visited.add((current, current.id))
            if current.id in unvisited:
                unvisited.remove(current.id)
            if current == world.starting_room:
                current = next_room(current, visited, traversal)
        # start the BFS to find the nearest unvisited exit
        found_path = False
        qu = Queue()
        paths = {current: [current]}
        qu.enqueue((current, None))
        while not found_path and qu.size() > 0:
            n, t = qu.dequeue()
            if n not in paths:
                paths[n] = paths[t] + [n]
                if unvisited_neighbors(visited, n):
                    found_path = True
                    nearest_exit = paths[n]
                enqueue_neighbors(n, qu)
            if n == current:
                enqueue_neighbors(n, qu)
        # get to the nearest exit
        if found_path and len(unvisited > 0):
            current = get_to_exit(current, nearest_exit, traversal)
    return traversal


def get_to_exit(c, nearest_exit, traversal):
    for i in nearest_exit[1:]:
        dir = find_room(c, i)
        traversal.append(dir)
        c = i
    return c


def find_room(c, i):
    if c.n_to:
        if c.n_to == i:
            return 'n'
    if c.e_to:
        if c.e_to == i:
            return 'e'
    if c.s_to:
        if c.s_to == i:
            return 's'
    if c.w_to:
        if c.w_to == i:
            return 'w'
    return 'fail'


def unvisited_neighbors(visited, c):
    available = False
    if c.n_to:
        if c.n_to not in visited:
            available = True
    if c.e_to:
        if c.e_to not in visited:
            available = True
    if c.s_to:
        if c.s_to not in visited:
            available = True
    if c.w_to:
        if c.w_to not in visited:
            available = True
    return available


def next_room(c, visited, traversal):
    if c.n_to:
        if (c.n_to, c.n_to.id) not in visited:
            traversal.append('n')
            return c.n_to
    elif c.e_to:
        if (c.e_to, c.e_to.id) not in visited:
            traversal.append('e')
            return c.e_to
    elif c.s_to:
        if (c.s_to, c.s_to.id) not in visited:
            traversal.append('s')
            return c.s_to
    elif c.w_to:
        if (c.w_to, c.w_to.id) not in visited:
            traversal.append('w')
            return c.w_to
    print('you shouldn"t be here')


def enqueue_neighbors(n, s):
    if n.n_to:
        s.enqueue((n.n_to, n))
    elif n.e_to:
        s.enqueue((n.e_to, n))
    elif n.s_to:
        s.enqueue((n.s_to, n))
    elif n.w_to:
        s.enqueue((n.w_to, n))


if __name__ == '__main__':
    # Load world
    world = World()

    # You may uncomment the smaller graphs for development and testing purposes.
    map_file = "maps/test_line.txt"
    # map_file = "maps/test_cross.txt"
    # map_file = "maps/test_loop.txt"
    # map_file = "maps/test_loop_fork.txt"
    # map_file = "maps/main_maze.txt"

    # Loads the map into a dictionary
    room_graph = literal_eval(open(map_file, "r").read())
    world.load_graph(room_graph)
    world.print_rooms()
    print(traverse(world))
