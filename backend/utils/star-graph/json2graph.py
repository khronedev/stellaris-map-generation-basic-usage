from graphviz import Graph
import json


def generate_all_stars(dot, data):
    clusters = {}

    for i, name in enumerate(data['stars']):
        star = data['stars'][name]

        pos = '{},{}!'.format(star['cords']['x'], star['cords']['y'])
        empire = None
        color = '#{:06X}'.format(i)

        def put_node(graph):
            graph.node(name, pos=pos, shape='none', clustercolor=color)

        if i not in clusters:
            clusters[i] = Graph(name='cluster{}'.format(i), graph_attr={'id': name})

        put_node(clusters[i])

    for name in clusters:
        cluster = clusters[name]
        dot.subgraph(graph=cluster)


def generate_sectors(dot, data):
    clusters = {}

    for i, name in enumerate(data['stars']):
        star = data['stars'][name]

        pos = '{},{}!'.format(star['cords']['x'], star['cords']['y'])
        empire = None

        if len(star['influencedBy']) > 0:
            influence_id = star['influencedBy'][0]['controlledBy']
            empire = data['empires'][influence_id]

        def put_node(graph, color):
            graph.node(name, pos=pos, shape='none', clustercolor=color)

        if empire:
            sector_id = None
            for sectorId in empire['sectors']:
                sector = empire['sectors'][sectorId]
                for star in sector['stars']:
                    if star == name:
                        sector_id = sector['id']

            if sector_id is None:
                print empire

            if sector_id not in clusters:
                clusters[sector_id] = Graph(name='cluster{}'.format(sector_id), graph_attr={'id': sector_id})

            put_node(clusters[sector_id], color='{}'.format(sector_id))

    for name in clusters:
        cluster = clusters[name]
        dot.subgraph(graph=cluster)


def generate_empires(dot, data):
    clusters = {}

    for i, name in enumerate(data['stars']):
        star = data['stars'][name]

        pos = '{},{}!'.format(star['cords']['x'], star['cords']['y'])
        empire = None
        color = '#{:06X}'.format(i)

        if len(star['influencedBy']) > 0:
            influence_id = star['influencedBy'][0]['controlledBy']
            empire = data['empires'][influence_id]
            color = empire['id']

        def put_node(graph):
            graph.node(name, pos=pos, shape='none', clustercolor=color)

        if empire:
            if empire['id'] not in clusters:
                clusters[empire['id']] = Graph(name='cluster{}'.format(empire['id']), graph_attr={'id': empire['id'], 'name': empire['name']})

            put_node(clusters[empire['id']])

    for name in clusters:
        cluster = clusters[name]
        dot.subgraph(graph=cluster)


def generate_dependencies(dot, data):
    clusters = {}

    for i, name in enumerate(data['stars']):
        star = data['stars'][name]

        pos = '{},{}!'.format(star['cords']['x'], star['cords']['y'])
        empire = None

        if len(star['influencedBy']) > 0:
            influence_id = star['influencedBy'][0]['controlledBy']
            empire = data['empires'][influence_id]

        def put_node(graph, cluster_id):
            graph.node(name, pos=pos, shape='none', clustercolor=cluster_id)

        if empire:
            cluster_id = empire['political_status']['independency']

            if cluster_id not in clusters:
                clusters[cluster_id] = Graph(name='cluster{}'.format(cluster_id), graph_attr={'id': cluster_id})

            put_node(clusters[cluster_id], cluster_id)

    for name in clusters:
        cluster = clusters[name]
        dot.subgraph(graph=cluster)


def generate_hyperlanes_graph(dot, data):
    for i, name in enumerate(data['stars']):
        star = data['stars'][name]

        dot.node(star['id'], shape='none')

        for id in star['hyperlanes']:
            hyperlane = star['hyperlanes'][id]
            dot.edge(star['id'], hyperlane['to'])


def execute():
    stars_file = open('../../samples/end-game/basics.json')
    data = json.loads(stars_file.read())
    stars_file.close()

    dot = Graph(strict='true')
    generate_all_stars(dot, data)
    dot.render('./tests/all-stars.dot')

    dot = Graph(strict='true')
    generate_sectors(dot, data)
    dot.render('./tests/sectors.dot')

    dot = Graph(strict='true')
    generate_empires(dot, data)
    dot.render('./tests/empires.dot')

    dot = Graph(strict='true')
    generate_dependencies(dot, data)
    dot.render('./tests/independencies.dot')

    dot = Graph(strict='true')
    generate_hyperlanes_graph(dot, data)
    dot.render('./tests/hyperlanes.dot')

execute()