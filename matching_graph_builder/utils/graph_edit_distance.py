import networkx as nx
from graph_pkg_core.algorithm.graph_edit_distance import GED
from graph_pkg_core.edit_cost.edit_cost_vector import EditCostVector
from graph_pkg_core.edit_cost.edit_cost_dirac import EditCostDirac
import graph_loader.transform.nx_to_anthony_transformer as transformer
import numpy as np

def calculate_ged(source_graph, target_graph, alpha, label_name, attribute_names = None, one_hot = False):
    if attribute_names == [] and not one_hot:
        ged = GED(EditCostDirac(1., 1., 1., 1., 'dirac', alpha = alpha))
    else:
        if one_hot:
            metric = 'dirac'
        else:
            metric = 'euclidean'
        ged = GED(EditCostVector(1., 1., 1., 1., metric, alpha = alpha))
    source_graph_ant = source_graph
    target_graph_ant = target_graph
    if isinstance(source_graph, nx.Graph) and isinstance(target_graph,nx.Graph):
        source_graph_ant = transformer.convert_graph(source_graph,label_name, attribute_names)
        target_graph_ant = transformer.convert_graph(target_graph,label_name, attribute_names)

    edit_cost = ged.compute_edit_distance(source_graph_ant,target_graph_ant)
    edit_path = convert_path(ged.phi)
    c = ged.C
    return edit_path, edit_cost, np.array(c)


def convert_path(phi):
    '''
    Hacky helper method to ensure path compatibility
    '''
    compatibility_path = []
    for i in range(len(phi)):
        compatibility_path.append((i,phi[i]))
    return compatibility_path



def is_insertion(src_node_idx, source_node_names, tar_node_idx, tar_node_names):
    return src_node_idx >= len(source_node_names) and tar_node_idx < len(tar_node_names)


def is_deletion(src_node_idx, source_node_names, tar_node_idx, target_node_names):
    return src_node_idx < len(source_node_names) and tar_node_idx >= len(target_node_names)


def is_substitution(src_node_name, tar_node_name, source_graph, target_graph):
    return source_graph.has_node(src_node_name) and target_graph.has_node(tar_node_name)


def relabel_node(source_graph, src_node_name, target_graph, tar_node_name):
    '''
    Relabel a node that got substituted, if it still exists in the graph
    '''
    if source_graph.has_node(src_node_name):
        target_node_attrs = target_graph.nodes[tar_node_name]
        for key, value in target_node_attrs.items():
            source_graph.nodes[src_node_name][key] = value

    return source_graph


def is_epsilon_epsilon(src_node_idx, src_node_names, tar_node_idx, tar_node_names):
    return src_node_idx >= len(src_node_names) and tar_node_idx >= len(tar_node_names)


def remove_isolated_nodes(graph):
    '''
    This method removes nodes that are not contained in any of the edges
    :param graph:
    :return:
    '''
    result = nx.Graph(graph)
    node_names = list(graph.nodes)
    edges = list(graph.edges)
    nodes_in_edges_one = []
    nodes_in_edges_two = []
    if len(edges) > 0:
        nodes_in_edges_one, nodes_in_edges_two = map(list, zip(*edges))

    for node_name in node_names:
        if node_name not in nodes_in_edges_one and node_name not in nodes_in_edges_two:
            result.remove_node(node_name)

    return result