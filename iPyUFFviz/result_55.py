import analyze_UFF as analiza
import show_analysis 
import numpy as np

def data55(drop, file, all_pt, dic55,trans_matrix,nodes):
    """data55
    
    Prepares outputs for vizualization data from datata sets 58
    
    Parameters
    ----------
    drop : string like 'normal mode'
        Possible analysis data stored in dataset 55
        possible choices:
        'normal mode'
        'complex eigenvalue first order (displacement)'
        'frequency response'
        'complex eigenvalue second order (velocity)'
    file : UFF class element
        UFF class element - file prepared for further usage
    all_pt: (nparray(x),nparray(y), nparray(z)) list of arrays
        list of nparray with x, array with y and an array with z coordintaes of all points
    dic55: {'2':....,'3':....,....} python dictonary
        dictonary with indices of dataset type 55 refer to used analyses type
        at pyuff supported:
        '2' - norma mode
        '3' - complex eigenvalue first order (displacement)
        '5' - frequency response
        '7' - complex eigenvalue second order (velocity)
    trans_matrix: ({'n': trans. matrix,....,'index': i},...) array like
        array of dictoraries with transformation matrix of local coordinate sistems in nodes and index of native dataset
    nodes: nodes: ({'n':[x[n],y[n],z[n]],....,'index': i},...) array like
        array of dictoraries with coordinates of nodes and index of native dataset

    Returns
    -------
    data: numpy array of shape (3, maximal lenth of data array from all 55 datasets,len(all_pt))
        matrix with function data from datasets 55 for all points in all three coordinates
    """

    in_names55 = {'normal mode':'2',
              'complex eigenvalue first order (displacement)':'3',
              'frequency response':'5',
              'complex eigenvalue second order (velocity)':'7'}
    drop = in_names55[drop.value]
    indices = dic55[drop]
    data = np.zeros((3,len(all_pt[0]),len(dic55[drop])))
    all_nodes = []
    for no in nodes:
        for n in list(no.keys()):
            if n == 'index':
                pass
            else:
                all_nodes.append(int(n))
    i=0            
    for index in indices:
        set55 = file.read_sets(index)
        for no in set55['node_nums']:
            n = all_nodes.index(no)
            def get_rotma():
                t = []
                for i in range(len(trans_matrix)):
                    t.append(trans_matrix[i][str(int(no))])
                if len(t)==1:
                    return t[0]
                else:
                    return None
            data[:,n,i]+=np.matmul(get_rotma(),np.array([set55['r1'][n],set55['r2'][n],set55['r3'][n]]))
        i+=1
    return np.transpose(data,axes=[0,2,1])