import matplotlib.pyplot as plt
import numpy as np
import time

from ShardTree import AccountBasedShardTree

# --------------------------------------------------------------------------------------
# ------------------------ RUN TEST FUNCTIONS ------------------------------------------
# --------------------------------------------------------------------------------------

def save_graph(d):
    global IMG_SEQ
    d.render(IMG_FOLDER_PATH+str(IMG_SEQ)+".gv", view=False)
    IMG_SEQ += 1

def run_iteration(shard_tree):
    shard_tree.balance_shards()
    shard_loads = [shard.load for shard in shard_tree.shards]
    EXP_VARIANCE.append(np.var(shard_loads))
    d = shard_tree.build_graph()
    save_graph(d)

# --------------------------------------------------------------------------------------
# ------------------------ MAIN CODE ---------------------------------------------------
# --------------------------------------------------------------------------------------

IMG_FOLDER_PATH = "./data/"+str(time.time())+"/"
IMG_SEQ = 0
EXP_VARIANCE = []
shard_tree = AccountBasedShardTree()
shard_tree.build_complete_binary_tree(2)

for account in shard_tree.accounts:
    print("Account:", account.id)
    print("Linked Accounts:", [a.id for a in account.linked_accounts])
    print("-------------------")

print("********************************************")
print("********************************************")
print("********************************************")


for shard in shard_tree.shards:
    print("Shard:", shard.id)
    print("Accounts:", [account.id for account in shard.load])
    print("-------------------")

shard_tree.build_graph().view()

# for i in range(10):
#     run_iteration(shard_tree)
