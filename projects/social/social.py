import numpy as np
from random import randint
from util import Queue


class User:
    def __init__(self, name):
        self.name = name
        self.friends = set()

    def add_friend(self, friend):
        self.friends.add(friend)


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.users[user_id].add_friend(self.users[friend_id])
            self.friendships[friend_id].add(user_id)
            self.users[friend_id].add_friend(self.users[user_id])

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def first_pass_populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(1, num_users+1):
            self.add_user(i)
        # Create friendships
        friends = np.random.normal(loc=avg_friendships, size=num_users)
        for i in range(1, self.last_id):
            for j in range(int(friends[i-1])):
                friend = randint(i+1, self.last_id)
                self.add_friendship(i, friend)

    def populate_graph(self, users, friends):
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(1, users+1):
            self.add_user(f'User {i}')

        possible_friends = [[False for _ in range(self.last_id)] for _ in range(self.last_id)]
        for i in range(users * friends // 2):
            a, b = (randint(1, self.last_id), randint(1, self.last_id))
            while possible_friends[a-1][b-1] or a == b:
                a, b = (randint(1, self.last_id), randint(1, self.last_id))
            possible_friends[a-1][b-1] = True
            possible_friends[b-1][a-1] = True
            self.add_friendship(a, b)

    def connected_network_percent(self, user):
        ''' user is an id, this returns what percent of the network
        is connected to that user by any degree of seperation'''
        network = self.get_all_social_paths(user)
        return (len(network) - 1)/len(self.users) * 100

    def average_degrees_seperation(self, user):
        ''' user is a user_id
        this returns the average degrees of seperation from a user to the
        rest of the social network'''
        network = self.get_all_social_paths(user).values()
        seperation = [len(i) for i in network]
        return (float(sum(seperation)) / len(seperation))

    def check_average_friends(self):
        friends = self.friendships.values()
        lengths = [len(i) for i in friends]
        return (float(sum(lengths)) / len(lengths))

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {user_id: [user_id]}  # Note that this is a dictionary, not a set
        q = Queue()
        q.enqueue((user_id, None))
        while q.size() > 0:
            n, t = q.dequeue()
            if n not in visited:
                visited[n] = visited[t] + [n]
                for x in self.friendships[n]:
                    q.enqueue((x, n))
            if n == user_id:
                for x in self.friendships[n]:
                    q.enqueue((x, n))
        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    # sg.populate_graph(10, 2)
    print(sg.connected_network_percent(1))
    print(sg.average_degrees_seperation(1))
    # connections = sg.get_all_social_paths(1)
    # print(connections)
