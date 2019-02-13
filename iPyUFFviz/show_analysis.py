import numpy as np

def basic_info(model):
    for i in range(len(model)):
        model_i = model[i]
        print(model_i['name'])
        print(model_i['description'])
    if len(model)>1:
        print('You have probably more than one model in file, so you can expect problems')

def data_info(nodes, dic55, dic58):
    X = []
    Y = []
    Z = []
    for i in range(len(nodes)):
        nodes_i = nodes[i]
        n_s = list(nodes_i.keys())
        for n in n_s[:-1]:
            X.append(nodes_i[n][0])
            Y.append(nodes_i[n][1])
            Z.append(nodes_i[n][2])
    X = np.asarray(X)
    Y = np.asarray(Y)
    Z = np.asarray(Z)
    all_pt=(X,Y,Z)
    print('file has data for ' + len(X) + ' points')

    pt58 = {}
    for key in dic58.keys():
        indices = dic58[key]
        x = []
        y = []
        z = []
        for i in indices:
            node = str(file.read_sets(i)['ref_node'])
            for j in range(len(nodes)):
                x.append(nodes[j][node][0])
                y.append(nodes[j][node][1])
                z.append(nodes[j][node][2])
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        pt58[key] = (x, y, z)
        print('Function type ',key, 'data are in ',len(x),' points')

    pt55 = {}
    for key in dic55.keys():
        indices = dic55[key]
        x = []
        y = []
        z = []
        for i in indices:
            node_nums = file.read_sets(i)['node_nums']
            for no in node_nums:
                node = str(no)
                for j in range(len(nodes)):
                    x.append(nodes[j][node][0])
                    y.append(nodes[j][node][1])
                    z.append(nodes[j][node][2])
        x = np.asarray(x)
        y = np.asarray(y)
        z = np.asarray(z)
        pt55[key] = (x, y, z)
        print('Analysis type ',key,' data are in ',len(x),'points')

    return all_pt,pt58,pt55
