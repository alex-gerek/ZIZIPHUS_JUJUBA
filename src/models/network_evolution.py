"""
ZIZIPHUS JUJUBA: Network Evolution & Topological Dynamics Engine.
Analyzes graph structure across chronological epochs (2011-2013, 2014-2015,
2016-2019, 2020-2022) to trace community emergence, degree distributions,
clustering coefficients, and structural bridges.
"""

import sqlite3
import collections
from typing import Dict, Any, List, Optional
import networkx as nx


EPOCHS = [
    {
        "id": "epoch_1",
        "name": "2011–2013: Early Modern Era (УЗБ-76 / Initial МДЖБ)",
        "start_year": 2010,
        "end_year": 2013
    },
    {
        "id": "epoch_2",
        "name": "2014–2015: Donbas Crisis & Codebook Peak (МДЖБ, ЗИЗИФУС, ПАСКОИТ)",
        "start_year": 2014,
        "end_year": 2015
    },
    {
        "id": "epoch_3",
        "name": "2016–2019: Command Rotation (ЖУОЗ & АНВФ)",
        "start_year": 2016,
        "end_year": 2019
    },
    {
        "id": "epoch_4",
        "name": "2020–2022: Current Era (НЖТИ & ВЖЦХ)",
        "start_year": 2020,
        "end_year": 2022
    }
]


class NetworkEvolutionEngine:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn

    def build_epoch_graph(self, start_year: int, end_year: int) -> nx.Graph:
        """Constructs an undirected co-occurrence and number-bridge network for an epoch."""
        G = nx.Graph()
        
        query = """
            SELECT m.id, m.callsign, m.date, cb.code_word, cb.digit_combination
            FROM CodeBlocks cb
            JOIN Messages m ON cb.message_id = m.id
            WHERE m.is_duplicate = 0 AND m.year >= ? AND m.year <= ?
            ORDER BY m.id ASC
        """
        rows = self.conn.execute(query, (start_year, end_year)).fetchall()
        
        msg_blocks = collections.defaultdict(list)
        for r in rows:
            cw = r['code_word'].strip().upper() if r['code_word'] else None
            num = r['digit_combination'].strip() if r['digit_combination'] else None
            msg_blocks[r['id']].append((cw, num))

        for mid, blocks in msg_blocks.items():
            words_in_msg = [b[0] for b in blocks if b[0]]
            nums_in_msg = [b[1] for b in blocks if b[1]]

            for w in words_in_msg:
                if not G.has_node(w):
                    G.add_node(w, type='codeword', label=w)
            for n in nums_in_msg:
                if not G.has_node(n):
                    G.add_node(n, type='number', label=n)

            # Edges between word and its number
            for w, n in blocks:
                if w and n:
                    if G.has_edge(w, n):
                        G[w][n]['weight'] += 1
                    else:
                        G.add_edge(w, n, weight=1, relation='paired')

            # Edges between co-occurring words in same message
            if len(words_in_msg) > 1:
                for i in range(len(words_in_msg)):
                    for j in range(i + 1, len(words_in_msg)):
                        w1, w2 = words_in_msg[i], words_in_msg[j]
                        if G.has_edge(w1, w2):
                            G[w1][w2]['weight'] += 1
                        else:
                            G.add_edge(w1, w2, weight=1, relation='cooccurrence')

        return G

    def get_epoch_metrics(self) -> List[Dict[str, Any]]:
        """Computes topological network metrics for all 4 epochs."""
        results = []
        for ep in EPOCHS:
            G = self.build_epoch_graph(ep['start_year'], ep['end_year'])
            n_nodes = G.number_of_nodes()
            n_edges = G.number_of_edges()

            if n_nodes > 0:
                density = round(nx.density(G), 5)
                avg_degree = round(sum(dict(G.degree()).values()) / n_nodes, 2)
                transitivity = round(nx.transitivity(G), 4)  # clustering coefficient
                components = list(nx.connected_components(G))
                n_components = len(components)
                giant_size = len(max(components, key=len)) if components else 0
                giant_ratio = round(giant_size / n_nodes * 100, 1)

                # Top hubs (highest degree nodes)
                degree_dict = dict(G.degree())
                top_hubs = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:5]
                hubs_list = [{'node': h[0], 'degree': h[1], 'type': G.nodes[h[0]].get('type', 'unknown')} for h in top_hubs]
            else:
                density, avg_degree, transitivity, n_components, giant_size, giant_ratio = 0, 0, 0, 0, 0, 0
                hubs_list = []

            results.append({
                'epoch_id': ep['id'],
                'epoch_name': ep['name'],
                'years': f"{ep['start_year']}–{ep['end_year']}",
                'nodes': n_nodes,
                'edges': n_edges,
                'density': density,
                'avg_degree': avg_degree,
                'transitivity_clustering': transitivity,
                'connected_components': n_components,
                'giant_component_size': giant_size,
                'giant_component_pct': giant_ratio,
                'top_hubs': hubs_list
            })
        return results

    def get_epoch_subgraph_vis(self, epoch_id: str, limit_nodes: int = 60) -> Dict[str, Any]:
        """Returns JSON node/edge payload for Vis.js rendering of a specific epoch."""
        ep = next((e for e in EPOCHS if e['id'] == epoch_id), EPOCHS[1])
        G = self.build_epoch_graph(ep['start_year'], ep['end_year'])

        if G.number_of_nodes() == 0:
            return {'nodes': [], 'edges': []}

        # Filter to highest degree nodes if large
        if G.number_of_nodes() > limit_nodes:
            top_nodes = set(dict(sorted(G.degree(), key=lambda x: x[1], reverse=True)[:limit_nodes]).keys())
            G_sub = G.subgraph(top_nodes).copy()
        else:
            G_sub = G

        vis_nodes = []
        for n, data in G_sub.nodes(data=True):
            ntype = data.get('type', 'codeword')
            is_target = n in ['ЗИЗИФУС', 'ПАСКОИТ', 'ГАШЕНИЕ', 'НИЗКИЙ', '7724 8209', '77248209']
            
            if is_target:
                color = '#f59e0b'
                size = 28
            elif ntype == 'number':
                color = '#a855f7'
                size = 14
            else:
                color = '#38bdf8'
                size = 20

            vis_nodes.append({
                'id': n,
                'label': n,
                'color': color,
                'size': size,
                'shape': 'box' if ntype == 'codeword' else 'ellipse',
                'font': {'color': '#f8fafc', 'face': 'monospace', 'size': 11}
            })

        vis_edges = []
        for u, v, data in G_sub.edges(data=True):
            weight = data.get('weight', 1)
            rel = data.get('relation', 'paired')
            is_bridge = (u in ['7724 8209', '77248209'] or v in ['7724 8209', '77248209'])
            color = '#ef4444' if is_bridge else ('#334155' if rel == 'paired' else '#10b981')
            
            vis_edges.append({
                'from': u,
                'to': v,
                'value': weight,
                'color': color,
                'width': 3 if is_bridge else 1.2
            })

        return {
            'epoch_id': ep['id'],
            'epoch_name': ep['name'],
            'nodes': vis_nodes,
            'edges': vis_edges
        }
