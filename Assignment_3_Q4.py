import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("../data/pinon_master.csv")
df_sub = df[["nodeid", "parent", "diameter"]]

num_rows = df.shape[0]

# Murray's Law: R_0^3 = R_1^3 + ... + R_n^3
parent_children_sizes = {}
parent_sizes = {}

node_ids_to_idx = dict(zip(list(df["nodeid"].values),
                            list(range(1, num_rows+1))))

node_ids_to_idx[0.0] = 0

for (nodeid, parentid, diameter) in df_sub.values:
    parent_idx = node_ids_to_idx[parentid]
    if parent_idx not in parent_children_sizes:
        parent_children_sizes[parent_idx] = [diameter]
    else:
        parent_children_sizes[parent_idx].append(diameter)
    parent_sizes[node_ids_to_idx[nodeid]] = diameter

parent_children_sizes
parent_sizes

murray_law_data = []
for parent_idx, children_sizes in parent_children_sizes.items():
    if parent_idx == 0:
        continue
    parent_size_cubed = parent_sizes[parent_idx]**3
    children_sizes_cubed = np.power(np.array(children_sizes), 3)
    sum_children_sizes_cubed = np.sum(children_sizes_cubed)
    murray_law_data.append((parent_size_cubed, sum_children_sizes_cubed))

x, y = zip(*murray_law_data)
min_val = min(np.min(x), np.min(y))
max_val = max((np.max(x), np.max(y)))
plt.scatter(x, y, s=0.5, c="k", label="Observed Branching Structure")

plt.plot((min_val, max_val), (min_val, max_val), label="Murray's Law")
plt.xlabel("$\sum_{i = 0}^{N} {r_i^3}$")
plt.ylabel("$r_j^3$")
plt.legend()
plt.loglog()
plt.savefig("figs/2021_POCS_Assignment_q4.pdf",bbox_inches="tight")
plt.show()