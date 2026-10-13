import sys, json, os, numpy as np
from PIL import Image, ImageOps, ImageDraw
from scipy.ndimage import uniform_filter1d
from scipy.signal import find_peaks
def load(n):
    im=ImageOps.exif_transpose(Image.open(os.path.expanduser(f'~/Downloads/20261013-{n}.jpeg'))).convert('L')
    return im
def detect(n, box, ncol, nb=12):
    im=load(n); a=np.asarray(im).astype(float)
    x0,y0,x1,y1=box
    sub=a[y0:y1,x0:x1]
    ink=np.clip(170-sub,0,None)
    cw=(x1-x0)/ncol
    H=y1-y0; res=[]
    for b in range(nb):
        ys=int(b*H/nb); ye=int((b+1)*H/nb)
        prof=ink[ys:ye].sum(0); prof=uniform_filter1d(prof,int(cw*0.5))
        pk,_=find_peaks(prof,distance=int(cw*0.6))
        top=sorted(pk,key=lambda p:-prof[p])[:ncol]
        res.append(((ys+ye)/2, sorted(top)))
    return res
if __name__=='__main__':
    n=sys.argv[1]; box=list(map(int,sys.argv[2:6])); nc=int(sys.argv[6])
    for y,p in detect(n,box,nc): print(int(y), [int(x)+box[0] for x in p])
