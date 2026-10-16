"""
Graph Intelligence & Network Analysis Engine for UVB-76.
Builds and analyzes the multi-relational graph:
- Nodes: Codeword, NumberGroup (8-digit), Radiogram, Callsign
- Edges: Word-to-Digits, Co-occurrence in Radiogram, Radiogram-Callsign, Number-Repetition
- Graph metrics: Centrality (degree, betweenness), Connected Components, Bridge detection
- Subgraph extraction around key targets (ЗИЗИФУС, ПАСКОИТ, ГАШЕНИЕ, НИЗКИЙ)
- JSON export formatted for Vis.js interactive frontend visualization and GraphML export.
"""

import sqlite3
import collections
from typing import Dict, Any, List, Optional
import networkx as nx

class GraphIntelligenceEngine:
    def __init__(self, db_conn: sqlite3.Connection):
        self.conn = db_conn
        self.G: Optional[nx.Graph] = None

    def build_full_network(self, year_filter: Optional[int] = None, 
                           callsign_filter: Optional[str] = None,
                           include_radiograms: bool = True) -> nx.Graph:
        """Constructs the NetworkX multi-entity graph from the database."""
        G = nx.Graph()
        
        # Build query filters
        filters = ["m.is_duplicate = 0"]
        params = []
        if year_filter:
            filters.append("m.year = ?")
            params.append(year_filter)
        if callsign_filter:
            filters.append("m.callsign LIKE ?")
            params.append(f"%{callsign_filter}%")
            
        where_clause = "WHERE " + " AND ".join(filters)
        
        # Fetch messages and blocks
        q = f"""
            SELECT m.id as msg_id, m.date, m.time_as_logged, m.callsign, m.header_number,
                   m.full_word_sequence, cb.block_index, cb.code_word, cb.digit_combination,
                   cb.digit_group_1, cb.digit_group_2
            FROM Messages m
            JOIN CodeBlocks cb ON m.id = cb.message_id
            {where_clause}
            ORDER BY m.date ASC, m.time_as_logged ASC
        """
        rows = self.conn.execute(q, params).fetchall()
        
        # Group by message to detect co-occurrences
        msg_blocks = collections.defaultdict(list)
        for r in rows:
            msg_blocks[r['msg_id']].append(r)
            
        for msg_id, blocks in msg_blocks.items():
            first = blocks[0]
            rg_id = f"MSG_{msg_id}"
            
            # Radiogram node
            if include_radiograms:
                G.add_node(rg_id, node_type='RADIOGRAM', 
                           label=f"RG {first['date']} {first['time_as_logged']}",
                           date=first['date'], time=first['time_as_logged'],
                           header=first['header_number'],
                           title=f"Радиограмма {first['date']} {first['time_as_logged']}\n{first['full_word_sequence']}")
                
                # Callsign node & edge
                if first['callsign']:
                    cs_name = first['callsign'].split('/')[0].strip()
                    cs_id = f"CS_{cs_name}"
                    if not G.has_node(cs_id):
                        G.add_node(cs_id, node_type='CALLSIGN', label=cs_name, title=f"Позывной: {first['callsign']}")
                    G.add_edge(rg_id, cs_id, edge_type='TRANSMITTED_UNDER', weight=1)
            
            # Codewords & Digits
            words_in_msg = []
            for b in blocks:
                w = b['code_word']
                d = b['digit_combination']
                w_id = f"WORD_{w}"
                d_id = f"NUM_{d}"
                
                # Add Word node
                if not G.has_node(w_id):
                    G.add_node(w_id, node_type='CODE_WORD', label=w, word=w,
                               title=f"Кодовое слово: {w}")
                words_in_msg.append(w_id)
                
                # Add Digits node
                if not G.has_node(d_id):
                    formatted_d = f"{b['digit_group_1']} {b['digit_group_2']}"
                    G.add_node(d_id, node_type='NUMBER_GROUP', label=formatted_d, digits=d,
                               title=f"Цифровая комбинация: {formatted_d}")
                    
                # Edge: Word <-> Digits
                if not G.has_edge(w_id, d_id):
                    G.add_edge(w_id, d_id, edge_type='WORD_TO_DIGITS', weight=1, dates=[b['date']])
                else:
                    G[w_id][d_id]['weight'] += 1
                    if 'dates' in G[w_id][d_id]:
                        G[w_id][d_id]['dates'].append(b['date'])
                        
                # Edge: Radiogram <-> Word
                if include_radiograms:
                    G.add_edge(rg_id, w_id, edge_type='CONTAINS_WORD', weight=1)
                    
            # Edges: Co-occurrence between words in the same radiogram
            for i in range(len(words_in_msg)):
                for j in range(i + 1, len(words_in_msg)):
                    w1, w2 = words_in_msg[i], words_in_msg[j]
                    if w1 != w2:
                        if not G.has_edge(w1, w2):
                            G.add_edge(w1, w2, edge_type='CO_OCCURRENCE', weight=1,
                                       radiograms=[rg_id], dates=[first['date']])
                        else:
                            G[w1][w2]['weight'] += 1
                            if 'radiograms' in G[w1][w2]:
                                G[w1][w2]['radiograms'].append(rg_id)
                                G[w1][w2]['dates'].append(first['date'])
                                
        self.G = G
        return G

    def get_network_metrics(self) -> Dict[str, Any]:
        """Calculates global and node-level graph metrics."""
        if self.G is None:
            self.build_full_network()
        G = self.G
        
        num_nodes = G.number_of_nodes()
        num_edges = G.number_of_edges()
        density = round(float(nx.density(G)), 6) if num_nodes > 0 else 0
        
        # Connected components
        components = list(nx.connected_components(G))
        comp_count = len(components)
        largest_comp_size = max(len(c) for c in components) if components else 0
        
        # Centrality
        degree_cent = nx.degree_centrality(G)
        top_degree = sorted(degree_cent.items(), key=lambda x: x[1], reverse=True)[:15]
        
        # Betweenness centrality (on a representative sample if huge)
        between_cent = nx.betweenness_centrality(G, k=min(100, num_nodes))
        top_betweenness = sorted(between_cent.items(), key=lambda x: x[1], reverse=True)[:15]
        
        def format_cent(items):
            res = []
            for node_id, score in items:
                data = G.nodes[node_id]
                res.append({
                    'node_id': node_id,
                    'label': data.get('label', node_id),
                    'node_type': data.get('node_type', 'UNKNOWN'),
                    'score': round(float(score), 4)
                })
            return res
            
        return {
            'total_nodes': num_nodes,
            'total_edges': num_edges,
            'density': density,
            'connected_components_count': comp_count,
            'largest_component_size': largest_comp_size,
            'top_degree_centrality': format_cent(top_degree),
            'top_betweenness_centrality': format_cent(top_betweenness)
        }

    def get_target_subgraph(self, target_words: List[str] = ['ЗИЗИФУС', 'ПАСКОИТ', 'ГАШЕНИЕ', 'НИЗКИЙ'],
                            depth: int = 1) -> Dict[str, Any]:
        """
        Extracts egocentric subgraph around the target keywords,
        highlighting bridge combinations (like 77248209).
        """
        if self.G is None:
            self.build_full_network(include_radiograms=False)
        G = self.G
        
        target_nodes = set()
        for w in target_words:
            node_id = f"WORD_{w.upper()}"
            if G.has_node(node_id):
                target_nodes.add(node_id)
                
        subgraph_nodes = set(target_nodes)
        for _ in range(depth):
            neighbors = set()
            for n in subgraph_nodes:
                if G.has_node(n):
                    neighbors.update(G.neighbors(n))
            subgraph_nodes.update(neighbors)
            
        subG = G.subgraph(subgraph_nodes)
        
        # Format for Vis.js network visualization
        vis_nodes = []
        for n, data in subG.nodes(data=True):
            ntype = data.get('node_type', 'UNKNOWN')
            color = '#38bdf8' # cyan for word
            shape = 'dot'
            size = 18
            if ntype == 'CODE_WORD':
                color = '#f59e0b' if any(t in n for t in target_words) else '#06b6d4'
                size = 22 if any(t in n for t in target_words) else 16
            elif ntype == 'NUMBER_GROUP':
                color = '#ef4444' if '77248209' in n else '#8b5cf6'
                size = 20 if '77248209' in n else 14
                shape = 'diamond'
            elif ntype == 'CALLSIGN':
                color = '#10b981'
                shape = 'triangle'
                size = 18
            elif ntype == 'RADIOGRAM':
                color = '#64748b'
                size = 10
                
            vis_nodes.append({
                'id': n,
                'label': data.get('label', n),
                'group': ntype,
                'title': data.get('title', n),
                'color': color,
                'shape': shape,
                'size': size,
                'font': {
                    'size': 11,
                    'color': '#f8fafc',
                    'face': 'JetBrains Mono, monospace',
                    'strokeWidth': 2,
                    'strokeColor': '#070b12'
                }
            })
            
        vis_edges = []
        for u, v, data in subG.edges(data=True):
            etype = data.get('edge_type', 'NORMAL')
            color = '#64748b'
            dashes = False
            title_desc = f"Связь: {etype}"
            if etype == 'WORD_TO_DIGITS':
                is_bridge = ('77248209' in u or '77248209' in v)
                color = '#ef4444' if is_bridge else '#3b82f6'
                title_desc = "Связь: Кодовое слово ↔ Числовая группа (WORD_TO_DIGITS)"
                if is_bridge:
                    title_desc = "КРИТИЧЕСКИЙ МОСТ: 7724 8209 (ЗИЗИФУС ↔ ПАСКОИТ)"
            elif etype == 'CO_OCCURRENCE':
                color = '#10b981'
                dashes = True
                title_desc = "Связь: Совместная передача в сообщении (CO_OCCURRENCE)"
                
            vis_edges.append({
                'from': u,
                'to': v,
                'relation': etype,
                'title': title_desc,
                'color': color,
                'dashes': dashes,
                'weight': data.get('weight', 1)
            })
            
        return {
            'nodes': vis_nodes,
            'edges': vis_edges,
            'node_count': len(vis_nodes),
            'edge_count': len(vis_edges)
        }

    def search_node(self, query: str) -> Dict[str, Any]:
        """Searches for a word or digits and returns its local neighborhood."""
        if self.G is None:
            self.build_full_network(include_radiograms=False)
        G = self.G
        
        q_upper = query.strip().upper()
        matched_nodes = []
        for n, data in G.nodes(data=True):
            label = data.get('label', '').upper()
            if q_upper in label or q_upper in n:
                matched_nodes.append(n)
                
        if not matched_nodes:
            return {'found': False, 'query': query, 'nodes': [], 'edges': []}
            
        # Build 1-hop neighborhood for matched nodes
        sub_nodes = set(matched_nodes)
        for mn in matched_nodes[:5]:
            sub_nodes.update(G.neighbors(mn))
            
        subG = G.subgraph(sub_nodes)
        
        vis_nodes = []
        for n, data in subG.nodes(data=True):
            ntype = data.get('node_type', 'UNKNOWN')
            color = '#38bdf8'
            shape = 'dot'
            size = 16
            if ntype == 'CODE_WORD':
                color = '#f59e0b' if any(t in n for t in ['ЗИЗИФУС', 'ПАСКОИТ', 'ГАШЕНИЕ', 'НИЗКИЙ']) else '#06b6d4'
                size = 22 if any(t in n for t in ['ЗИЗИФУС', 'ПАСКОИТ', 'ГАШЕНИЕ', 'НИЗКИЙ']) else 16
            elif ntype == 'NUMBER_GROUP':
                color = '#ef4444' if '77248209' in n else '#8b5cf6'
                size = 20 if '77248209' in n else 14
                shape = 'diamond'
            elif ntype == 'CALLSIGN':
                color = '#10b981'
                shape = 'triangle'
                size = 18

            vis_nodes.append({
                'id': n,
                'label': data.get('label', n),
                'group': ntype,
                'title': data.get('title', n),
                'color': color,
                'shape': shape,
                'size': size,
                'font': {
                    'size': 11,
                    'color': '#f8fafc',
                    'face': 'JetBrains Mono, monospace',
                    'strokeWidth': 2,
                    'strokeColor': '#070b12'
                }
            })
            
        vis_edges = []
        for u, v, data in subG.edges(data=True):
            etype = data.get('edge_type', 'NORMAL')
            color = '#64748b'
            dashes = False
            title_desc = f"Связь: {etype}"
            if etype == 'WORD_TO_DIGITS':
                is_bridge = ('77248209' in u or '77248209' in v)
                color = '#ef4444' if is_bridge else '#3b82f6'
                title_desc = "Связь: Кодовое слово ↔ Числовая группа (WORD_TO_DIGITS)"
                if is_bridge:
                    title_desc = "КРИТИЧЕСКИЙ МОСТ: 7724 8209"
            elif etype == 'CO_OCCURRENCE':
                color = '#10b981'
                dashes = True
                title_desc = "Связь: Совместная передача (CO_OCCURRENCE)"

            vis_edges.append({
                'from': u,
                'to': v,
                'relation': etype,
                'title': title_desc,
                'color': color,
                'dashes': dashes,
                'weight': data.get('weight', 1)
            })
            
        return {
            'found': True,
            'query': query,
            'matched_count': len(matched_nodes),
            'nodes': vis_nodes,
            'edges': vis_edges
        }
