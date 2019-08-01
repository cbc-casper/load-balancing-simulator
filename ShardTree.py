import random
import graphviz
import matplotlib
import numpy as np

from Shard import Shard
from Account import Account

def get_edge_tuple(shard1, shard2):
    if shard2 in shard1.children:
        return (shard1, shard2)
    elif shard1 in shard2.children:
        return (shard2, shard1)
    assert False, "Shards are not neighbors"

class ShardTree:
    def __init__(self):
        self.root = None
        self.shards = []
        self.shards_depth_map = {}
        self.edges = []
        self.norm = None
        self.cmap = None

    # def inorder_traversal_util(self, root):
    #     if root is not None:
    #         print(root.id)
    #         for child in root.children:
    #             inorder_traversal(child)
    #
    # def inorder_traversal(self):
    #     self.inorder_traversal_util(self.root)

    # ---------------------------------------------------------
    # ------------- BUILD SHARD TREE FUNCTIONS ----------------
    # ---------------------------------------------------------

    def assign_shard_depths_util(self, root):
        if root is not None:
            if root.parent is None:
                root.depth = 0
            else:
                root.depth = root.parent.depth + 1
            for child in root.children:
                self.assign_shard_depths_util(child)

    def assign_shard_depths(self):
        self.assign_shard_depths_util(self.root)

    def get_all_shards_util(self, root):
        if root is None:
            return []
        shards = [root]
        for child in root.children:
            shards.extend(self.get_all_shards_util(child))
        return shards

    def get_all_shards(self):
        return self.get_all_shards_util(self.root)

    def build_shard_depth_map(self):
        shards_depth_map = {}
        for shard in self.shards:
            if shard.depth not in shards_depth_map:
                shards_depth_map[shard.depth] = [shard]
            else:
                shards_depth_map[shard.depth].append(shard)
        return shards_depth_map

    def get_all_edges(self):
        edges = []
        for shard in self.shards:
            edges.extend([(shard, child) for child in shard.children])
        return edges

    def build_complete_binary_tree_util(self, root, depth):
        if(root.depth==depth):
            return
        root.children = [Shard(2*root.id+1, load=[], target=None, parent=root, depth=root.depth+1, children=[]), \
                         Shard(2*root.id+2, load=[], target=None, parent=root, depth=root.depth+1, children=[])]
        self.build_complete_binary_tree_util(root.children[0], depth)
        self.build_complete_binary_tree_util(root.children[1], depth)

    def build_complete_binary_tree(self, depth):
        # Build a complete binary shard tree of specified depth
        # Also sets self.shards and self.shards_depth_map fields
        self.root = Shard(0, load=[], target=None, parent=None, depth=0, children=[])
        self.build_complete_binary_tree_util(self.root, depth)
        self.shards = self.get_all_shards()
        self.shards_depth_map = self.build_shard_depth_map()
        self.edges = self.get_all_edges()

    # ---------------------------------------------------------
    # ------------- TREE UTILITY FUNCTIONS --------------------
    # ---------------------------------------------------------

    def get_lca(self, shard1, shard2):
        higher_depth_shard = shard1 if shard1.depth > shard2.depth else shard2
        lower_depth_shard = shard1 if shard1.depth <= shard2.depth else shard2

        for _ in range(higher_depth_shard.depth-lower_depth_shard.depth):
            higher_depth_shard = higher_depth_shard.parent

        while higher_depth_shard != lower_depth_shard:
            higher_depth_shard = higher_depth_shard.parent
            lower_depth_shard = lower_depth_shard.parent

        assert higher_depth_shard is not None, "Shards do not have an LCA"
        return higher_depth_shard

    def get_path(self, shard1, shard2):
        lca = self.get_lca(shard1, shard2)
        path_shard1_lca = []
        path_shard2_lca = []
        current_shard = shard1
        while current_shard != lca:
            path_shard1_lca.append(get_edge_tuple(current_shard, current_shard.parent))
            current_shard = current_shard.parent
        current_shard = shard2
        while current_shard != lca:
            path_shard2_lca.append(get_edge_tuple(current_shard, current_shard.parent))
            current_shard = current_shard.parent
        path_shard2_lca.reverse()
        return path_shard1_lca + path_shard2_lca

    # --------------------------------------------------
    # ------------- BALANCING FUNCTIONS ----------------
    # --------------------------------------------------

    def choose_shard_to_balance(self):
        # Chooses a shard to balance
        pass

    def balance_shards(self):
        # Chooses a shard to balance and balances it using specified balancing algorithm
        pass

    # -------------------------------------------------
    # ------------- GRAPHVIZ FUNCTIONS ----------------
    # -------------------------------------------------

    def get_shard_label(self, shard):
        # Get graph label for rendering image
        pass

    def build_graph(self):
        # Returns a graph object corresponding to this shard tree
        pass

    def setup_colormap(self):
        # Sets self.colormap for coloring shards according to shard load
        pass

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

class SingleContinuousLoadShardTree(ShardTree):
    # ShardTree that contains Shards with a single, continuous load parameter

    '''
    Example instantiation:
    shard_tree = SingleContinuousLoadShardTree()
    shard_tree.build_complete_binary_tree(2)
    shard_tree.setup_colormap()
    '''

    # ---------------------------------------------------------
    # ------------- BUILD SHARD TREE FUNCTIONS ----------------
    # ---------------------------------------------------------

    def build_complete_binary_tree(self, depth):
        super().build_complete_binary_tree(depth)
        for shard in self.shards:
            shard.load = random.randint(8,17)
        self.assign_target_loads()

    # --------------------------------------------------
    # ------------- BALANCING FUNCTIONS ----------------
    # --------------------------------------------------

    def choose_shard_heavier_than_target(self):
        lucky_shard = random.choice(self.shards)
        while lucky_shard.load <= lucky_shard.target:
            lucky_shard = random.choice(self.shards)
        return lucky_shard

    def choose_shard_to_balance(self):
        return self.choose_shard_heavier_than_target()

    def assign_target_loads(self):
        shard_loads = [shard.load for shard in self.shards]
        target_load = sum(shard_loads)/len(shard_loads)
        min_load = min(shard_loads)
        max_load = max(shard_loads)
        for shard in self.shards:
            shard.target = target_load

    def balance_with_lightest_neighbor(self, lucky_shard):
        lucky_shard_neighbors = [lucky_shard.parent] if lucky_shard.parent is not None else []
        for child in lucky_shard.children:
            lucky_shard_neighbors.append(child)

        min_load_neighbor = lucky_shard_neighbors[0]
        for shard in lucky_shard_neighbors[1:]:
            if shard.load < min_load_neighbor.load:
                min_load_neighbor = shard

        print("min_load_neighbor:", min_load_neighbor.id)

        min_load_neighbor.load += lucky_shard.load-lucky_shard.target
        lucky_shard.load = lucky_shard.target

    def balance_shards(self):
        lucky_shard = self.choose_shard_to_balance()
        print("lucky_shard:", lucky_shard.id)
        self.balance_with_lightest_neighbor(lucky_shard)

    # -------------------------------------------------
    # ------------- GRAPHVIZ FUNCTIONS ----------------
    # -------------------------------------------------

    def get_shard_label(self, shard):
        return '%05.2f'%shard.load + ' (' + '%02d'%shard.id + ')'

    def build_graph(self):
        shards_depth_map = self.shards_depth_map
        d = graphviz.Digraph(format='png')
        d.node_attr.update(style='filled')
        for depth in shards_depth_map.keys():
            s = graphviz.Digraph('subgraph'+str(depth))
            s.graph_attr.update(rank='same')
            for shard in shards_depth_map[depth]:
                node_color = '#%02x%02x%02x' % tuple([int(x*255) for x in self.cmap(self.norm(shard.load))[0:3]])
                s.node(self.get_shard_label(shard), color=node_color)
                for child in shard.children:
                    d.edge(self.get_shard_label(shard), self.get_shard_label(child))
            d.subgraph(s)
        d.node_attr.update(fontname='Courier Bold')
        return d

    def setup_colormap(self):
        shard_loads = [shard.load for shard in self.shards]
        target_load = sum(shard_loads)/len(shard_loads)
        min_load = min(shard_loads)
        max_load = max(shard_loads)
        max_deviation = max(abs(target_load-min_load), abs(max_load-target_load))
        self.norm = matplotlib.colors.Normalize(vmin=target_load-max_deviation, vmax=target_load+max_deviation)
        self.cmap = matplotlib.cm.get_cmap('coolwarm')

# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

class AccountBasedShardTree(ShardTree):
    # ShardTree that contains Shards with Account objects (which have avg. gas consumption, storage size, and communicate with other accounts)

    def __init__(self):
        self.accounts = []
        self.account_shard_map = {}
        self.edge_weights_map = {}
        super().__init__()

    # ---------------------------------------------------------
    # ------------- BUILD SHARD TREE FUNCTIONS ----------------
    # ---------------------------------------------------------

    def build_account_shard_map(self):
        account_shard_map = {}
        for shard in self.shards:
            for account in shard.load:
                account_shard_map[account] = shard
        return account_shard_map

    def build_complete_binary_tree(self, depth):
        # Build the complete binary tree structure
        super().build_complete_binary_tree(depth)

        # Construct Account objects
        accounts_per_shard = 10
        num_shards = (2**(depth+1)-1)
        num_accounts = accounts_per_shard*num_shards
        linked_accounts_per_account = 2
        self.accounts = [ Account(id=x, gas_size=random.randint(1, 20), storage_size=random.randint(1, 100)) for x in range(num_accounts) ]
        for account in self.accounts:
            possible_linked_accounts = self.accounts.copy()
            possible_linked_accounts.remove(account)
            account.linked_accounts = list(np.random.choice(possible_linked_accounts, size=linked_accounts_per_account, replace=False))
            for linked_account in account.linked_accounts:
                account.linked_accounts_tx_count[linked_account] = random.randint(1, 3)

        # Assign accounts to shards
        accounts_list = self.accounts.copy()
        np.random.shuffle(accounts_list)
        for shard in self.shards:
            shard.load = accounts_list[:accounts_per_shard]
            accounts_list = accounts_list[accounts_per_shard:]
        self.account_shard_map = self.build_account_shard_map()
        self.edge_weights_map = self.calculate_edge_weights()

    # ---------------------------------------------------------
    # ------------- TREE UTILITY FUNCTIONS --------------------
    # ---------------------------------------------------------

    def calculate_edge_weights(self):
        edge_weights_map = {}
        for edge in self.edges:
            edge_weights_map[edge] = 0
        for shard in self.shards:
            for account in shard.load:
                for linked_account in account.linked_accounts:
                    path = self.get_path(self.account_shard_map[account], self.account_shard_map[linked_account])
                    for edge in path:
                        edge_weights_map[edge] += account.linked_accounts_tx_count[linked_account]
        return edge_weights_map

    # -------------------------------------------------
    # ------------- GRAPHVIZ FUNCTIONS ----------------
    # -------------------------------------------------

    def get_shard_label(self, shard):
        # shard_label = ", ".join(map(str, [(account.id, account.gas_size) for account in shard.load]))
        # return shard_label + '\n (' + str(shard.id) + ')'
        shard_label = str(sum(list(map(lambda account: account.gas_size, shard.load))))
        return shard_label + ' (' + '%02d'%shard.id + ')'

    def build_graph(self):
        shards_depth_map = self.shards_depth_map
        d = graphviz.Digraph(format='png')
        d.node_attr.update(style='filled')
        d.node_attr.update(fontname='Courier Bold')
        d.edge_attr.update(fontname='Courier Bold')
        for depth in shards_depth_map.keys():
            s = graphviz.Digraph('subgraph'+str(depth))
            s.graph_attr.update(rank='same')
            for shard in shards_depth_map[depth]:
                shard_gas_size_load = sum(list(map(lambda account: account.gas_size, shard.load)))
                node_color = '#%02x%02x%02x' % tuple([int(x*255) for x in self.node_cmap(self.node_cmap_norm(shard_gas_size_load))[0:3]])
                s.node(self.get_shard_label(shard), color=node_color)
                # s.node(shard.get_shard_label(), color='#%02x%02x%02x' % tuple([int(x*255) for x in self.cmap(self.norm(shard.load))[0:3]]))
                for child in shard.children:
                    edge = (shard, child)
                    edge_label = '%03d'%self.edge_weights_map[edge]
                    edge_color = '#%02x%02x%02x' % tuple([int(x*255) for x in self.edge_cmap(self.edge_cmap_norm(self.edge_weights_map[edge]))[0:3]])
                    edge_penwidth = '2.5'
                    # edge_penwidth = str(2*self.edge_cmap_norm(self.edge_weights_map[edge]))
                    d.edge(self.get_shard_label(shard), self.get_shard_label(child), label=edge_label, color=edge_color, penwidth=edge_penwidth)
            d.subgraph(s)
        return d

    def setup_node_colormap(self):
        # shard_loads = [shard.load for shard in self.shards]
        # target_load = sum(shard_loads)/len(shard_loads)
        # min_load = min(shard_loads)
        # max_load = max(shard_loads)
        # max_deviation = max(abs(target_load-min_load), abs(max_load-target_load))
        # self.norm = matplotlib.colors.Normalize(vmin=target_load-max_deviation, vmax=target_load+max_deviation)
        # self.cmap = matplotlib.cm.get_cmap('coolwarm')
        gas_size_loads = [sum(list(map(lambda account: account.gas_size, shard.load))) for shard in self.shards]
        min_gas_size_load = min(gas_size_loads)
        max_gas_size_load = max(gas_size_loads)
        avg_gas_size_load = sum(gas_size_loads)/len(gas_size_loads)
        max_deviation = max( abs(avg_gas_size_load-min_gas_size_load), abs(max_gas_size_load-avg_gas_size_load) )
        self.node_cmap_norm = matplotlib.colors.Normalize(vmin=avg_gas_size_load-2*max_deviation, vmax=avg_gas_size_load+2*max_deviation)
        self.node_cmap = matplotlib.cm.get_cmap('coolwarm')
        # assert False, "Stopping"

    def setup_edge_colormap(self):
        min_edge_wt = min(self.edge_weights_map.values())
        max_edge_wt = max(self.edge_weights_map.values())
        avg_edge_wt = sum(self.edge_weights_map.values())/len(self.edge_weights_map.values())
        max_deviation = max( abs(avg_edge_wt-min_edge_wt), abs(max_edge_wt-avg_edge_wt) )
        self.edge_cmap_norm = matplotlib.colors.Normalize(vmin=avg_edge_wt-2*max_deviation, vmax=avg_edge_wt+2*max_deviation)
        self.edge_cmap = matplotlib.cm.get_cmap('coolwarm')
