import re
import itertools
import math
import multiprocessing
import ctypes

class Graph:
    def __init__(self, MAX_TIME):
        self.Nodes = {}
        self.Edges = {}
        self.time = [0]
        self.volume = [0]
        self.total_pressure = [0]
        self.pressure = [0]
        self.MAX_TIME = MAX_TIME

    def add_node(self, name: str, pressure: int):
        self.Nodes[name] = {"pressure": pressure, "flowing": False}
    
    def add_edge(self, first_node: str, second_node: str):
        if first_node in self.Edges:
            self.Edges[first_node].append(second_node)
        else:
            self.Edges[first_node] = [second_node]

    def shortest_path(self, start, dest):
        if dest == "":
            return []

        dist_tree = Graph(self.MAX_TIME)
        remaining_nodes = set(self.Nodes.keys())
        search_list = [start]
        remaining_nodes.remove(start)
        while len(search_list) > 0:
            explored_node = search_list.pop(0)
            neighbors = self.Edges[explored_node]
            for neighbor in neighbors:
                if neighbor in remaining_nodes:
                    search_list.append(neighbor)
                    remaining_nodes.remove(neighbor)
                    dist_tree.add_edge(neighbor, explored_node)

        node = dest
        path = [dest]
        while node != start:
            node = dist_tree.Edges[node][0]
            path.append(node)

        path.pop(0)
        path.reverse()
        return path

    def fit_shortest_paths(self):
        keys = list(self.Nodes.keys())
        keys.sort()
        self.shortest_paths = {}
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                self.shortest_paths[(keys[i], keys[j])] = self.shortest_path(keys[i], keys[j])

        return self.shortest_paths

    def increment_time(self, times):
        new_time = times[-1] - self.time[-1]

        if self.MAX_TIME > new_time:
            self.volume.append(self.volume[-1] + self.total_pressure[-1] * new_time)
            self.time.append(times[-1])
        else:
            self.volume.append(self.volume[-1] + self.total_pressure[-1] * (self.MAX_TIME - self.time[-1]))
            self.time.append(self.MAX_TIME)

    def increment_pressure(self, nodes):
        pressure_arr = []
        is_empty = True
        for name in nodes:
            if name != "" and self.Nodes[name]["pressure"] != self.pressure[-1]:
                pressure_term = self.Nodes[name]["pressure"]
                self.pressure.append(pressure_term)
                pressure_arr.append(pressure_term)
                is_empty = False

        if is_empty:
            self.pressure.append(0)
        self.total_pressure.append(self.total_pressure[-1] + sum(pressure_arr))


    def reset(self):
        for name in self.Nodes:
            self.Nodes[name]["flowing"] = False
        self.total_pressure = [0]
        self.volume = [0]
        self.time = [0]

    def step_back(self):
        self.volume.pop()
        self.total_pressure.pop()
        self.pressure.pop()
        self.time.pop()


class Agent:

    def __init__(self, g:Graph):
        self.g = g
        self.move_num = 0
        self.total_moves = [0]
        self.nodes_reached = ["AA"]

    def move(self, new_node):

        src_dest = [self.nodes_reached[-1], new_node]
        src_dest.sort()

        path = self.g.shortest_paths[tuple(src_dest)]
        self.move_num += len(path)
        if len(path) > 0 and self.g.time[-1] + self.move_num + 1 < self.g.MAX_TIME:
            self.nodes_reached.append(new_node)
        else:
            self.move_num = 0

    def wait(self):
        if self.g.time[-1] + self.move_num < self.g.MAX_TIME:
            self.move_num += 1

    def open(self):
        self.move_num += 1
        self.g.Nodes[self.nodes_reached[-1]]["flowing"] = True
        return self.nodes_reached[-1]


    def end_turn(self):
        self.total_moves.append(self.total_moves[-1] + self.move_num)
        self.move_num = 0

    def reset(self):
        self.total_moves = 0
        self.move_num = 0
        self.nodes_reached = ["AA"]

    def step_back(self):
        self.nodes_reached.pop()
        self.total_moves.pop()

    def reverse_wait(self):
        self.total_moves.pop()


def create_graph(name, MAX_TIME):
    g = Graph(MAX_TIME)
    pattern = "Valve ([A-Z]{2}) has flow rate=([\d]+); tunnels* leads* to valves* ((?:[A-Z]{2}, )*)([A-Z]{2})"
    f = open(name)
    for line in f:
        matches = re.search(pattern, line).groups()
        node = matches[0]
        pressure = int(matches[1])
        if len(matches[2]) > 0:
            edge_list = re.split(", ", matches[2])
            edge_list[-1] = matches[3]
        else:
            edge_list = [matches[3]]

        g.add_node(node, pressure)
        for edge in edge_list:
            g.add_edge(node, edge)

    g.fit_shortest_paths()
    return g


def run_permutation1(g, nonzero_nodes, agent, max_volume, indent):

    if g.time[-1] >= g.MAX_TIME:
        return max_volume

    node_permutations = itertools.permutations(nonzero_nodes, 1)

    i = 0
    for permutation in node_permutations:
        new_nodes = []
        move_nums = []
        print("{0}:{1}".format(indent, i))
        i += 1
        permutation = permutation[0]

        agent.move(permutation[0])
        if agent.move_num == 0:
            while g.time[-1] + agent.move_num < g.MAX_TIME:
                agent.wait()

            new_nodes.append("")
            move_nums.append(agent.move_num)
            g.increment_time(move_nums[0])
            agent.end_turn()

            if g.volume[-1] > max_volume:
                max_volume = g.volume[-1]

            g.step_back()
            continue

        new_nodes.append(agent.open())
        move_nums.append(agent.move_num)

        g.increment_time(new_nodes, move_nums)
        g.increment_pressure(new_nodes[0])

        nonzero_nodes_copy = nonzero_nodes.copy()
        nonzero_nodes_copy.remove(permutation)
        pressure = list(zip(*nonzero_nodes_copy))
        if len(pressure) > 0:
            pressure = pressure[1]
        volume_bound = sum(pressure, g.total_pressure[-1])*(g.MAX_TIME - g.time[-1]) + g.volume[-1]

        agent.end_turn()
        if max_volume >= volume_bound:
            g.step_back()
            agent.step_back()
            continue

        if g.volume[-1] > max_volume:
            max_volume = g.volume[-1]

        max_volume = run_permutation1(g, nonzero_nodes_copy, agent, max_volume, indent + "*")
        g.step_back()
        agent.step_back()

    if i == 0:
        while g.time[-1] + agent.move_num < g.MAX_TIME:
            agent.wait()

        new_nodes = []
        move_nums = []
        new_nodes.append("")
        move_nums.append(agent.move_num)
        g.increment_time(new_nodes, move_nums)
        agent.end_turn()

        if g.volume[-1] > max_volume:
            max_volume = g.volume[-1]

        g.step_back()

    return max_volume


def aoc16a(name, r=None):
    MAX_TIME = 30
    global g
    g = create_graph(name, MAX_TIME)

    nonzero_nodes = []
    for name in g.Nodes:
        if g.Nodes[name]["pressure"] > 0:
            nonzero_nodes.append((name, g.Nodes[name]["pressure"]))
    nonzero_nodes.sort(key=lambda x: x[1], reverse=True)

    agent = Agent(g)
    max_volume = run_permutation1(g, nonzero_nodes, agent, 0, "")

    print(max_volume)


def run_permutation2(g, nonzero_nodes, agents, max_volume, indent):
    if g.time[-1] >= g.MAX_TIME:
        return max_volume

    node_permutations = itertools.permutations(nonzero_nodes, 2)

    i = 0
    for permutation in node_permutations:
        new_nodes = ["", ""]
        print("{0}:{1}".format(indent, i))
        i += 1

        for perm_num in range(len(permutation)):
            permutation_item = permutation[perm_num]
            agent_num = 0
            end_points1 = [agents[agent_num].nodes_reached[-1], permutation_item[0]]
            end_points2 = [agents[agent_num + 1].nodes_reached[-1], permutation_item[0]]
            end_points1.sort()
            end_points2.sort()
            node_distance1 = agents[agent_num].total_moves[-1] + \
                            len(g.shortest_paths[tuple(end_points1)])
            node_distance2 = agents[agent_num + 1].total_moves[-1] + \
                            len(g.shortest_paths[tuple(end_points2)])

            if agents[agent_num + 1].total_moves[-1] < agents[agent_num].total_moves[-1]:
                agent_num = agent_num + 1
            elif agents[agent_num + 1].total_moves[-1] == agents[agent_num].total_moves[-1] and \
                    node_distance2 < node_distance1:

                agent_num = agent_num + 1

            agents[agent_num].move(permutation_item[0])
            new_nodes[agent_num] = agents[agent_num].open()

            agents[agent_num].end_turn()

            if agents[0].total_moves[-1] < agents[1].total_moves[-1]:
                g.increment_time(agents[0].total_moves)
                g.increment_pressure([agents[0].nodes_reached[-1]])
            elif agents[0].total_moves[-1] > agents[1].total_moves[-1]:
                g.increment_time(agents[1].total_moves)
                g.increment_pressure([agents[1].nodes_reached[-1]])
            else:
                g.increment_time(agents[1].total_moves)
                g.increment_pressure(new_nodes)

        nonzero_nodes_calc = nonzero_nodes.copy()
        nonzero_nodes_copy = nonzero_nodes.copy()
        for item in permutation:
            if g.Nodes[item[0]]["pressure"] in g.pressure:
                nonzero_nodes_calc.remove(item)
            nonzero_nodes_copy.remove(item)

        pressure = list(zip(*nonzero_nodes_calc))
        if len(pressure) > 0:
            pressure = pressure[1]

        volume_bound = sum(pressure, g.total_pressure[-1])*(g.MAX_TIME - g.time[-1]) + g.volume[-1]

        if max_volume >= volume_bound:
            for _ in range(2):
                if len(agents[0].total_moves) > len(agents[1].total_moves):
                    agents[0].step_back()
                else:
                    agents[1].step_back()
                g.step_back()
            continue

        if g.volume[-1] > max_volume:
            max_volume = g.volume[-1]

        max_volume = run_permutation2(g, nonzero_nodes_copy, agents, max_volume, indent + "*")
        for _ in range(2):
            if len(agents[0].total_moves) > len(agents[1].total_moves):
                agents[0].step_back()
            else:
                agents[1].step_back()
            g.step_back()

    if i == 0:
        if agents[0].total_moves[-1] > agents[1].total_moves[-1]:
            last_pressure = agents[0].nodes_reached[-1]
        else:
            last_pressure = agents[-1].nodes_reached[-1]

        for agent_num in range(len(agents)):
            next_num = (agent_num + 1) % len(agents)
            while agents[agent_num].total_moves[-1] + agents[agent_num].move_num < \
                    agents[next_num].total_moves[-1] + agents[next_num].move_num:

                agents[agent_num].wait()

            agents[agent_num].end_turn()

        if agents[0].total_moves[-1] > agents[1].total_moves[-1]:
            g.increment_time(agents[0].total_moves)
        else:
            g.increment_time(agents[1].total_moves)
        g.increment_pressure([last_pressure])

        while agents[0].total_moves[-1] + agents[0].move_num < g.MAX_TIME:
            agents[0].wait()

        agents[0].end_turn()

        g.increment_time(agents[0].total_moves)
        g.increment_pressure(["", ""])

        if g.volume[-1] > max_volume:
            max_volume = g.volume[-1]

        agents[0].reverse_wait()
        for agent in agents:
            agent.reverse_wait()
            g.step_back()



    return max_volume



def aoc16b(name, r=None):
    MAX_TIME = 26
    global g
    g = create_graph(name, MAX_TIME)

    nonzero_nodes = []
    for name in g.Nodes:
        if g.Nodes[name]["pressure"] > 0:
            nonzero_nodes.append((name, g.Nodes[name]["pressure"]))
    nonzero_nodes.sort(key=lambda x: x[1], reverse=True)

    agents = [Agent(g), Agent(g)]
    max_volume = run_permutation2(g, nonzero_nodes, agents, 0, "")

    print(max_volume)

if __name__ == '__main__':
    #aoc16a("input16_test.txt")
    #aoc16a("input16.txt")
    aoc16b("input16_test.txt")
    #aoc16b("input16.txt", r=None)