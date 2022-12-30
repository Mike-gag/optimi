from matplotlib import pyplot as plt

import SolutionDrawer
from VRP_Model import *


class Solution:

    def __init__(self):
        self.cost = 0.0
        self.routes = []
    
    def print_results(self):
        tot_cost = 0
        true_total_cost = 0
        for k in self.routes:
            for n in k.sequenceOfNodes:
                print(str(n.ID) + ", ", end="")
            print()
            tot_cost+=k.cost
            rt_cost, load = calculate_route_details(k.sequenceOfNodes)
            true_total_cost+=rt_cost

        print(tot_cost)
        print(true_total_cost)


class Saving:
    def __init__(self, n1, n2, sav):
        self.n1 = n1
        self.n2 = n2
        self.score = sav


class Solver:

    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix
        self.capacity = m.capacity
        self.sol = None
        self.bestSolution = None
        self.no_of_vehicles = 14
        self.used = {self.depot.ID}

    #vriskei ton kontinotero komvo sto route r pou exei teleutaio komvo ton n
    #dinei to index tou komvou kai to dist tou apo ton n
    def find_node(self,r, n):
        dist = self.distanceMatrix[n.ID]
        nearest_v = 10000000
        nearest_index = 0
        for i in range(0, len(dist) - 1):
            if dist[i] < nearest_v and i not in self.used and r.load + self.allNodes[i].demand < r.capacity:
                nearest_index = i
                nearest_v = dist[i]
        self.used.add(nearest_index)
        return nearest_index, nearest_v

    #ftiaxnei arxikh lysh nearest neighbor 
    #epi tou solution attribute tou solver object (self.sol)
    def nearestneighbor(self):
        for i in range(0, self.no_of_vehicles):
            self.sol.routes.append(Route(self.depot, self.capacity))
        j = 0
        for i in range(1, len(self.allNodes) - 1):
            route = self.sol.routes[j % self.no_of_vehicles]
            node = route.sequenceOfNodes[-1]
            nearest_possible, value = self.find_node(route, node)
            self.allNodes[nearest_possible].isRouted = True
            if(len(route.sequenceOfNodes)==1):
                self.allNodes[nearest_possible].waitingtime = value
                print("here1")
            else:
                self.allNodes[nearest_possible].waitingtime=route.sequenceOfNodes[-1].waitingtime + value
                print("here2")
            route.load += self.allNodes[nearest_possible].demand
            route.cost += self.allNodes[nearest_possible].waitingtime
            self.allNodes[nearest_possible].waitingtime += 10
            route.sequenceOfNodes.append(self.allNodes[nearest_possible])



            j += 1
    #solve
    # otan mpoun kai ta operators tha kallountai apo edw oxi sth main 
    def solve(self):
            
        model = Model()
        model.BuildModel()

        self.sol = Solution()
        self.nearestneighbor()

        self.sol.print_results()


#eykleidia apostash 2 komvwn
def distance(from_node, to_node):
    dx = from_node.x - to_node.x
    dy = from_node.y - to_node.y
    dist = math.sqrt(dx ** 2 + dy ** 2)
    return dist

#dwse ena route
#pare pisw to cost kai ton forto
def calculate_route_details(nodes_sequence):
    rt_load = 0
    rt_cumulative_cost = 0
    tot_time = 0
    for i in range(len(nodes_sequence) - 1):
        from_node = nodes_sequence[i]
        to_node = nodes_sequence[i + 1]
        tot_time += distance(from_node, to_node)
        rt_cumulative_cost += tot_time
        tot_time += 10
        rt_load += from_node.demand
    return rt_cumulative_cost, rt_load


# plot solution
# for r in range(0, len(sol.routes)):
#     rt = sol.routes[r]
#     for i in range(0, len(rt.sequenceOfNodes) - 1):
#         c0 = rt.sequenceOfNodes[i]
#         c1 = rt.sequenceOfNodes[i + 1]
#         plt.plot([c0.x, c1.x], [c0.y, c1.y])
#
# plt.show()

#edw einai h main
#apla ftiaxneis ena solver kai patas .solve() gia na pareis lysh
#.print_results() gia apotelesmata
if __name__=="__main__":

    model = Model()
    model.BuildModel()

    solver = Solver(model)
    solver.solve()
    solver.sol.print_results()
