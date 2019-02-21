import analyze_UFF as analiza
import show_analysis 
import numpy as np

def data58(drop, file, all_pt, dic58,places58,trans_matrix):
    """data58
    
    [summary]
    
    Parameters
    ----------
    drop : string like 'Frequency Response Function'
        Posible function data stored in dataset 58
        possible choices:
        'General or Unknown',
        'Time Response',
        'Auto Spectrum'',
        'Cross Spectrum',
        'Frequency Response Function',
        'complex eigenvalue second order (velocity)'
    file : UFF class element
        UFF class element - file prepared for further usage
    all_pt: (nparray(x),nparray(y), nparray(z)) list of arrays
        list of nparray with x, array with y and an array with z coordintaes of all points
    dic58: {'1':....,'2':....,....} python dictonary
        dictonary with indices of dataset type 58 refer to used function type
        at pyuff supported:
        '0' - General or Unknown
        '1' - Time Response
        '2' - Auto Spectrum
        '3' - Cross Spectrum
        '4' - Frequency Response Function
        '6' - Coherence
    places58: {0: [....], 1: [....],....} dictonary
        dictonary with informaion about whichd dataset 58 has infomaton about point in points array all_pt
    trans_matrix: ({'n': trans. matrix,....,'index': i},...) array like
        array of dictoraries with transformation matrix of local coordinate sistems in nodes and index of native dataset
    
    Returns
    -------
    data: numpy array of shape (3, maximal lenth of data array from all 58 datasets,len(all_pt))
        matrix with function data from datasets 58 for all points in all three coordinates
    time: boolean
        is true if drop is 'Time Response' or 'General or Unknown'
    """

    in_names58 ={'General or Unknown':'0',
              'Time Response':'1',
              'Auto Spectrum':'2',
              'Cross Spectrum':'3',
              'Frequency Response Function':'4',
              'complex eigenvalue second order (velocity)':'6'}
    drop = in_names58[drop]
    if drop == '0' or '1':
        time = True
    data = np.zeros((3,len(all_pt[0]),1))
    indices = dic58[drop]
    for index in indices:
        set58 = file.read_sets(index)
        data_i=np.zeros((3,len(all_pt[0]),set58['data'].size))

        place = []
        for key in places58.keys():
            A = set(places58[key])
            B = set([index])
            if B.issubset(A):
                place.append(key)
        def get_rotma():
            t = []
            for i in range(len(trans_matrix)):
                t.append(trans_matrix[i][set58['ref_node']])
            if len(t)==1:
                return t[0]
            else:
                return None

        def get_data():
            direc = set58['rsp_dir']
            if np.abs(direc)<4:
                data_a = np.zeros([3,len(set58['data'])])
                data_a[abs(direc)-1] = np.sign(direc)*set58['data']
            else:
                direc = direc-3
                data_a = np.zeros([3,len(set58['data'])])
                data_a[abs(direc)-1] = np.sign(direc)*set58['data']
            return np.matmul(get_rotma(),data_a)


        if len(place)>1:
            print(len(place))
        if len(place)==0:
            print('Meritev nima točke s koordinatami - warning')
        if len(place)==1:
            place = place[0]
            data_i[:,place,:] = get_data()

        if data_i[0,0].size > data[0,0].size:
            data_i[:,:,:data.shape[2]] += data
            data = data_i
        else:
            data[:,:,:data_i.shape[2]] += data_i
    #return np.transpose(data,axes=[0,2,1])[0],np.transpose(data,axes=[0,2,1])[1],np.transpose(data,axes=[0,2,1])[2]
    return np.transpose(data,axes=[0,2,1]),time