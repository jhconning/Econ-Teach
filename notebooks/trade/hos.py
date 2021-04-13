# -*- coding: utf-8 -*-

"""
Code for specific factors model
Created on Mon Oct 3 2019 16 08:57:01 2019

@author: jconning
"""


import numpy as np
from scipy.optimize import fsolve, minimize
np.seterr(divide='ignore', invalid='ignore')
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
import seaborn

plt.rcParams["figure.figsize"] = (9,9)
plt.style.use('seaborn-colorblind')
plt.rcParams["axes.spines.right"] = True
plt.rcParams["axes.spines.top"] = False
plt.rcParams["font.size"] = 18
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['axes.grid']=True

Kbar = 100     # economywide capital endowment
Lbar = 100     # economywide labor endowment
alpha = 0.6   # A capital share
beta = 0.4    # M capital share
theta = 0.5    # A consumption share

def F(K,L, alpha=alpha, beta=beta):
    return K**alpha * L**(1-alpha)

def G(K,L, alpha=alpha, beta=beta):
    return K**beta * L**(1-beta)

def U(Ca,Cm, theta=theta):
    return Ca**theta * Cm**(1-theta) 

def obj(X, alpha=alpha, beta=beta):
    return - U( F(X[0], X[1], alpha), G(Kbar-X[0], Lbar-X[1], beta) )

def kl(wr, kshare):
    return (kshare/(1-kshare))* wr

def isoq(L, kshare, qbar):
    return (qbar/(L**(1-kshare)))**(1/kshare)

def klplot(KL):
    wr = np.linspace(0,10,100)
    f, ax = plt.subplots(1)
    ax.set_xlabel(r'$\frac{K}{L}$')
    ax.set_xlim(0,10)
    ax.set_ylim(0,10)
    ax.set_ylabel(r'$\frac{w}{r}$ -- wage-rental')
    ax.plot(kl(wr, alpha), wr, linewidth=4)
    ax.plot(kl(wr, beta), wr, linewidth=4)
    ax.axvline(KL)
    ax.text(KL+0.5, 9, r'$\frac{\bar K}{\bar L}$ ')
    ax.set_aspect('equal');

ll = np.linspace(0.1,Lbar,100)
ll_ = np.linspace(0.05*Lbar,0.80*Lbar,100)

def SS(p):
    Za = alpha**alpha * (1-alpha)**((1-alpha))
    Zm = beta**beta * (1-beta)**((1-beta))  
    return (p*(Za/Zm))**(1/(alpha-beta))

def lerner(p):
    wr = SS(p=p)
    Kas = kl(wr, alpha)
    Kms = kl(wr, beta)
    QQ=30
    Lmqq = QQ/Kms**beta
    Kmqq = Kms*Lmqq
    Laqq = p*QQ/(Kas**alpha)
    Kaqq = Kas*Laqq

    I = Kmqq + wr*Lmqq
    f, ax = plt.subplots(1)
    plt.scatter(Laqq,Kaqq)
    plt.scatter(Lmqq,Kmqq)
    print(f'w/r = {wr:2.2f}, KLa = {Kas:2.2f}, KLm = {Kms:2.2f}')
    plt.xlim(0,100)
    plt.ylim(0,100)
    plt.plot(ll, Kas*ll, ':')
    plt.plot(ll, Kms*ll, ':')
    plt.plot(ll_, isoq(ll_,beta, QQ),'b')
    plt.plot(ll_, isoq(ll_,alpha, p*QQ))
    plt.text(ll_[-1],isoq(ll_[-1],beta,QQ),f"Qm={QQ}")
    plt.text(ll_[-1],isoq(ll_[-1],alpha,p*QQ),f"Qa=p*{QQ}")
    plt.plot(ll, I - wr*ll,'b:')
    plt.xlabel('L - labor')
    plt.ylabel('K - capital')
    plt.suptitle('Lerner Diagram', y=0.98)
    plt.title(f'w/r = {wr:2.2f},   Ka/La = {Kas:2.2f},   Km/Lm = {Kms:2.2f}', fontsize = 12)
    plt.gca().set_aspect('equal');

def ssplot(p):
    wr = SS(p=p)
    print(p,wr)
    pp = np.linspace(0.2,2,100)
    plt.plot(pp, SS(pp),'b')
    plt.ylabel(r'$\frac{w}{r}$')
    plt.xlabel(r'$p = \frac{p_m}{p_a}$')
    plt.axhline(y = wr, xmin = 0, xmax = p)
    plt.axvline(x = p, ymin=0, ymax =wr, linestyle=':')
    plt.ylim(0,6);

def num_opt(alpha=alpha, beta=beta):
    x0 = [50,50] # -- guess
    sol = minimize(obj, x0,args=(alpha,beta))
    Kae, Lae  = sol.x
    Qae, Qme = F(Kae,Lae, alpha), G(Kbar-Kae, Lbar-Lae, beta)
    return Qae, Qme

def PPF(La, alpha=alpha, beta=beta):
    '''Vary La and return F(Ka, La), G(K-Ka, L-La)'''
    Delta = (alpha/beta)*(1-beta)/(1-alpha)
    Ka = (Delta * La * Kbar) / (Lbar +(Delta-1)*La)
    return F(Ka,La), G(Kbar-Ka, Lbar-La)
    
def indif(Cm, theta , ubar):
    return (ubar/(Cm**(1-theta)))**(1/theta)

def closed_plot(alpha=alpha, beta=beta):
    Qa, Qm = PPF(ll, alpha, beta)
    Qae, Qme = num_opt(alpha, beta)
    print(Qae, Qme)
    plt.plot(Qm, Qa)
    plt.plot(ll, indif(ll, theta, U(Qae,Qme)) )
    plt.ylim(0,110)
    plt.xlim(0,110)
    plt.scatter(Qme, Qae);

def rybplot(p, Kbar=Kbar, Lbar=Lbar, alpha=alpha, beta=beta):
    """ Trade-style Edgeworth KL line intersections
    """
    ll = np.linspace(0.1,Lbar,100)
    wr = SS(p)
    ka = kl(wr, alpha)
    km = kl(wr, beta)
    LA = (Kbar-km*Lbar)/(ka-km)
    KA = ka*LA
    LM, KM = Lbar - LA, Kbar - KA
    fig, ax = plt.subplots()
    ax.set_xlim(0,Lbar)
    ax.set_ylim(0,Kbar)
    ax.set_xlabel('L - Labor')
    ax.set_ylabel('K - Capital')
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)
    ax.set_aspect('equal')
    ax.plot(ll,ka*ll, '--')
    ax.plot(ll,km*ll, '--')
    
    ax.scatter(LA,KA)
    ax.scatter(LM,KM)
    ax.scatter(0.5,0.5)
    Im = (KA-km*LA)+km*ll
    Ia = (KM-ka*LM)
    llm_up = np.linspace(LA,Lbar,100)
    lla_lo = np.linspace(LM,Lbar,100)
    ax.plot(llm_up,(KA-km*LA)+km*llm_up,'--')
    ax.plot(lla_lo,(KM-ka*LM)+ka*lla_lo,'--')
    ax.text(1.05*Lbar, 0.95*Kbar,r'  $p$'+f' = {p:3.1f}', fontsize=14)
    ax.text(1.05*Lbar, 0.95*Kbar-6,r'$(L_A,K_A)$'+f' = ({LA:2.0f}, {KA:2.0f})', fontsize=14)
    ax.text(1.05*Lbar, 0.95*Kbar-12,r'$(L_M,K_M)$'+f' = ({LM:2.0f}, {KM:2.0f})', fontsize=14)
    ax.text(1.05*Lbar, 0.95*Kbar-18,r'$(Q_A, Q_M)$'+f' = ({F(KA,LA):2.0f},{G(KM,LM):2.0f} )', fontsize=14)
    

def hos_eq(p, Kbar=Kbar, Lbar=Lbar):
    wr = SS(p)
    ka = kl(wr, alpha)
    km = kl(wr, beta)
    LA = (Kbar-km*Lbar)/(ka-km)
    KA = ka*LA
    return LA, KA

def edgeworth(L, Kbar=Kbar, Lbar=Lbar, alpha=alpha, beta=beta):
    """efficiency locus: """
    a = (1-alpha)/alpha
    b = (1-beta)/beta
    return b*L*Kbar/(a*(Lbar-L)+b*L)


def edgeplot(LA, Kbar=Kbar, Lbar=Lbar,alpha=alpha,beta=beta):
    """Draw an edgeworth box
    
    arguments:
    LA -- labor allocated to ag, from which calculate QA(Ka(La),La) 
    """
    KA = edgeworth(LA, Kbar, Lbar,alpha, beta)
    RTS = (alpha/(1-alpha))*(KA/LA)
    QA = F(KA,LA,alpha)
    QM = G(Kbar-KA,Lbar-LA,beta)
    print("(LA,KA)=({:4.1f}, {:4.1f})  (QA, QM)=({:4.1f}, {:4.1f})  RTS={:4.1f}"
          .format(LA,KA,QA,QM,RTS))
    La = np.arange(1,Lbar)
    fig, ax = plt.subplots(figsize=(7,6))
    ax.set_xlim(0, Lbar)
    ax.set_ylim(0, Kbar)
    ax.plot(La, edgeworth(La,Kbar,Lbar,alpha,beta),'k-')
    #ax.plot(La, La,'k--')
    ax.plot(La, isoq(La, alpha, QA))
    ax.plot(La, Kbar-isoq(Lbar-La, beta, QM),'g-')
    ax.plot(LA, KA,'ob')
    ax.vlines(LA,0,KA, linestyles="dashed")
    ax.hlines(KA,0,LA, linestyles="dashed")
    ax.text(-6,-6,r'$O_A$',fontsize=16)
    ax.text(Lbar,Kbar,r'$O_M$',fontsize=16)
    ax.set_xlabel(r'$L_A -- Labor$', fontsize=16)
    ax.set_ylabel('$K_A - Capital$', fontsize=16)
    #plt.show()
    
    
def ppf(LA,Kbar=Kbar, Lbar=Lbar,alpha=alpha,beta=beta):
    """Draw a production possibility frontier
    
    arguments:
    LA -- labor allocated to ag, from which calculate QA(Ka(La),La) 
    """
    fig, ax = plt.subplots(figsize=(6,5))
    KA = edgeworth(LA, Kbar, Lbar,alpha, beta)
    RTS = (alpha/(1-alpha))*(KA/LA)
    QA = F( KA,LA,alpha)
    QM = G(Kbar-KA,Lbar-LA,beta)
    ax.scatter(QA,QM)
    La = np.arange(0,Lbar)
    Ka = edgeworth(La, Kbar, Lbar,alpha, beta)
    Qa = F(Ka,La,alpha)
    Qm = G(Kbar-Ka,Lbar-La,beta)
    ax.set_xlim(0, Lbar)
    ax.set_ylim(0, Kbar)
    ax.plot(Qa, Qm,'k-')
    ax.set_xlabel(r'$Q_A$',fontsize=18)
    ax.set_ylabel(r'$Q_B$',fontsize=18)
    plt.show()
    
    
def wreq(p,a=alpha, b=beta):
    B = ((1-a)/(1-b))*(a/(1-a))**a  * ((1-b)/b)**b
    return B*p

def ssline(a=alpha, b=beta):
    p = np.linspace(0.1,10,100)
    plt.title('The Stolper-Samuelson line')
    plt.xlabel(r'$p = \frac{P_a}{P_m}$', fontsize=18)
    plt.ylabel(r'$ \frac{w}{r}$', fontsize=18)
    plt.plot(p,wreq(p, a, b));