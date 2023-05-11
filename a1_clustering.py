import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cluster import AgglomerativeClustering
colors = ['white', 'g', 'b', 'c', 'm', 'y', 'k', 'w', 'orange', 'purple',\
        'brown', 'pink', 'gray', 'olive', 'cyan', 'lime', 'teal', 'lavender',\
        'maroon', 'navy', 'gold', 'salmon', 'tan', 'aqua', 'indigo', 'azure',\
        'beige', 'coral', 'crimson', 'fuchsia', 'honeydew', 'ivory', 'khaki',\
        'linen', 'magenta', 'plum', 'snow', 'thistle', 'wheat', 'yellowgreen']

def makeClusters(dist, threshold, linkage="average", image=True):
    THRESHOLD = threshold
    dist_np = np.array(dist)
    rows, cols = dist_np.shape
    close_mat = np.where(dist_np <= THRESHOLD, 0, 1)
    cmap = ListedColormap(["black", "white"])
    if image:
        fig, axes = plt.subplots(1,2,figsize=(30, 15))
        axes[0].imshow(close_mat, cmap=cmap)
        axes[0].set_xticks(np.arange(cols))
        axes[0].set_yticks(np.arange(rows))
        axes[0].grid(False)
    
    hc = AgglomerativeClustering(metric="precomputed", linkage="average", distance_threshold=THRESHOLD, n_clusters=None)
    labels = hc.fit_predict(dist_np)
    clustering_dict_nodes = {}
    clustering_dict_labels = {}
    for i,l in enumerate(labels):
        clustering_dict_nodes[i] = l
        if l not in clustering_dict_labels.keys():
            clustering_dict_labels[l] = [i]
        else:
            clustering_dict_labels[l].append(i)
    cmap1 = ListedColormap(colors[:len(clustering_dict_labels.keys())])
    cluster_mat = np.zeros((rows, cols))
    for i in range(rows):
        for j in range(cols):
            if clustering_dict_nodes[i] == clustering_dict_nodes[j]:
                cluster_mat[i, j] = clustering_dict_nodes[i] + 1
    if image:
        axes[1].imshow(cluster_mat, cmap=cmap1)
        axes[1].set_xticks(np.arange(cols))
        axes[1].set_yticks(np.arange(rows))
        axes[1].grid(False)
        plt.show()
    num_clusters = len(clustering_dict_labels.keys())
    return num_clusters, labels, clustering_dict_nodes, clustering_dict_labels
