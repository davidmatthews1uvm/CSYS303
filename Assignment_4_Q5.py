import networkx as nx
import matplotlib.pyplot as plt
import scipy as sp
import numpy as np

# use (i,j,k) notation to label each node for networkx.
# i+j+k = 3*(n-1) so k is redundent
# i,j,k \in [0, 2*(n-1)]

def symmetrize(a):
    """
    https://stackoverflow.com/questions/2572916/numpy-smart-symmetric-matrix
    Return a symmetrized version of NumPy array a.

    Values 0 are replaced by the array value at the symmetric
    position (with respect to the diagonal), i.e. if a_ij = 0,
    then the returned array a' is such that a'_ij = a_ji.

    Diagonal values are left untouched.

    a -- square NumPy array, such that a_ij = 0 or a_ji = 0, 
    for i != j.
    """
    return a + a.T - np.diag(a.diagonal())

class SymNDArray(np.ndarray):
    """
    https://stackoverflow.com/questions/2572916/numpy-smart-symmetric-matrix
    NumPy array subclass for symmetric matrices.

    A SymNDArray arr is such that doing arr[i,j] = value
    automatically does arr[j,i] = value, so that array
    updates remain symmetrical.
    """

    def __setitem__(self, key, value):
        super(SymNDArray, self).__setitem__(key, value)                    
        super(SymNDArray, self).__setitem__(key, value)                    

def symarray(input_array):
    """
    https://stackoverflow.com/questions/2572916/numpy-smart-symmetric-matrix
    Return a symmetrized version of the array-like input_array.

    The returned array has class SymNDArray. Further assignments to the array
    are thus automatically symmetrized.
    """
    return symmetrize(np.asarray(input_array)).view(SymNDArray)


def normalize_arr(arr, gamma):
    return arr / np.power(np.sum(np.power(arr, gamma)), 1/gamma)
    # return arr / np.linalg.norm(arr, ord=gamma)


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

def run_step(A, K, I_vec, gamma):
    capital_gamma = 2 * gamma / (gamma + 1)
    Lambda = np.diag(np.sum(K, axis=0))

    U_vec = np.linalg.solve(Lambda - K, I_vec)

    xx, yy = np.meshgrid(U_vec, U_vec)
    I_mat = K * (xx - yy)
    K_prime = normalize_arr(np.power(np.abs(I_mat), 2 - capital_gamma), gamma)
    # print(K_prime[0, :10])
    return K_prime

n = 8
G = construct_network(n)
A = nx.adjacency_matrix(G)
A_dense = A.todense()

# gamma = 0.5
number_of_nodes = A.shape[0]

source_node_current = 1e3
sink_node_current = -1 * source_node_current / (number_of_nodes - 1)


I_vec = np.ones(number_of_nodes)
I_vec *= sink_node_current
I_vec[0] = source_node_current
assert I_vec.sum() == 0

for gamma in [0.5, 2.0]:
    K = symarray(np.multiply(A_dense,  np.random.random(A.shape)))
    K = normalize_arr(K, gamma)
    assert (abs(np.power(K, gamma).sum() - 1) < 1e-15)

    for i in range(100):
        try:
            K = run_step(A, K, I_vec, gamma)
        except Exception as e:
            print(e)
            break

    K_np = np.array(K)
    K_np = np.where(np.fromfunction(lambda x,y: y - x > 0, shape=K_np.shape), K_np, 0)
    K_np = K_np[K_np != 0]
    K_np = normalize_arr(K_np, 1)
    G2 = nx.from_numpy_array(np.array(K) + 1e-15 * A.todense())
    edges = G2.edges()
    weights = [edges[edge]["weight"] for edge in edges]
    weights_np = normalize_arr(np.array(weights), 1.0)
    weights_np = np.power(weights_np, 2/3)


    pos = nx.nx_agraph.graphviz_layout(G2)

    plt.figure(figsize=(10,10))
    ax = plt.gca()
    ax.set_title(f"N: {n} | $\gamma = {gamma}$", fontsize=24)
    nx.draw_networkx_edges(G, ax=ax, pos=pos, edgelist=edges, width=weights_np*100)
    _ = ax.axis('off')
    ax.set_xlim(0, 1000)
    ax.set_ylim(0, 1150)
    plt.savefig(f"figs/2021_POCS_Assignment_4_network_q5_gamma_{gamma}.pdf", bbox_inches="tight")

