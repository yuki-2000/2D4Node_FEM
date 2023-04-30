# -*- coding: utf-8 -*-
"""
Created on Sun May  8 12:45:40 2022

@author: yuki
"""

import numpy as np

x = np.array(range(1000))
y = np.array(range(20))

amp = 100




xx, yy = np.meshgrid(x,y)

xx = xx.ravel()
yy = yy.ravel()

cordinate = []
for i in range(len(x) * len(y)):
    cordinate.append([xx[i],yy[i]])
cordinate = np.array(cordinate, dtype=np.float64)
cordinate /=amp
element = []

"""
elnum = 0
elx = 0
ely = 0
for i in range(len(y)-1):

    
    for j in range(len(x)-1):
        element.add([elnum, ely*len(x)+elx,  ely*len(x)+elx+1, (ely+1)*len(x)+elx,  (ely+1)*len(x)+elx+1 ])
        elnum += 1
    ely +=1
"""


elnum = 0
for i in range(len(y)-1):    
    for j in range(len(x)-1):
        element.append([elnum, i*len(x)+j,  i*len(x)+j+1,  (i+1)*len(x)+j+1 , (i+1)*len(x)+j])
        elnum += 1


element = np.array(element)

#1スタートに変更
element +=1







import pandas as pd
cornum = np.array(range(1, len(cordinate) +1))
df = pd.DataFrame(cordinate, cornum, dtype=np.float64)
df.to_csv('benchmark_input_point.txt',sep=' ', header=False, index=True)


df = pd.DataFrame(element)
df.to_csv('benchmark_input_eleme.txt',sep=' ', header=False, index=False)


matid = np.ones(len(element) ,dtype=np.int32)
elenum = np.array(range(1, len(element) +1))


df = pd.DataFrame(matid, elenum)
df.to_csv('benchmark_input_material.txt',sep=' ', header=False, index=True)



fixed_node = np.where(cordinate[:,0]==0)[0] 

fix_direction = [1 for i in range(len(fixed_node))]
fix_direction += [2 for i in range(len(fixed_node))]
fix_direction = np.array(fix_direction)

fixed_node = np.append(fixed_node, fixed_node)
fixed_node +=1
ficed_val = [0 for i in range(len(fixed_node))]
ficed_val = np.array(ficed_val)

fixednodenum = np.array(range(1, len(fixed_node) +1))


df = pd.DataFrame( fixed_node, fixednodenum)
df[1] = fix_direction
df[2] = ficed_val
df.to_csv('benchmark_input_fixednodes.txt',sep=' ', header=False, index=True)






print(len(cordinate), "!モデル節点数")
print(len(element), "!モデル要素数")
print(1,  "!材料種類数")
print(len(fixed_node),"!拘束点数")

analysys_text = ""
analysys_text += str(len(cordinate)) + "!モデル節点数\n"
analysys_text += str(len(element)) +"!モデル要素数\n"
analysys_text += "1 !材料種類数\n"
analysys_text += str(len(fixed_node)) + "!拘束点数\n"
analysys_text +="3 !荷重点数\n1.0d3 !変形図倍率\n1.0d0 !厚み"


with open("benchmark_input_AnalysisConditions.txt", mode='w', encoding="utf-8") as f:
    f.write(analysys_text)

import matplotlib.pyplot as plt
import matplotlib.collections
import numpy as np

def showMeshPlot(nodes, elements, values, title):

    y = nodes[:,0]
    z = nodes[:,1]

    def quatplot(y,z, quatrangles, values, ax=None, **kwargs):

        if not ax: ax=plt.gca()
        yz = np.c_[y,z]
        verts= yz[quatrangles]
        pc = matplotlib.collections.PolyCollection(verts, **kwargs)
        pc.set_array(values)
        ax.add_collection(pc)
        ax.autoscale()
        return pc

    fig, ax = plt.subplots(dpi=500)
    ax.set_aspect('equal')

    pc = quatplot(y,z, np.asarray(elements), values, ax=ax, 
             edgecolor="black", cmap="rainbow",linewidths=(0.1,))
    fig.colorbar(pc, ax=ax)        
    #ax.plot(y,z, marker="o", ls="", color="black")

    ax.set(title=title, xlabel='X Axis', ylabel='Y Axis')

    plt.show()
    #fig.savefig(f'result_{title}.png')



node = cordinate
eleme = element[:,1:]
title = "test"
value = np.zeros(len(x) * len(y))

showMeshPlot(nodes=node, elements=eleme-1, values=value, title = title)











