import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp

# use (i,j,k) notation to label each node for networkx.
# i+j+k = 3*(n-1) so k is redundent
# i,j,k \in [0, 2*(n-1)]

def construct_network(n):
    G = nx.Graph()
    for i in range(2 * n - 1):
        for j in range(2 * n-1):
            k = 3 * (n-1) - i - j
            if k >= 0 and k < 2 * n - 1:
                for (a,b) in [(-1,0),
                                (-1,1),
                                (0,1)]:
                    k_prime = k - a - b
                    if k_prime >= 0 and k_prime < 2 * n - 1:
                        if 0 <= i+a < 2*n - 1 and 0 <= j+b < 2*n - 1:
                            G.add_edge((i,j), (i+a, j+b))
                        if 0 <= i+b < 2*n - 1 and 0 <= j+a < 2*n - 1:
                            G.add_edge((i,j), (i+b, j+a))
    return G

n = 8
G = construct_network(n)
pos = nx.nx_agraph.graphviz_layout(G)

plt.figure(figsize=(10,10))
ax = plt.gca()
ax.set_title(f"Triangular lattice with N: {n}", fontsize=24)
nx.draw(G, with_labels=False, ax=ax, pos=pos)
_ = ax.axis('off')
plt.savefig("figs/2021_POCS_Assignment_3_network_q5.pdf", bbox_inches="tight")
# plt.show()

A = nx.adjacency_matrix(G).todense()

plt.figure(figsize=(10,10))
ax = plt.gca()
ax.imshow(A, cmap="gray")
ax.set_title(f"Adjacency Matrix for triangular lattice with N: {n}", fontsize=24)
# _ = ax.axis("off")
plt.savefig("figs/2021_POCS_Assignment_3_q5_adj_matrix.pdf", bbox_inches="tight")