import numpy as np
import ipywidgets as widgets
import ipyvolume as ipv

def basic_info(model):
    """basic_info
    
    prints basic info abaout models saved in antiv UFF
    
    Parameters
    ----------
    model : ({'name':..., 'descript':...,'index': i},...) list 
        list of dictonaries with name, description of model and index of native dataset
    Returns
    -------
    info: array 
        array of read model name and description. If native file has more then one dataset 151,
        first elemet is wearning about multiple model in nativ uff. 
    """

    info=[]
    if len(model)>1:
        info.append('You have probably infomation about more then %i models in file, so you can expect problems') % (len(model))
    for i in range(len(model)):
        model_i = model[i]
        info.append(model_i['name'])
        info.append(model_i['description'])
    return info
    

def data_info(file, nodes, lines, dic55, dic58):
    """data_info
    
    Prints how many point are in nativ UFF, and what kind of analysis result or mesurment data are stored.
    Prepares arrays of x,y and z coordintas for points and points with data

    Parameters
    ----------
    file : UFF class element
        UFF class element - file prepared for further usage
    nodes : ({'n':[x[n],y[n],z[n]],....,'index': i},...) list like
        list of dictoraries with coordinates of nodes and index of native dataset
    lines: ({'trace':number,'nodes':np.array(.....),'index': i},...) array like
        array of dictonaries with trance lines and theri nodes
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
    
    Returns
    -------
    all_pt: (nparray(x),nparray(y), nparray(z)) list of arrays
        list of nparray with x, array with y and an array with z coordintaes of all apint
    pt58: {'1':(nparray(x),nparray(y), nparray(z)),....} dictonary
        dictonary with arrays with x, y and z coordinte of reference node of dataset type 58 refer to used function type
        at pyuff supported:
        '0' - General or Unknown
        '1' - Time Response
        '2' - Auto Spectrum
        '3' - Cross Spectrum
        '4' - Frequency Response Function
        '6' - Coherence
    pt55: {'2':(nparray(x),nparray(y), nparray(z)),....} dictonary
        dictonary with arrays with x, y and z coordinte of reference node of dataset type 55 refer to used analyses type
        at pyuff supported:
        '2' - norma mode
        '3' - complex eigenvalue first order (displacement)
        '5' - frequency response
        '7' - complex eigenvalue second order (velocity)
    lines: ({'trace':number,'nodes':np.array(.....),'index': i,'x_l':....,'y_l':....,'z_l':......},...) array like
        array of dictonaries with trance lines, theri nodes and coordinates
    info_data: array of strins
        array of strins with informations obout data at points in native uff 
    """

    X = []
    Y = []
    Z = []
    info = []
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
    info.append(('file has data for %s points') % (len(X)))
    

    for i in range(len(lines)):
        l_nodes = lines[i]['nodes']
        x = []
        y = []
        z = []
        for n in l_nodes:
            no = str(int(n))
            for j in range(len(nodes)):
                x.append(nodes[j][no][0])
                y.append(nodes[j][no][1])
                z.append(nodes[j][no][2])
        lines[i]['x_l'] = np.array([x,x])
        lines[i]['y_l'] = np.array([y,y])
        lines[i]['z_l'] = np.array([z,z])


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
        info.append(('Function type %s data are in %s points') % (key,len(x)))

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
        info.append(('Analysis type%s data are in %s points') % (key,len(x)))

    return all_pt,pt58,pt55,lines,info

def print_info(info_model,info_data):
    for i in info_model:
        print(i)
    for i in info_data:
        print(i)

def basic_show_NB(file,model,nodes, lines, dic55, dic58):
    """basic_show_NB
    
    Function prepair output with basic information obout data in uff file and draw out points and trce lines in 3D.
    Points are highlighted baised on chosen options in buttons and dropdown menu
    
    Parameters
    ----------
    file: UFF class element
        UFF class element - file prepared for further usage
    model: ({'name':..., 'descript':...,'index': i},...) array like
        array of dictonaries with name, description of model and index of native dataset
    nodes: ({'n':[x[n],y[n],z[n]],....,'index': i},...) array like
        array of dictoraries with coordinates of nodes and index of native dataset
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
    
    Returns
    -------
    buttons: ipywidgets
        ipywidgets radio buttons
    drop: ipywidgets
        ipywidgets dropdown meni of options referd to choice in radio buttons
    """



    info = basic_info(model)
    all_pt,pt58,pt55,traces,info_data = data_info(file, nodes, lines, dic55, dic58)    
    for inf in info_data:
        info.append(inf)
    
    names55 ={'2': 'norma mode',
              '3': 'complex eigenvalue first order (displacement)',
              '5': 'frequency response',
              '7': 'complex eigenvalue second order (velocity)'}
    names58 ={'0': 'General or Unknown',
              '1': 'Time Response',
              '2': 'Auto Spectrum',
              '3': 'Cross Spectrum',
              '4': 'Frequency Response Function',
              '6': 'complex eigenvalue second order (velocity)'}
    in_names55 = {'norma mode':'2',
              'complex eigenvalue first order (displacement)':'3',
              'frequency response':'5',
              'complex eigenvalue second order (velocity)':'7'}
    in_names58 ={'General or Unknown':'0',
              'Time Response':'1',
              'Auto Spectrum':'2',
              'Cross Spectrum':'3',
              'Frequency Response Function':'4',
              'complex eigenvalue second order (velocity)':'6'}
    buttons = widgets.RadioButtons(options=['Function data', 'Analysis'],description='Results type:')
    drop = widgets.Dropdown(options=[names58[key] for key in dic58.keys()])
    
    def drop_data(*args):
        if buttons.value == 'Analysis':
            drop.options = [names55[key] for key in dic55.keys()]
        if buttons.value=='Function data':
            drop.options = [names58[key] for key in dic58.keys()]
    buttons.observe(drop_data,'value')
    
    def data_points(buttons, drop):
        fig = ipv.figure()
        basic_model = ipv.scatter(all_pt[0],all_pt[1],all_pt[2],size=2,marker='sphere',color='red')
        for i in range(len(traces)):
            x_l = traces[i]['x_l']
            y_l = traces[i]['y_l']
            z_l = traces[i]['z_l']
            lin = ipv.plot_wireframe(x_l,y_l,z_l)
        if drop != None:
            if buttons == 'Analysis':
                x = pt55[in_names55[drop]][0]
                y = pt55[in_names55[drop]][1]
                z = pt55[in_names55[drop]][2]
                points_hi = ipv.scatter(x,y,z,size=3,color='blue',marker='circle_2d')
            if buttons == 'Function data':
                x = pt58[in_names58[drop]][0]
                y = pt58[in_names58[drop]][1]
                z = pt58[in_names58[drop]][2]
                points_hi = ipv.scatter(x,y,z,size=3,color='blue',marker='circle_2d')
        
        ipv.xlim(min(all_pt[0])-1,max(all_pt[0])+1)
        ipv.ylim(min(all_pt[1])-1,max(all_pt[1])+1)
        ipv.zlim(min(all_pt[2])-1,max(all_pt[2])+1)
        ipv.show()
       
    
    out = widgets.interactive_output(data_points, {'buttons':buttons, 'drop':drop})
    display(widgets.VBox([widgets.VBox([widgets.Label(i) for i in info]),widgets.HBox([out,widgets.VBox([buttons,drop])])]))
    
    return buttons,drop