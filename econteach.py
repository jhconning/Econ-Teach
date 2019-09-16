# -*- coding: utf-8 -*-
"""
Created on Mon Sep 16 08:57:01 2019

@author: jconning
"""

import numpy as np
import matplotlib.pyplot as plt


plt.style.use('bmh')
plt.rcParams["figure.figsize"] = [7,7]
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["font.size"] = 18



# Some default parameters when none are supplied
MPLX = 1
MPLY = 1
LBAR = 100

NAMEX = 'Good X'
NAMEY = 'Good Y'

XMAX = LBAR*MPLX*4   # for plot bounds and aesthetics
YMAX = LBAR*MPLY*4
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
    plt.text(0.3*XMAX, 0.9*YMAX, 
             r'   $\frac{P_X}{P_Y}=$'+'{:3.2f}'.format(px/py)+' Y/X',
             fontsize=12)
    if show: #use False for subplots
        plt.show();
        
def ppf(mplx=MPLX, mply=MPLY, lbar=LBAR, show = False, title='Home'):   
    '''Plot a linear PPF diagram 
       show == False delays plt.show() to allow other elements to be plotted first'''
    qy = mply*lbar - (mply/mplx) * QX
    plt.plot(QX, qy, linewidth=2, label='PPF')
    plt.axis([0,XMAX,0,YMAX])
    plt.xlabel(NAMEX), plt.ylabel(NAMEY), plt.title(title)
    plt.text(0.15*XMAX, 0.9*YMAX, 
             r' $\frac{MPL_Y}{MPL_X}=\frac{P_X}{P_Y}=$'+'{:3.2f}'.format(mply/mplx)
             + ' Y/X', fontsize=14  )  
    if show: #use False for subplots
        plt.show();
        
def openppf(mplx, mply, lbar, pw, show=True, title='Home'):
    ppf(mplx, mply, lbar, show=False, title=title)
    if pw < (mply/mplx):
        plt.plot(QX, mply*lbar - pw * QX, linestyle='--' )
        plt.scatter(0, mply*lbar, s=100, clip_on=False)
    else:
        plt.plot(QX, pw*mplx*lbar - pw * QX, linestyle='--' )
        plt.scatter(mplx*lbar,0, s=100, clip_on=False)
  
def twopane(mplx, mply, lbar, mplfx, mplfy, lbarf, p):
    foreign = openppf
    plt.figure(1, figsize =(12,12))
    plt.subplot(121, aspect='equal')
    openppf(mplx, mply, lbar, p, show = False)
    plt.subplot(122, aspect='equal')
    foreign(mplfx, mplfy, lbarf, p, show=False, title='Foreign')
    plt.ylabel(''); 

def indif(x, ubar):
    return ubar/x      

def indif_plot(p, I):
    xe, ye = I/(2*p) , I/2
    plt.scatter(xe,ye)
    ubar = xe*ye
    QX_ = np.where( (QX>xe*0.3)&(QX<xe*2), QX, 
                   np.nan)
    plt.plot(QX_, indif(QX_, ubar))

    

if __name__ == "__main__":
    print('budget plot')
    budget()
    
    print('simple PPF')
    ppf(mplx=2,mply=1,lbar=200)
    
    print('open economy PPF')
    openppf(mplx=2,mply=1,lbar=200, pw=1)
    
    print('two country')
    twopane(MPLX, MPLY, LBAR, 4*MPLX, 2*MPLY, LBAR, p=3/4)
    