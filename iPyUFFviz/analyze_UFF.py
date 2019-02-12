import pyuff
import numpy as np

def anlyze_UFF(path):

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

    keys_58 = [1, 2, 3, 4, 6]
    keys_55 = [2, 3, 5, 7]
    dic58 = {}
    dic55 = {}
    model = []
    nodes = []
    trans_matrix = []

    for key in keys_55:
        index = []
        for i in uffdic['55']:
            f_typ = file.read_sets(i)['analysis_type']
            if f_typ == key:
                index.append(i)
        dic55[key] = index

    for key in keys_58:
        index = []
        for i in uffdic['58']:
            f_typ = file.read_sets(i)['func_type']
            if f_typ == key:
                index.append(i)
        dic58[key] = index

    for i in uffdic['151']:
        model.append({'name': file.read_sets(i)['model_name'], 'descript': file.read_sets(i)['description'],'index': i})

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

    return file,uffdic,model,nodes,trans_matrix,dic55,dic58




path="C:\\Users\\Lovro\\Documents\\5.Letnik\\Magistrska\\Podatki in meritve\\meritve_Nosilec.uff"

a = anlyze_UFF(path)
print(a)
