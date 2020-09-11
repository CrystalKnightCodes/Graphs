
from graph import Graph
from util import Stack, Queue

class FamilyTree(Graph):
    def __init__(self, ancestors = []):
        self.vertices = {}
        for ancestor in ancestors:
            self.add_pair(ancestor)

    def add_pair(self, pair):
        if pair[0] not in self.vertices:
            self.vertices[pair[0]] = set()
        if pair[1] not in self.vertices:
            self.vertices[pair[1]] = set()
        self.add_edge(pair[1], pair[0])

    def find_earliest(self, child):
        if child not in self.vertices:
            raise KeyError("Child not found.")
        
        pending = Queue()
        depth = 0

        parents = list(self.get_neighbors(child))

        if not parents:
            return -1

        parents.sort()
        for parent in parents:
            pending.enqueue((parent, depth + 1))

            while len(pending.queue) > 0:
                entry = pending.dequeue()

                if depth != entry[1]:
                    depth = entry[1]
                    parents = [entry[0]]
                else:
                    if entry[0] > parents[0]:
                        parents.append(entry[0])
                    else:
                        parents.insert(0, entry[0])
                
                for parent in self.get_neighbors(entry[0]):
                    pending.enqueue((parent, depth + 1))
            
            return parents[0]


def earliest_ancestor(ancestors, starting_node):
    tree = FamilyTree(ancestors)
    return tree.find_earliest(starting_node)