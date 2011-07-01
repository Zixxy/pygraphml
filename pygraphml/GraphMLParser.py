#-*- coding: utf-8 -*-

from xml.dom import minidom

from Graph import *
from Node import *
from Edge import *

class GraphMLParser:
    """
    """

    def __init__(self):
        """
        """

    def write(self, graph, fname):
        """
        """

        doc = minidom.Document()

        root = doc.createElement('graphml')
        doc.appendChild(root)
        
        graph_node = doc.createElement('graph')
        graph_node.setAttribute('id', graph.name)
        if graph.directed:
            graph_node.setAttribute('edgedefault', 'directed')
        else:
            graph_node.setAttribute('edgedefault', 'undirected')
        root.appendChild(graph_node)

        attr = []
        
        # Add nodes
        for n in graph.nodes():

            node = doc.createElement('node')
            node.setAttribute('id', n['label'])
            for a in n.attributes():
                if a != 'label':

                    if a not in attr:
                        attr_node = doc.createElement('key')
                        attr_node.setAttribute('id', a)
                        attr_node.setAttribute('attr.name', a)
                        attr_node.setAttribute('attr.type', 'string')
                        root.appendChild(attr_node)
                    
                    data = doc.createElement('data')
                    data.setAttribute('key', a)
                    data.appendChild(doc.createTextNode(str(n[a])))
                    node.appendChild(data)
            graph_node.appendChild(node)

        for e in graph.edges():

            edge = doc.createElement('edge')
            edge.setAttribute('source', e.node1['label'])
            edge.setAttribute('target', e.node2['label'])
            for a in e.attributes():
                if e != 'label':

                    if a not in attr:
                        attr_node = doc.createElement('key')
                        attr_node.setAttribute('id', a)
                        attr_node.setAttribute('attr.name', a)
                        attr_node.setAttribute('attr.type', 'string')
                        root.appendChild(attr_node)
                    
                    data = doc.createElement('data')
                    data.setAttribute('key', a)
                    data.appendChild(doc.createTextNode(e[a]))
                    node.appendChild(data)
            graph_node.appendChild(edge)

        f = open(fname, 'w')
        f.write(doc.toprettyxml(indent = '    '))
    
    def parse(self, fname):
        """
        """

        dom = minidom.parse(open(fname, 'r'))

        root = dom.getElementsByTagName("graphml")[0]
        graph = root.getElementsByTagName("graph")[0]
        name = graph.getAttribute('id')

        g = Graph(name)

        # # Get attributes
        # attributes = []
        # for attr in root.getElementsByTagName("key"):
        #     attributes.append(attr)

        # Get nodes
        for node in graph.getElementsByTagName("node"):
            n = g.add_node(node.getAttribute('id'))

            for attr in node.getElementsByTagName("data"):
                if attr.firstChild:
                    n[attr.getAttribute("key")] = attr.firstChild.data
                else:
                    n[attr.getAttribute("key")] = ""

        # Get edges
        for edge in graph.getElementsByTagName("edge"):
            source = edge.getAttribute('source')
            dest = edge.getAttribute('target')
            e = g.add_edge_by_label(source, dest)

            for attr in edge.getElementsByTagName("data"):
                if attr.firstChild:
                    e[attr.getAttribute("key")] = attr.firstChild.data
                else:
                    e[attr.getAttribute("key")] = ""

        return g


if __name__ == '__main__':

    parser = GraphMLParser()
    g = parser.parse('test.graphml')

    g.show(True)
    
        
