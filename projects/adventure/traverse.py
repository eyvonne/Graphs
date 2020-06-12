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
        # go until all exits have been visited using DFS
        visited = set()
        while unvisited_neighbors(visited, current):
            visited.add(current)
            if current.id in unvisited:
                unvisited.remove(current.id)
            current = next_room(current, visited, unvisited, traversal)
            if current == next_room(current, visited, unvisited):
                break
        # I need the loop to run one more time than it does, so for now I'll just hack
        visited.add(current)
        if current.id in unvisited:
            unvisited.remove(current.id)
        # start the BFS to find the nearest unvisited exit
        if len(unvisited) > 0:
            # starting the BFS
            found_path = False
            qu = Queue()
            paths = {current: [current]}
            qu.enqueue((current, None))
            while not found_path and qu.size() > 0:
                ne, t = qu.dequeue()
                if ne not in paths:
                    paths[ne] = paths[t] + [ne]
                    if super_unvisited_neighbors(unvisited, ne):  # this needs to be super unvisited
                        found_path = True
                        nearest_exit = paths[ne]
                    enqueue_neighbors(ne, qu)
                if ne == current:
                    enqueue_neighbors(ne, qu)
            # get to the nearest exit
            # if found_path and len(unvisited > 0):
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


def super_unvisited_neighbors(unvisited, c):
    available = False
    if c.n_to:
        if c.n_to.id in unvisited:
            available = True
    if c.e_to:
        if c.e_to.id in unvisited:
            available = True
    if c.s_to:
        if c.s_to.id in unvisited:
            available = True
    if c.w_to:
        if c.w_to.id in unvisited:
            available = True
    return available


def next_room(c, visited, unvisited, traversal=None):
    if c.n_to and c.n_to.id in unvisited:
        if c.n_to not in visited:
            if traversal is not None:
                traversal.append('n')
            return c.n_to
    elif c.e_to and c.e_to.id in unvisited:
        if c.e_to not in visited:
            if traversal is not None:
                traversal.append('e')
            return c.e_to
    elif c.s_to and c.s_to.id in unvisited:
        if c.s_to not in visited:
            if traversal is not None:
                traversal.append('s')
            return c.s_to
    elif c.w_to and c.w_to.id in unvisited:
        if c.w_to not in visited:
            if traversal is not None:
                traversal.append('w')
            return c.w_to
    return c


def enqueue_neighbors(n, s):
    if n.n_to:
        s.enqueue((n.n_to, n))
    if n.e_to:
        s.enqueue((n.e_to, n))
    if n.s_to:
        s.enqueue((n.s_to, n))
    if n.w_to:
        s.enqueue((n.w_to, n))


if __name__ == '__main__':
    # Load world
    world = World()

    # You may uncomment the smaller graphs for development and testing purposes.
    # map_file = "maps/test_line.txt"
    # map_file = "maps/test_cross.txt"
    # map_file = "maps/test_loop.txt"
    map_file = "maps/test_loop_fork.txt"
    # map_file = "maps/main_maze.txt"

    # Loads the map into a dictionary
    room_graph = literal_eval(open(map_file, "r").read())
    world.load_graph(room_graph)
    world.print_rooms()
    path = traverse(world)
    print(path)
    print(len(path))
