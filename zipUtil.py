import bz2
import pickle

def zip_write(filename, data):
    with bz2.BZ2File(filename+'.pbz2', 'w') as f:
        pickle.dump(data, f)

def zip_read(filename):
    if ('.pbz2' in filename):
        return pickle.load(bz2.BZ2File(filename, 'rb'))
    else:
        return pickle.load(bz2.BZ2File(filename+'.pbz2', 'rb'))