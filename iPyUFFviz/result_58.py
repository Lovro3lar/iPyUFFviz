import analyze_UFF as analiza
import show_analysis 
import numpy as np

def data58(drop, file, all_pt, dic58,places58):
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
            return np.array([[1., 0., 0.],
                [0., 1., 0.],
                [0., 0., 1.]])

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
    return np.transpose(data,axes=[0,2,1])[0],np.transpose(data,axes=[0,2,1])[1],np.transpose(data,axes=[0,2,1])[2]