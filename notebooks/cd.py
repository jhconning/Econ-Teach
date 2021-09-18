
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
import numpy as np
plt.style.use('seaborn-whitegrid')
from mpl_toolkits.mplot3d import *
from matplotlib import cm
from scipy.optimize import minimize




plt.style.use('bmh')
plt.rcParams["figure.figsize"] = [7,7]
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["font.size"] = 18

ALPHA = 1/2

# Consumer choice

def budgetc(c0,p,I):
    '''c1 as a function of c0 along budget line'''
    return I - p*c0

def u(c, a=ALPHA):
    '''Utility at c=(c[0], c[1])'''
    return (c[0]**a)*(c[1]**(1-a))

def MU0(c, a=ALPHA):
    '''MU of Cobb-Douglas'''
    return  a*u(c,a)/c[0] 

def MU1(c, a=ALPHA):
    return  (1-a)*u(c,a)/c[1]

def indif(c0, ubar, a=ALPHA):
    '''c1 as function of c0, implicitly defined by U(c0, c1) = ubar'''
    return (ubar/(c0**a))**(1/(1-a))

def cd_demands(p,I,a =ALPHA):
    '''Analytic solution for interior optimum'''
    c0 = a * I/p
    c1 = (1-a)*I
    c = [c0,c1]
    uopt = u(c,a)
    return c, uopt

def consume_plot(p, I, a=ALPHA):
    cmax = max(I, I/p)*1.1
    c0 = np.linspace(0.1,cmax,num=100)
    ce, uebar = cd_demands(p, I, a)
    fig, ax = plt.subplots(figsize=(9,9))
    ax.plot(c0, budgetc(c0, p, I), lw=2.5)
    ax.fill_between(c0, budgetc(c0, p, I), alpha = 0.2)
    ax.plot(c0, indif(c0, uebar, a), lw=2.5)
    ax.vlines(ce[0],0,ce[1], linestyles="dashed")
    ax.hlines(ce[1],0,ce[0], linestyles="dashed")
    ax.plot(ce[0],ce[1],'ob')

    ax.set_xlim(0, cmax)
    ax.set_ylim(0, cmax)
    ax.set_xlabel(r'$c_0$', fontsize=16)
    ax.set_ylabel('$c_1$', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

def arb_plot(c0g=20, I=100, p=1):
    cg = [c0g, I - c0g]
    cmax = max(I, I/p)*1.1
    c0 = np.linspace(0.1,cmax,num=100)
    
    '''Display characteristics of a guess along the constraint'''
    fig, ax = plt.subplots(figsize=(9,9))
    ax.plot(c0, budgetc(c0, p, I), lw=1)
    ax.fill_between(c0, budgetc(c0, p, I), alpha = 0.2)
    ax.plot(c0, indif(c0, u(cg)), lw=2.5)
    ax.vlines(cg[0],0,cg[1], linestyles="dashed")
    ax.hlines(cg[1],0,cg[0], linestyles="dashed")
    ax.plot(cg[0],cg[1],'ob')
    mu0pd, mu1pd = MU0(cg), MU1(cg)/p
    if mu0pd > mu1pd:
        inq = r'$>$'
    elif mu0pd < mu1pd:
        inq = r'$<$'
    else:
        inq =r'$=$'
    ax.text(60, 120, r'$\frac{MU_0}{p_0}$'+inq+r'$\frac{MU_1}{p_1}$',fontsize=20)
    utext = r'$({:5.1f}, {:5.1f}) \ \ U={:5.3f}$'.format(cg[0], cg[1], u(cg))
    ax.text(60, 100, utext, fontsize=12)
    ax.set_xlim(0, cmax)
    ax.set_ylim(0, cmax)
    ax.set_xlabel(r'$c_0$', fontsize=16)
    ax.set_ylabel('$c_1$', fontsize=16)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.set_title('The No-Arbitrage argument')
    plt.show()


#


## Ricardian model

def rppf(mplx, mply, lbar, show = True, title='Home'):
    '''Plot a linear PPF diagram
       show == False delays plt.show() to allow other elements to be plotted first'''
    qy = mply*lbar - (mply/mplx) * QX
    plt.plot(QX, qy, linewidth=2, label='PPF')
    plt.axis([0,XMAX,0,YMAX])
    plt.xlabel(NAMEX), plt.ylabel(NAMEY), plt.title(title)
    plt.text(0.3*XMAX, 0.9*YMAX,
             r'   $\frac{MPL_Y}{MPL_X}=$'+'{:3.2f}'.format(mply/mplx))
    if show: #use False for subplots
        plt.show();

## Linear Demand and Supply


def PD(Q, A, b):
    return np.array(A - b * Q)

def PS(Q, F, c):
    return np.array(F + c * Q)

def market(Q, A, b, F, c):
    plt.figure(figsize=(7,7))
    plt.plot(Q,PD(Q, A, b))
    plt.plot(Q, PS(Q, F, c))
    plt.show()
    

if __name__ == '__main__':
    print('Running program tests')


