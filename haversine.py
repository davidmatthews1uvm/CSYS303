import numpy as np


def dist(coord1,coord2):
    lon1,lat1=coord1
    lon2,lat2=coord2
    
    R=6371000                               # radius of Earth in meters
    phi_1=np.radians(lat1)
    phi_2=np.radians(lat2)

    delta_phi=np.radians(lat2-lat1)
    delta_lambda=np.radians(lon2-lon1)

    a=np.sin(delta_phi/2.0)**2+\
        np.cos(phi_1)*np.cos(phi_2)*\
        np.sin(delta_lambda/2.0)**2
    c=2*np.arctan2(np.sqrt(a), np.sqrt(1-a))
    return R * c # meters!