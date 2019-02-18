import pyuff
import numpy as np

def anlyze_UFF(path):
    """anlyze_UFF

    function reads UFF, and prepare returns. Return are prepered for further procesing. 

    Parameters
    ----------
    path : string
        paht of chosen UFF file you want to analyze

    Returns
    -------
    file: UFF class element
        UFF class element - file prepared for further usage
    uffdic: {'151':...,'15':...,...} python dictonary
        dictonary with indices of included uff datasets (file.get_sets())
    model: ({'name':..., 'descript':...,'index': i},...) array like
        array of dictonaries with name, description of model and index of native dataset
    nodes: ({'n':[x[n],y[n],z[n]],....,'index': i},...) array like
        array of dictoraries with coordinates of nodes and index of native dataset
    lines: ({'trace':number,'nodes':np.array(.....),'index': i},...) array like
        array of dictonaries with trance lines and theri nodes
    trans_matrix: ({'n': trans. matrix,....,'index': i},...) array like
        array of dictoraries with transformation matrix of local coordinate sistems in nodes and index of native dataset
    dic55: {'2':....,'3':....,....} python dictonary
        dictonary with indices of dataset type 55 refer to used analyses type
        at pyuff supported:
        '2' - norma mode
        '3' - complex eigenvalue first order (displacement)
        '5' - frequency response
        '7' - complex eigenvalue second order (velocity)
    dic58: {'1':....,'2':....,....} python dictonary
        dictonary with indices of dataset type 58 refer to used function type
        at pyuff supported:
        '0' - General or Unknown
        '1' - Time Response
        '2' - Auto Spectrum
        '3' - Cross Spectrum
        '4' - Frequency Response Function
        '6' - Coherence
    """
    
    file = pyuff.UFF(path)
    sets = file.get_set_types()
    sup_sets = file.get_supported_sets()

    uffdic = {}
    for a in sup_sets:
        index = []
        for i in range(len(sets)):
            if str(int(sets[i])) == a:
                index.append(i)
        uffdic[a] = index

    keys_58 = ['0', '1', '2', '3', '4', '6']
    keys_55 = ['2', '3', '5', '7']
    dic58 = {}
    dic55 = {}
    lines = []
    model = []
    nodes = []
    trans_matrix = []

    for key in keys_55:
        index = []
        for i in uffdic['55']:
            f_typ = file.read_sets(i)['analysis_type']
            if str(f_typ) == key:
                index.append(i)
        dic55[key] = index

    for key in keys_58:
        index = []
        for i in uffdic['58']:
            f_typ = file.read_sets(i)['func_type']
            if str(f_typ) == key:
                index.append(i)
        dic58[key] = index

    for i in uffdic['151']:
        model.append({'name': file.read_sets(i)['model_name'], 'description': file.read_sets(i)['description'],'index': i})

    for i in uffdic['15']:
        dic = {}
        no = file.read_sets(i)['node_nums']
        x = file.read_sets(i)['x']
        y = file.read_sets(i)['y']
        z = file.read_sets(i)['z']
        for n in range(len(no)):
            dic[str(int(no[n]))] = [x[n],y[n],z[n]]
        dic['index'] = i
        nodes.append(dic)

    for i in uffdic['82']:
        dic = {}
        dic['trace'] = file.read_sets(i)['trace_num']
        dic['nodes'] = file.read_sets(i)['nodes']
        dic['index'] = i
        lines.append(dic)

    for i in uffdic['2420']:
        dic = {}
        no = file.read_sets(i)['CS_sys_labels']
        tm = file.read_sets(i)['CS_matrices']
        for n in range(len(no)):
            dic[str(int(no[n]))] = tm[n]
        dic['index'] = i
        trans_matrix.append(dic)

    def cleanup(dic):
        
        re_keys = []
        for key in dic.keys():
            if dic[key] == []:
                re_keys.append(key)
        for key in re_keys:
            del dic[key]
        return dic

    uffdic=cleanup(uffdic)
    dic55=cleanup(dic55)
    dic58=cleanup(dic58)

    return file,uffdic,model,nodes,lines,trans_matrix,dic55,dic58
    