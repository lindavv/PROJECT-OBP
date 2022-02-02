import matplotlib.pyplot as plt
import os
from stuff.map_dfs import *
import networkx as nx

def make_map(orders, id, n):
    # Find the coordinates at which all nodes should be plotted
    pos = {k: (lon, lat) for k, (lat, lon) in nx.get_node_attributes(g, "coordinate").items()}

    fig= plt.figure(frameon=False)
    fig.set_size_inches(7,5)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)

    # Plot all nodes and edges
    nx.draw_networkx_nodes(g, pos=pos, node_color="black", node_size=0.1);
    nx.draw_networkx_nodes(g, pos = pos, nodelist=[i for i in restaurant_indices], node_color="black", node_size=28);
    nx.draw_networkx_edges(g,pos=pos, width=0.5, arrows=False, edge_color='grey');

    route = orders[id].vehicle.route
    if orders[id].status == 'Preparing' or orders[id].status == 'Driving':
        j = 0
        rest = 0
        for k in range(len(route)):
            if route[k].type_ == 1:
                if route[k].order.id == id:
                    j=k
            elif route[k].type_ == 0:
                if route[k].order.id == id:
                    rest=k

        route = route[:k+1]

        # current position
        nx.draw_networkx_nodes(g, pos=pos, nodelist=[route[0].location], node_color="green", node_size = 100)

        # drop off node (customer)
        nx.draw_networkx_nodes(g, pos=pos, nodelist=[route[-1].location], node_color="purple", node_size=100)

        # restaurant node (unless current position is restautant)
        if rest > 0:
            nx.draw_networkx_nodes(g, pos=pos, nodelist=[route[rest].location], node_color="purple", node_size=100)

        for k in range(len(route)-1):
            r = nx.algorithms.shortest_path(g, route[k].location, route[k+1].location, weight= "time")
            nx.draw_networkx_edges(g.edge_subgraph(zip(r, r[1:])), pos=pos, width=5, arrows=False, edge_color="red")










    plt.savefig(os.getcwd() + "\DSS\pics\map_"+ str(n)+".png")
    plt.clf()
    plt.cla()
    plt.close(fig)