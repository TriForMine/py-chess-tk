class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def __str__(self):
        res = ""
        res += str(self.data) + "\n"
        for node in self.children:
            res += "-- " + str(node) + "\n"
        return res

    def add_node(self, obj):
        self.children.append(obj)

    def get_children_data(self):
        res = []
        for node in self.children:
            res.append(node.data)
        return res
