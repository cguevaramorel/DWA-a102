# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 14:44:37 2021

@author: carlosGuevara
"""

# install git
# conda install pip
# pip install git+https://github.com/woodcrafty/PyETo#egg=PyETo
import numpy as np
import pandas as pd
import pyeto as pyeto
from pyeto import thornthwaite, monthly_mean_daylight_hours, deg2rad


from check import *
from coefficients import *

#%% class Roof
class Roof(object):
    ''' 
    generic roof object for water balance calculations 
    
    Parameters
    ----------
    Area : float
         element area in m2       
        
    P : float
      precipitation in mm/a
          
    ETp : float
        evapotranspiration in mm/yr
        
    Sp : float
       storage height in mm
       default: 0.3
    
    
    Methods
    -------
    steep: Berechnungsansatz B.3.1: Steildach (alle Deckungsmaterialien)
           Flachdach (Metall, Glas) 
    
    
    Notes
    -----
    Storage height (Sp) in roofs varies between 0.1 and 0.6 mm. 
    Standard storage value for steep roof in general is 0.3 mm, 
    in case of glass or metal cover use 0.6 mm
    
    Examples
    --------
    
    
    '''
    
    def __init__(self, area, pcp, Etp, Sp=0.3):
        
        self.area = area
        self.pcp = pcp
        self.Etp = Etp
        self.Sp = Sp
        
        
        # check physical ranges from input values
        validRange(self.pcp, 'p')
        validRange(self.Etp, 'Etp')
        validRange(self.Sp, 'Sp')
        
    def __repr__(self):
        ''' '''
        return f'Roof object with area: {self.area} and height: {self.Sp}'
        

    def steep(self):
        '''
        Calculates steep roof coefficients
        
        Parameters
        ----------

           
        Notes    
        ------

        
        Returns
        -------
        df : DataFrame 
        '''          
        pcp = self.pcp
        area = self.area
        # calculate a coefficient          
        a = a_steepRoof(pcp, self.Etp, self.Sp)
        g = 0
        v = 1-a-g
        RD = pcp*a
        GWN = pcp*g
        ETP = pcp*v
        inflow = area*pcp / 1000
        Q_RD = area*pcp*a / 1000
        Q_GWN = area*pcp*g / 1000
        Q_ETP = area*pcp*v / 1000    
        # pfractions = (a, g, v)
        results = [{'Name' : "Area", 'Unit': "m2", 'Value': self.area},
                   {'Name' : "P", 'Unit': "mm/a", 'Value': self.pcp,},
                   {'Name' : "ETp", 'Unit': "mm/a", 'Value': self.Etp},
                   {'Name' : "a", 'Unit': "-", 'Value': a},
                   {'Name' : "g", 'Unit': "-", 'Value': g},
                   {'Name' : "v", 'Unit': "-", 'Value': v},
                   {'Name' : "RD", 'Unit': "mm/a", 'Value': RD},
                   {'Name' : "GWN", 'Unit': "mm/a", 'Value': GWN},
                   {'Name' : "ETp", 'Unit': "mm/a", 'Value': ETP},
                   {'Name' : "Inflow", 'Unit': "m3/a",'Value': inflow},
                   {'Name' : "RD flow", 'Unit': "m3/a", 'Value': Q_RD},
                   {'Name' : "GWN flow", 'Unit': "m3/a", 'Value': Q_GWN},
                   {'Name' : "ETP flow", 'Unit': "m3/a", 'Value': Q_ETP}]
        results = pd.DataFrame(results)
        results.Value = results.Value.round(3)
        return(results)

#%% run
if __name__ == "__main__":
    # Daylight hours
    mmdlh = pyeto.monthly_mean_daylight_hours(pyeto.deg2rad(52.38), 2014)
    # time
    monthly_t = [3.1, 3.5, 5.0, 6.7, 9.3, 12.1, 14.3, 14.1, 11.8, 8.9, 5.5, 3.8]
    #Evapotranspiration [mm/a] acc. to Thornthwaite
    Etp = sum(pyeto.thornthwaite(monthly_t, mmdlh))
    # roof area [m2]
    area = 100
    # precipitation [mm/a]
    pcp = 505 
    # roof object
    roof = Roof(area, pcp, Etp)
    # call steep
    steep = roof.steep()
