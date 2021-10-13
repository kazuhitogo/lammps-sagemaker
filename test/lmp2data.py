def readlines_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def func_elec(filein, naatom):
    lines = readlines_file(filein)
    i = 0
    while(True):
        if('Atoms' in lines[i]):
            break
        i += 1
    elec = np.array([float(lines[i+2+j].split()[3]) for j in range(naatom)])
    return elec

def func_replica():
    fname = sys.argv[1]
#    print(fname)
#    sys.exit()
#    fname = 'equiliv'
    filein1 = 'tmp1'
    filein1 = 'lmp_' + filein1 + '.data'
    filein2 = 'lmp_' + fname + '.lammpstrj'
    fileout1 = 'lmp_' + fname + '.data'

    print('start', fname)
    lines = readlines_file(filein2)
    naatom = int(lines[3])
    x1, x2 = lines[-naatom-4].split()
    x1, x2 = float(x1), float(x2)
    sdx = x2 - x1
    y1, y2 = lines[-naatom-3].split()
    y1, y2 = float(y1), float(y2)
    sdy = y2 - y1
    z1, z2 = lines[-naatom-2].split()
    z1, z2 = float(z1), float(z2)
    sdz = z2 - z1
    nstep = int(lines[-naatom-8])
    li = [_.split() for _ in lines[-naatom:]]
    df_trj = pd.DataFrame(li, dtype='float').sort_values(0)
    mat_trj = df_trj.values
    print('naatom, nstep, x1, x2, y1, y2, z1, z2 =', naatom, nstep, x1, x2, y1, y2, z1, z2)
    
    elec = func_elec(filein1, naatom)
    print('sum qulon', np.sum(elec))
    mat_trj = np.insert(mat_trj, 3, elec, axis=1)
    
    fi1 = open(filein1, 'r')
    lines = fi1.readline()
    fo1 = open(fileout1, "wt")
    
    while lines:
        if('xlo' in lines):
            fo1.write(" %.10e %.10e xlo xhi\n" %(x1, x2)); lines = fi1.readline()
            fo1.write(" %.10e %.10e ylo yhi\n" %(y1, y2)); lines = fi1.readline()
            fo1.write(" %.10e %.10e zlo zhi\n" %(z1, z2)); lines = fi1.readline()
            break
        else:
            fo1.write("%s" %lines); lines = fi1.readline()
    while lines:
        if('Atoms' in lines):
            fo1.write("%s" %lines); lines = fi1.readline()
            fo1.write("%s" %lines); lines = fi1.readline()
            for i in range(naatom):
                fo1.write("%7d %4d %d %.15e %.8e %.8e %.8e %2d %2d %2d\n" %(mat_trj[i,0], mat_trj[i,1], \
                    mat_trj[i,2], mat_trj[i,3], mat_trj[i,4]*sdx+x1, mat_trj[i,5]*sdy+y1, mat_trj[i,6]*sdz+z1, \
                    mat_trj[i,7], mat_trj[i,8], mat_trj[i,9]))
            fo1.write("\n")
            break
        else:
            fo1.write("%s" %lines); lines = fi1.readline()
    while ('Bonds' not in lines):
        lines = fi1.readline()
    while lines:
        fo1.write("%s" %lines); lines = fi1.readline()
    fo1.close()
    print('finish replica')

def main():
    func_replica()

import numpy as np
import pandas as pd
import time, sys, os ,codecs

if __name__=='__main__':
    main()
