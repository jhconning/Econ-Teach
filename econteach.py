# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 08:57:01 2019

@author: jconning
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve


plt.style.use('bmh')
plt.rcParams["figure.figsize"] = [7,7]
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["font.size"] = 18



# Some default parameters when none are supplied
MPLX = 2
MPLY = 1
LBAR = 100

NAMEX = 'Good X'
NAMEY = 'Good Y'

XMAX = 400   # for plot bounds and aesthetics
YMAX = 400
N = 50              # num of datapoints to plot
QX =  np.linspace(0.1, XMAX, N)

def budget(px=1, py=1, I=100, show = False):   
    '''Plot a linear PPF diagram 
       show == False delays plt.show() to allow other elements to be plotted first'''
    XMAX, YMAX = 300,300
    qy = I/py - (px/py) * QX
    plt.plot(QX, qy, linewidth=2, label='Budget')
    plt.axis([0,XMAX,0,YMAX])
    plt.xlabel(NAMEX), plt.ylabel(NAMEY)
    #plt.text(0.3*XMAX, 0.9*YMAX, 
    #         r'   $\frac{P_X}{P_Y}=$'+'{:3.2f}'.format(px/py)+' Y/X',
    #         fontsize=12)
    if show: #use False for subplots
        plt.show();
        
def ppf(mplx=MPLX, mply=MPLY, lbar=LBAR, show = False, title='Home'):   
    '''Plot a linear PPF diagram 
       show == False delays plt.show() to allow other elements to be plotted first'''
    qy = mply*lbar - (mply/mplx) * QX
    plt.plot(QX, qy, linewidth=2, label='PPF')
    plt.axis([0,XMAX,0,YMAX])
    plt.xlabel(NAMEX), plt.ylabel(NAMEY)
    plt.title(title)
    plt.text(0.15*XMAX, 0.9*YMAX, 
             r' $\frac{MPL_Y}{MPL_X}=\frac{P_X}{P_Y}=$'+'{:3.2f}'.format(mply/mplx)
             + ' Y/X', fontsize=14  )  
    if show: #use False for subplots
        plt.show();
        
def twoppf(mplx, mply, lbar, mplfx, mplfy, lbarf):
    foreign = ppf
    plt.figure(1, figsize =(12,12))
    plt.subplot(121, aspect='equal')
    ppf(mplx, mply, lbar, title='Home')
    plt.subplot(122, aspect='equal')
    foreign(mplfx, mplfy, lbarf, title='Foreign')
    plt.ylabel('')
          
       
# We assume very simple Cobb-Douglas preferences
    
def indif(x, ubar):
    return ubar/x      

def demands(p, I):
     return I/(2*p) , I/2

def indif_plot(p, I):
    xd, yd = demands(p, I)
    plt.scatter(xd,yd)
    ubar = xd*yd
    QX_ = np.where( (QX>xd*0.3)&(QX<xd*2), QX, np.nan) #clip for aesthetics
    plt.plot(QX_, indif(QX_, ubar))
    
def openeq(mplx=MPLX, mply=MPLY, lbar=LBAR, pw=1):
    if pw > mply/mplx:
        qx = mplx*lbar
        qy = 0
    elif pw <= mply/mplx:
        qx =0
        qy = mply*lbar
    I = pw*qx + qy       
    cx, cy = demands(pw,I)
    return qx, qy, cx, cy
       

def openppf(mplx=MPLX, mply=MPLY, lbar=LBAR, pw=1, show = False, title='Home'):
    '''Like ppf but also plots world price line and specialization'''
    ppf(mplx, mply, lbar)
    qx, qy, cx, cy = openeq(mplx, mply, lbar, pw)
    plt.scatter(qx,qy)
    plt.title(title)
    I = pw*qx + qy    #income measured in units of y
    budget(px=pw, py=1, I=I)
    indif_plot(pw, I)


def worldprice(mplx, mply, lbar, mplfx, mplfy, lbarf):
    '''  World equilibrium price consistent with balanced trade
    By Walras' law we just need to find price at which excess demand in 
    one market is eliminated
    '''
    def xsdemand(p):
        qx, _, cx, _ = openeq(mplx, mply, lbar, p)
        qfx, _, cfx, _ = openeq(mplfx, mplfy, lbarf, p)
        return (cx + cfx) - (qx + qfx) 
    
    guess = (mply/mplx + mplfy/mplfx)/2 
    return fsolve(xsdemand, guess)[0]
    

def twopane(mplx=MPLX, mply=MPLY, lbar=LBAR, 
            mplfx=MPLY, mplfy=MPLX, lbarf=LBAR, p=1):
    foreign = openppf
    plt.figure(1, figsize =(12,12))
    plt.subplot(121, aspect='equal')
    openppf(mplx, mply, lbar, p, title='Home')
    plt.subplot(122, aspect='equal')
    foreign(mplfx, mplfy, lbarf, p, title='Foreign')
    plt.ylabel('')
    
def worldeq(mplx=MPLX, mply=MPLY, lbar=LBAR, 
            mplfx=MPLY, mplfy=MPLX, lbarf=LBAR):
    
    pw = worldprice(mplx, mply, lbar, mplfx, mplfy, lbarf)
    twopane(mplx, mply, lbar, mplfx, mplfy, lbarf, p=pw)

    

if __name__ == "__main__":
    print('budget plot')
    budget()
    
    print('simple PPF')
    ppf(mplx=2,mply=1,lbar=200)
    
    print('open economy PPF')
    openppf(mplx=2,mply=1,lbar=200, pw=1)
    
    print('two country')
    twopane(MPLX, MPLY, LBAR, 4*MPLX, 2*MPLY, LBAR, p=3/4)
    