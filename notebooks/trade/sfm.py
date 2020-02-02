# -*- coding: utf-8 -*-

"""
Code for:
 -  specific factors model SFM.ipynb
 -  Tariff_in_general_equilibrium.ipynb

Created on Mon Oct 3 2019 16 08:57:01 2019

@author: jconning
"""


import numpy as np
from scipy.optimize import fsolve
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
import seaborn

plt.style.use('seaborn-colorblind')
plt.rcParams["figure.figsize"] = [7,7]
plt.rcParams["axes.spines.right"] = True
plt.rcParams["axes.spines.top"] = False
plt.rcParams["font.size"] = 18
plt.rcParams['axes.grid']=True

Tbar = 100       # Fixed specific land in ag. 
Kbar = 100       # Fixed specific capital in manuf
Lbar = 400       # Total number of mobile workers
LbarMax = 400    # Lbar will be on slider, max value.

p    = 1.00      # initial rel price of ag goods, p = Pa/Pm
alpha, beta = 0.5, 0.5  # labor share in ag, manuf

La = np.linspace(1, LbarMax-1,LbarMax)
Lm = Lbar - La

def F(La, Tbar = Tbar):
    return (Tbar**(1-alpha) * La**alpha)

def G(Lm, Kbar =Kbar):
    return (Kbar**(1-beta) * Lm**beta) 

def MPLa(La, Tbar=Tbar):
    return alpha*Tbar**(1-alpha) * La**(alpha-1)

def MPLm(Lm, Kbar=Kbar):
    return beta*Kbar**(1-beta) * Lm**(beta-1)

def MPT(La, Tbar=Tbar):
    return (1-alpha)*Tbar**(-alpha) * La**alpha

def MPK(Lm, Kbar=Kbar):
    return (1-beta)*Kbar**(-beta) * Lm**beta

def ppf(Tbar=Tbar, Kbar=Kbar, Lbar=Lbar):
    plt.xlim(0,300)
    plt.ylim(0,300)
    Qa = F(La, Tbar) * (La<Lbar)
    Qm = G(Lm, Kbar) 
    plt.title('Production Possibility Frontier')
    plt.xlabel(r'$Q_a$')
    plt.ylabel(r'$Q_m$')
    plt.plot(Qa, Qm)
    plt.gca().set_aspect('equal')


LDa = p * MPLa(La) *(La<Lbar)         # for Cobb-Douglas MPL can be written this way
LDm = MPLm(Lbar-La)

def eqn(p, Lbar=Lbar, Tbar=Tbar, Kbar=Kbar):
    '''returns numerically found equilibrium labor allocation and wage'''
    def func(La):
        return p*MPLa(La, Tbar) - MPLm(Lbar-La, Kbar)
    Laeq = fsolve(func, 1)[0]
    return Laeq, p*MPLa(Laeq, Tbar)

def u(x,y):
    '''Utility function'''
    return x*y

def XD(p, Lbar = Lbar, Tbar=Tbar, Kbar=Kbar):
    '''Cobb-Douglas demand for goods given world prices (national income computed)'''
    LAe, we = eqn(p, Lbar, Tbar, Kbar)
    # gdp at world prices measured in manuf goods
    gdp = p*F(LAe, Tbar = Tbar) + G(Lbar -LAe, Kbar=Kbar)
    return (1/2)*gdp/p, (1/2)*gdp

def indif(x, ubar):
    return ubar/x 

def p_autarky(Lbar=Lbar, Tbar=Tbar, Kbar=Kbar):
    '''Find autarky product prices. By Walras' law enough to find price that 
    sets excess demand in just one market''' 
    def excessdemandA(p):
        LAe, _ = eqn(p)
        QA = F(LAe, Tbar = Tbar)
        CA, CM = XD(p, Lbar=Lbar) 
        return QA-CA
    peq = fsolve(excessdemandA, 1)[0]
    return peq
    
def sfmtrade(p):
    Ca = np.linspace(0,200,200)
    LAe, we = eqn(p)
    X, Y = F(LAe, Tbar = Tbar), G(Lbar -LAe)
    gdp = p*X + Y
    print(f'(QX, QY) = ({X:3.1f}, {Y:3.1f})')
    print(f'(CX, CY) = ({XD(p)[0]:3.1f}, {XD(p)[1]:3.1f})')
    plt.scatter(F(LAe, Tbar), G(Lbar-LAe, Tbar), label='Trade produce')
    plt.scatter(*XD(p),label='Trade consume', marker='s')
    plt.scatter(*XD(p_autarky()), marker='x', label='Autarky')
    plt.plot([0,gdp/p],[gdp, 0])
    ppf(100)
    ub = u(*XD(p))
    #plt.ylim(0,gdp)
    #plt.xlim(0,gdp)
    plt.xlim(0,300)
    plt.ylim(0,300)
    plt.plot(Ca, indif(Ca, ub))
    plt.grid(False)
    plt.legend()
    plt.gca().spines['bottom'].set_position('zero')
    plt.gca().spines['left'].set_position('zero')





La = np.arange(0, LbarMax)   # this is always over the LbarMax range

def sfmplot(p, Lbar=LbarMax, Tbar=Tbar, Kbar=Kbar, show=True):
    Lm = Lbar - La
    Qa = (Tbar**(1-alpha) * La**alpha) * (La<Lbar)
    Qm = Kbar**(1-beta) * (Lbar - La)**beta
    pMPLa = (p * alpha * Qa/La)*(La<Lbar)     # for Cobb-Douglass MPL can be written this way
    MPLm = beta * Qm/(Lbar-La)
    LA, weq = eqn(p, Lbar, Tbar, Kbar)
    ymax = 1.0
    plt.ylim(0,ymax)
    plt.xlim(0,LbarMax)
    plt.title('Specific Factors Model')
    plt.plot(La, pMPLa, linewidth = 3, label='AG labor demand')
    plt.plot(La, MPLm, linewidth=3, label ='MF labor demand')
    plt.scatter(LA, weq, s=100, color='black')
    plt.axhline(weq, linestyle='dashed')
    plt.axvline(Lbar, linewidth = 3)
    plt.plot([LA, LA],[0, weq], linestyle='dashed')
    plt.xlabel('Labor')
    plt.ylabel('Real wage --' + r'$\frac{w}{p_M}$')
    plt.grid()
    if show:
        plt.legend(loc=(1.04,0.9))
        print("(La, Lm) = ({0:3.0f}, {1:3.0f})   wage: (w/Pm, w/Pa) =({2:3.2f}, {3:3.2f})"
              .format(LA, Lbar-LA, weq, weq/p))
        print("land rent: (v/Pa, v/Pm) = ({0:3.2f}, {1:3.2f})  capital rental: (r/Pa, r/Pm) = ({2:3.2f}, {3:3.2f})"
              .format(MPT(LA,Tbar), p*MPT(LA,Tbar), MPK(Lbar-LA,Kbar)/p, MPK(Lbar-LA, Kbar)    )   )
        plt.show()

def sfmplot2(p):
    sfmplot(1, show=False)
    sfmplot(p, show=False)
    plt.grid(False)
    if p == 1:
        plt.title('SF Model');
    else:
        La0, w0 = eqn(1)
        plt.scatter(La0,w0*p, s=100, color='black')  #where wage would rise to without labor movement 
        if p>1:
            plt.title(r'$\frac{P_a}{P_m} \uparrow  \rightarrow  \frac{w}{P_m} \uparrow, \frac{w}{P_a} \downarrow $'  );
        elif p<1:
            plt.title(r'$\frac{P_a}{P_m} \downarrow  \rightarrow  \frac{w}{P_m} \downarrow, \frac{w}{P_a} \uparrow $'  );
    plt.show();
        

## For the tariffs in general equilibrium

def open_trade(p, t=0, dt=False):
    ppf(100)
    Ca = np.linspace(0,250,200)
    pt = p*(1+t)
    LAe, we = eqn(pt)
    X, Y = F(LAe, Tbar = Tbar), G(Lbar -LAe)
    wgdp = p*X + Y  # gdp at world prices
    dgdp = pt*X + Y
    plt.scatter(*XD(p,t), marker='o', label='Trade')
    plt.scatter(X,Y, marker='o', label='Trade')
    plt.plot([0,wgdp/p],[wgdp, 0])
    ub = u(*XD(p,t))
    plt.ylim(0,300)
    plt.xlim(0,300)
    plt.plot(Ca, indif(Ca, ub))
    if dt:
        plt.plot([0,dgdp/pt],[dgdp, 0], c='g')
    plt.grid(False)
    #plt.legend()
    ax = plt.gca()
    ax.spines['bottom'].set_position('zero')
    ax.spines['left'].set_position('zero')