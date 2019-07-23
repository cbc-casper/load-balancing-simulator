class Shard:
    def __init__(self, id, load, target, parent=None, depth=0, children=[]):
        self.id = id
        self.load = load
        self.target = target
        self.parent = parent
        self.depth = depth
        self.children = children
