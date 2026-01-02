# -*- coding: utf-8 -*-

"""
Heckscher-Ohlin-Samuelson (HOS) International Trade Model

This module implements the two-sector, two-factor HOS model of international trade,
demonstrating factor price equalization, Stolper-Samuelson effects, and the
Rybczynski theorem.

Created on Mon Oct 3 2019 16:08:57:01 2019
@author: jconning
Refactored: 2026-01-02 - Separated computation from visualization
"""

from typing import Dict, Tuple, Optional
from dataclasses import dataclass
import numpy as np
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed


# ============================================================================
# Model Parameters
# ============================================================================

@dataclass
class HOSParams:
    """Parameters for the HOS model.

    Attributes:
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A (agriculture)
        beta: Capital share in sector M (manufacturing)
        theta: Consumption share parameter for utility
    """
    Kbar: float = 100.0
    Lbar: float = 100.0
    alpha: float = 0.6
    beta: float = 0.4
    theta: float = 0.5

    def __post_init__(self):
        """Validate parameters."""
        if not 0 < self.alpha < 1:
            raise ValueError(f"alpha must be in (0,1), got {self.alpha}")
        if not 0 < self.beta < 1:
            raise ValueError(f"beta must be in (0,1), got {self.beta}")
        if abs(self.alpha - self.beta) < 1e-10:
            raise ValueError("alpha and beta must differ for HOS model")
        if self.Kbar <= 0 or self.Lbar <= 0:
            raise ValueError("Endowments must be positive")


# Default parameters for backward compatibility
DEFAULT_PARAMS = HOSParams()

# Legacy global variables for backward compatibility
Kbar = DEFAULT_PARAMS.Kbar
Lbar = DEFAULT_PARAMS.Lbar
alpha = DEFAULT_PARAMS.alpha
beta = DEFAULT_PARAMS.beta
theta = DEFAULT_PARAMS.theta


# ============================================================================
# Production and Utility Functions
# ============================================================================

def F(K: float, L: float, alpha: float = alpha) -> float:
    """Cobb-Douglas production function for sector A.

    Args:
        K: Capital input
        L: Labor input
        alpha: Capital share

    Returns:
        Output quantity
    """
    return K**alpha * L**(1-alpha)


def G(K: float, L: float, beta: float = beta) -> float:
    """Cobb-Douglas production function for sector M.

    Args:
        K: Capital input
        L: Labor input
        beta: Capital share

    Returns:
        Output quantity
    """
    return K**beta * L**(1-beta)


def U(Ca: float, Cm: float, theta: float = theta) -> float:
    """Cobb-Douglas utility function.

    Args:
        Ca: Consumption of good A
        Cm: Consumption of good M
        theta: Preference parameter

    Returns:
        Utility level
    """
    return Ca**theta * Cm**(1-theta)


# ============================================================================
# Factor Intensity and Factor Price Functions
# ============================================================================

def kl_ratio(wr: float, kshare: float) -> float:
    """Calculate optimal capital-labor ratio given factor prices.

    Args:
        wr: Wage-rental ratio (w/r)
        kshare: Capital share in production

    Returns:
        Optimal K/L ratio
    """
    return (kshare / (1 - kshare)) * wr


def stolper_samuelson(p: float, alpha: float, beta: float) -> float:
    """Calculate equilibrium wage-rental ratio from Stolper-Samuelson theorem.

    Args:
        p: Relative price (Pa/Pm)
        alpha: Capital share in sector A
        beta: Capital share in sector M

    Returns:
        Equilibrium wage-rental ratio (w/r)
    """
    Za = alpha**alpha * (1-alpha)**(1-alpha)
    Zm = beta**beta * (1-beta)**(1-beta)
    return (p * (Za / Zm))**(1 / (alpha - beta))


def wage_rental_from_price(p: float, a: float = alpha, b: float = beta) -> float:
    """Calculate wage-rental ratio from price (alternative formulation).

    Args:
        p: Relative price (Pa/Pm)
        a: Capital share in sector A
        b: Capital share in sector M

    Returns:
        Equilibrium wage-rental ratio (w/r)
    """
    B = ((1-a)/(1-b)) * (a/(1-a))**a * ((1-b)/b)**b
    return B * p**(1/(b-a))


# ============================================================================
# Equilibrium Calculations
# ============================================================================

def calculate_hos_equilibrium(p: float, Kbar: float = Kbar, Lbar: float = Lbar,
                              alpha: float = alpha, beta: float = beta) -> Dict[str, float]:
    """Calculate HOS equilibrium allocations and outputs.

    Args:
        p: Relative price (Pa/Pm)
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A
        beta: Capital share in sector M

    Returns:
        Dictionary containing:
            - LA, KA: Labor and capital in sector A
            - LM, KM: Labor and capital in sector M
            - QA, QM: Output quantities
            - wr: Wage-rental ratio
            - ka_ratio, km_ratio: K/L ratios by sector
    """
    # Calculate equilibrium factor prices
    wr = stolper_samuelson(p, alpha, beta)
    ka = kl_ratio(wr, alpha)
    km = kl_ratio(wr, beta)

    # Calculate factor allocations
    LA = (Kbar - km * Lbar) / (ka - km)
    KA = ka * LA
    LM = Lbar - LA
    KM = Kbar - KA

    # Calculate outputs
    QA = F(KA, LA, alpha)
    QM = G(KM, LM, beta)

    return {
        'LA': LA, 'KA': KA,
        'LM': LM, 'KM': KM,
        'QA': QA, 'QM': QM,
        'wr': wr,
        'ka_ratio': ka,
        'km_ratio': km
    }


def edgeworth_locus(L: np.ndarray, Kbar: float = Kbar, Lbar: float = Lbar,
                    alpha: float = alpha, beta: float = beta) -> np.ndarray:
    """Calculate efficiency locus in Edgeworth box.

    Args:
        L: Labor allocation to sector A (can be array)
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A
        beta: Capital share in sector M

    Returns:
        Capital allocation to sector A along efficiency locus
    """
    A = (beta * (1 - alpha)) / (alpha * (1 - beta))
    return (L * Kbar) / (A * (Lbar - L) + L)


def isoquant_K(L: np.ndarray, kshare: float, qbar: float) -> np.ndarray:
    """Calculate capital for a given isoquant.

    Args:
        L: Labor input (can be array)
        kshare: Capital share
        qbar: Output level

    Returns:
        Capital required for given L to produce qbar
    """
    return (qbar / (L**(1 - kshare)))**(1 / kshare)


def indifference_curve(Cm: np.ndarray, theta: float, ubar: float) -> np.ndarray:
    """Calculate Ca for given utility level.

    Args:
        Cm: Consumption of good M (can be array)
        theta: Preference parameter
        ubar: Utility level

    Returns:
        Consumption of good A for given utility
    """
    return (ubar / (Cm**(1 - theta)))**(1 / theta)


def calculate_ppf(Kbar: float = Kbar, Lbar: float = Lbar,
                  alpha: float = alpha, beta: float = beta,
                  n_points: int = 100) -> Tuple[np.ndarray, np.ndarray]:
    """Calculate production possibility frontier.

    Args:
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A
        beta: Capital share in sector M
        n_points: Number of points to calculate

    Returns:
        Tuple of (QA, QM) arrays along the PPF
    """
    La = np.linspace(0.1, Lbar - 0.1, n_points)
    Ka = edgeworth_locus(La, Kbar, Lbar, alpha, beta)
    Qa = F(Ka, La, alpha)
    Qm = G(Kbar - Ka, Lbar - La, beta)

    return Qa, Qm


def optimize_closed_economy(alpha: float = alpha, beta: float = beta,
                            theta: float = theta, Kbar: float = Kbar,
                            Lbar: float = Lbar) -> Dict[str, float]:
    """Find autarky equilibrium (utility maximization subject to PPF).

    Args:
        alpha: Capital share in sector A
        beta: Capital share in sector M
        theta: Consumption preference parameter
        Kbar: Total capital endowment
        Lbar: Total labor endowment

    Returns:
        Dictionary with optimal QA, QM, utility, and allocations
    """
    def objective(X):
        """Negative utility for minimization."""
        Ka, La = X[0], X[1]
        Ca = F(Ka, La, alpha)
        Cm = G(Kbar - Ka, Lbar - La, beta)
        return -U(Ca, Cm, theta)

    # Initial guess
    x0 = [Kbar / 2, Lbar / 2]

    # Solve
    result = minimize(objective, x0, method='Nelder-Mead')

    if not result.success:
        raise RuntimeError(f"Optimization failed: {result.message}")

    Kae, Lae = result.x
    Qae = F(Kae, Lae, alpha)
    Qme = G(Kbar - Kae, Lbar - Lae, beta)
    Ue = U(Qae, Qme, theta)

    return {
        'QA': Qae, 'QM': Qme,
        'KA': Kae, 'LA': Lae,
        'utility': Ue
    }


def calculate_lerner_diagram(p: float, QM_fixed: float = 30,
                             alpha: float = alpha, beta: float = beta,
                             Kbar: float = Kbar, Lbar: float = Lbar) -> Dict[str, float]:
    """Calculate quantities for Lerner diagram.

    Args:
        p: Relative price (Pa/Pm)
        QM_fixed: Fixed quantity of M for isoquant
        alpha: Capital share in sector A
        beta: Capital share in sector M
        Kbar: Total capital endowment
        Lbar: Total labor endowment

    Returns:
        Dictionary with allocations, outputs, and factor intensities
    """
    wr = stolper_samuelson(p, alpha, beta)
    Kas = kl_ratio(wr, alpha)
    Kms = kl_ratio(wr, beta)

    # Calculate quantities on isoquants
    Lm_iso = (QM_fixed / Kms**beta)**(1 / (1 - beta))
    Km_iso = Kms * Lm_iso

    QA_val = p * QM_fixed
    La_iso = (QA_val / Kas**alpha)**(1 / (1 - alpha))
    Ka_iso = Kas * La_iso

    # Isocost line
    I = Km_iso + wr * Lm_iso

    return {
        'wr': wr, 'KLa': Kas, 'KLm': Kms,
        'Lm_iso': Lm_iso, 'Km_iso': Km_iso,
        'La_iso': La_iso, 'Ka_iso': Ka_iso,
        'QM': QM_fixed, 'QA': QA_val,
        'isocost_intercept': I
    }


# ============================================================================
# Visualization Functions
# ============================================================================

def setup_plot_style():
    """Configure matplotlib style for HOS plots."""
    plt.style.use('seaborn-v0_8-colorblind')
    plt.rcParams.update({
        "figure.figsize": (10, 6),
        "axes.spines.right": True,
        "axes.spines.top": False,
        "font.size": 18,
        "axes.grid": True
    })


def plot_factor_intensity(KL_ratio: float, alpha: float = alpha, beta: float = beta):
    """Plot factor intensity curves for both sectors.

    Args:
        KL_ratio: Overall K/L ratio to mark
        alpha: Capital share in sector A
        beta: Capital share in sector M
    """
    wr = np.linspace(0, 10, 100)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlabel(r'$K/L$')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.set_ylabel(r'$w/r$ -- wage-rental')
    ax.plot(kl_ratio(wr, alpha), wr, linewidth=4, label='Sector A')
    ax.plot(kl_ratio(wr, beta), wr, linewidth=4, label='Sector M')
    ax.axvline(KL_ratio, linestyle='--', color='gray')
    ax.text(KL_ratio + 0.5, 9, r'$\bar{K}/\bar{L}$')
    ax.legend()
    ax.set_aspect('equal')
    plt.tight_layout()


def plot_stolper_samuelson(p: float, alpha: float = alpha, beta: float = beta):
    """Plot Stolper-Samuelson relationship.

    Args:
        p: Current relative price to highlight
        alpha: Capital share in sector A
        beta: Capital share in sector M
    """
    wr = stolper_samuelson(p, alpha, beta)
    pp = np.linspace(0.2, 2, 100)
    wr_curve = stolper_samuelson(pp, alpha, beta)

    fig, ax = plt.subplots()
    ax.plot(pp, wr_curve, 'b', linewidth=2)
    ax.axhline(y=wr, color='gray', linestyle='--', alpha=0.7)
    ax.axvline(x=p, color='gray', linestyle='--', alpha=0.7)
    ax.scatter(p, wr, s=100, c='red', zorder=5)
    ax.set_ylabel(r'$w/r$')
    ax.set_xlabel(r'$p = P_a/P_m$')
    ax.set_ylim(0, 6)
    ax.set_title('Stolper-Samuelson Relationship')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    print(f"p = {p:.2f}, w/r = {wr:.2f}")


def plot_lerner_diagram(p: float, QM_fixed: float = 30,
                        alpha: float = alpha, beta: float = beta,
                        Kbar: float = Kbar, Lbar: float = Lbar):
    """Plot Lerner diagram showing factor intensity and isoquants.

    Args:
        p: Relative price
        QM_fixed: Fixed quantity of M for reference
        alpha: Capital share in sector A
        beta: Capital share in sector M
        Kbar: Total capital endowment
        Lbar: Total labor endowment
    """
    results = calculate_lerner_diagram(p, QM_fixed, alpha, beta, Kbar, Lbar)

    ll = np.linspace(0.1, Lbar, 100)
    ll_ = np.linspace(0.05 * Lbar, 0.80 * Lbar, 100)

    fig, ax = plt.subplots(figsize=(10, 10))

    # Factor intensity rays
    ax.plot(ll, results['KLa'] * ll, ':', label=f"K/L (A) = {results['KLa']:.2f}")
    ax.plot(ll, results['KLm'] * ll, ':', label=f"K/L (M) = {results['KLm']:.2f}")

    # Isoquants
    ax.plot(ll_, isoquant_K(ll_, beta, QM_fixed), 'b', linewidth=2,
            label=f"Qm = {QM_fixed}")
    ax.plot(ll_, isoquant_K(ll_, alpha, results['QA']), 'g', linewidth=2,
            label=f"Qa = {results['QA']:.1f}")

    # Isocost line
    ax.plot(ll, results['isocost_intercept'] - results['wr'] * ll, 'r:',
            linewidth=2, label='Isocost')

    # Optimal points
    ax.scatter(results['Lm_iso'], results['Km_iso'], s=100, c='blue', zorder=5)
    ax.scatter(results['La_iso'], results['Ka_iso'], s=100, c='green', zorder=5)

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.set_xlabel('L - labor')
    ax.set_ylabel('K - capital')
    ax.set_title(f'Lerner Diagram\nw/r = {results["wr"]:.2f}, '
                 f'Ka/La = {results["KLa"]:.2f}, Km/Lm = {results["KLm"]:.2f}')
    ax.legend()
    ax.set_aspect('equal')
    plt.tight_layout()

    print(f'w/r = {results["wr"]:2.2f}, KLa = {results["KLa"]:2.2f}, KLm = {results["KLm"]:2.2f}')


def plot_edgeworth_box(LA: float, Kbar: float = Kbar, Lbar: float = Lbar,
                       alpha: float = alpha, beta: float = beta):
    """Plot Edgeworth box with efficiency locus and isoquants.

    Args:
        LA: Labor allocation to sector A
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A
        beta: Capital share in sector M
    """
    KA = edgeworth_locus(LA, Kbar, Lbar, alpha, beta)
    RTS = (alpha / (1 - alpha)) * (KA / LA)
    QA = F(KA, LA, alpha)
    QM = G(Kbar - KA, Lbar - LA, beta)

    print(f"(LA, KA) = ({LA:4.1f}, {KA:4.1f})  "
          f"(QA, QM) = ({QA:4.1f}, {QM:4.1f})  RTS = {RTS:4.1f}")

    La = np.linspace(1, Lbar - 1, 100)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.set_xlim(0, Lbar)
    ax.set_ylim(0, Kbar)

    # Efficiency locus
    ax.plot(La, edgeworth_locus(La, Kbar, Lbar, alpha, beta), 'k-', linewidth=2)

    # Isoquants
    ax.plot(La, isoquant_K(La, alpha, QA), 'b-')
    ax.plot(La, Kbar - isoquant_K(Lbar - La, beta, QM), 'g-')

    # Current allocation
    ax.plot(LA, KA, 'ro', markersize=10)
    ax.vlines(LA, 0, KA, linestyles="dashed", alpha=0.5)
    ax.hlines(KA, 0, LA, linestyles="dashed", alpha=0.5)

    # Origin labels
    ax.text(-6, -6, r'$O_A$', fontsize=16)
    ax.text(Lbar - 3, Kbar + 3, r'$O_M$', fontsize=16)

    ax.set_xlabel(r'$L_A$ - Labor in A', fontsize=16)
    ax.set_ylabel(r'$K_A$ - Capital in A', fontsize=16)
    plt.tight_layout()


def plot_ppf(LA: float, Kbar: float = Kbar, Lbar: float = Lbar,
             alpha: float = alpha, beta: float = beta):
    """Plot production possibility frontier.

    Args:
        LA: Labor allocation to sector A (point to highlight)
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A
        beta: Capital share in sector M
    """
    KA = edgeworth_locus(LA, Kbar, Lbar, alpha, beta)
    QA = F(KA, LA, alpha)
    QM = G(Kbar - KA, Lbar - LA, beta)

    Qa, Qm = calculate_ppf(Kbar, Lbar, alpha, beta)

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(Qa, Qm, 'k-', linewidth=2, label='PPF')
    ax.scatter(QA, QM, s=100, c='red', zorder=5)
    ax.set_xlim(0, Lbar)
    ax.set_ylim(0, Kbar)
    ax.set_xlabel(r'$Q_A$', fontsize=18)
    ax.set_ylabel(r'$Q_M$', fontsize=18)
    ax.set_title('Production Possibility Frontier')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    plt.tight_layout()


def plot_closed_economy(alpha: float = alpha, beta: float = beta,
                        theta: float = theta, Kbar: float = Kbar,
                        Lbar: float = Lbar):
    """Plot autarky equilibrium on PPF with indifference curve.

    Args:
        alpha: Capital share in sector A
        beta: Capital share in sector M
        theta: Consumption preference parameter
        Kbar: Total capital endowment
        Lbar: Total labor endowment
    """
    # Calculate equilibrium
    eq = optimize_closed_economy(alpha, beta, theta, Kbar, Lbar)

    # Calculate PPF
    Qa, Qm = calculate_ppf(Kbar, Lbar, alpha, beta)

    # Indifference curve
    cm_range = np.linspace(0.1, Lbar, 100)
    ca_indif = indifference_curve(cm_range, theta, eq['utility'])

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.plot(Qm, Qa, 'k-', linewidth=2)
    ax.plot(cm_range, ca_indif, 'b--', linewidth=2)
    ax.scatter(eq['QM'], eq['QA'], s=150, c='red', zorder=5)

    ax.set_ylim(0, 110)
    ax.set_xlim(0, 110)
    ax.set_xlabel(r'$Q_M$', fontsize=18)
    ax.set_ylabel(r'$Q_A$', fontsize=18)
    ax.set_title('Closed Economy Equilibrium')
    ax.set_aspect('equal')
    plt.tight_layout()

    print(f'Autarky: (QA, QM) = ({eq["QA"]:.1f}, {eq["QM"]:.1f})')


def plot_rybczynski(p: float, Kbar: float = Kbar, Lbar: float = Lbar,
                    alpha: float = alpha, beta: float = beta):
    """Plot Rybczynski diagram showing factor allocations.

    Args:
        p: Relative price
        Kbar: Total capital endowment
        Lbar: Total labor endowment
        alpha: Capital share in sector A
        beta: Capital share in sector M
    """
    eq = calculate_hos_equilibrium(p, Kbar, Lbar, alpha, beta)

    ll = np.linspace(0.1, Lbar, 100)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, Lbar)
    ax.set_ylim(0, Kbar)
    ax.set_xlabel('L - Labor')
    ax.set_ylabel('K - Capital')
    ax.spines['top'].set_visible(True)
    ax.spines['right'].set_visible(True)

    # Factor intensity rays
    ax.plot(ll, eq['ka_ratio'] * ll, '--')
    ax.plot(ll, eq['km_ratio'] * ll, '--')

    # Allocations
    ax.scatter(eq['LA'], eq['KA'], s=150, c='blue', zorder=5)
    ax.scatter(eq['LM'], eq['KM'], s=150, c='green', zorder=5)

    # Extension lines from allocation points
    llm_up = np.linspace(eq['LA'], Lbar, 100)
    lla_lo = np.linspace(eq['LM'], Lbar, 100)
    ax.plot(llm_up, (eq['KA'] - eq['km_ratio'] * eq['LA']) + eq['km_ratio'] * llm_up,
            '--', alpha=0.5)
    ax.plot(lla_lo, (eq['KM'] - eq['ka_ratio'] * eq['LM']) + eq['ka_ratio'] * lla_lo,
            '--', alpha=0.5)

    # Text annotations
    ax.text(1.05 * Lbar, 0.95 * Kbar,
            f'p = {p:3.1f}', fontsize=14)
    ax.text(1.05 * Lbar, 0.95 * Kbar - 6,
            f'(LA, KA) = ({eq["LA"]:2.0f}, {eq["KA"]:2.0f})', fontsize=14)
    ax.text(1.05 * Lbar, 0.95 * Kbar - 12,
            f'(LM, KM) = ({eq["LM"]:2.0f}, {eq["KM"]:2.0f})', fontsize=14)
    ax.text(1.05 * Lbar, 0.95 * Kbar - 18,
            f'(QA, QM) = ({eq["QA"]:2.0f}, {eq["QM"]:2.0f})', fontsize=14)

    ax.set_aspect('equal')
    plt.tight_layout()


def plot_ss_line(alpha: float = alpha, beta: float = beta):
    """Plot the Stolper-Samuelson line.

    Args:
        alpha: Capital share in sector A
        beta: Capital share in sector M
    """
    p = np.linspace(0.5, 1.5, 500)
    wr = wage_rental_from_price(p, alpha, beta)

    fig, ax = plt.subplots()
    ax.plot(p, wr, linewidth=2)
    ax.set_title('The Stolper-Samuelson line')
    ax.set_xlabel(r'$p = \frac{P_a}{P_m}$', fontsize=18)
    ax.set_ylabel(r'$\frac{w}{r}$', fontsize=18)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()


# ============================================================================
# Legacy Functions (backward compatibility)
# ============================================================================

def klplot(KL):
    """Legacy function: Plot factor intensity diagram."""
    plot_factor_intensity(KL)


def ssplot(p):
    """Legacy function: Plot Stolper-Samuelson line."""
    plot_stolper_samuelson(p)


def lerner(p):
    """Legacy function: Plot Lerner diagram."""
    plot_lerner_diagram(p)


def edgeplot(LA, Kbar=Kbar, Lbar=Lbar, alpha=alpha, beta=beta):
    """Legacy function: Plot Edgeworth box."""
    plot_edgeworth_box(LA, Kbar, Lbar, alpha, beta)


def ppf(LA, Kbar=Kbar, Lbar=Lbar, alpha=alpha, beta=beta):
    """Legacy function: Plot PPF."""
    plot_ppf(LA, Kbar, Lbar, alpha, beta)


def rybplot(p, Kbar=Kbar, Lbar=Lbar, alpha=alpha, beta=beta):
    """Legacy function: Plot Rybczynski diagram."""
    plot_rybczynski(p, Kbar, Lbar, alpha, beta)


def closed_plot(alpha=alpha, beta=beta):
    """Legacy function: Plot closed economy equilibrium."""
    plot_closed_economy(alpha, beta)


def HOS(p, Kbar=Kbar, Lbar=Lbar, alpha=alpha, beta=beta):
    """Legacy function: Combined HOS plot (Edgeworth box at equilibrium)."""
    eq = calculate_hos_equilibrium(p, Kbar, Lbar, alpha, beta)
    plot_edgeworth_box(eq['LA'], Kbar, Lbar, alpha, beta)


def hos_eq(p, Kbar=Kbar, Lbar=Lbar):
    """Legacy function: Calculate HOS equilibrium."""
    eq = calculate_hos_equilibrium(p, Kbar, Lbar, alpha, beta)
    return eq['LA'], eq['KA']


def num_opt(alpha=alpha, beta=beta):
    """Legacy function: Numerical optimization for closed economy."""
    eq = optimize_closed_economy(alpha, beta)
    return eq['QA'], eq['QM']


def ssline(a=alpha, b=beta):
    """Legacy function: Plot Stolper-Samuelson line."""
    plot_ss_line(a, b)


# Backward compatibility aliases
SS = stolper_samuelson
kl = kl_ratio
isoq = isoquant_K
indif = indifference_curve
edgeworth = edgeworth_locus
wreq = wage_rental_from_price
obj = lambda X, alpha=alpha, beta=beta: -U(F(X[0], X[1], alpha),
                                           G(Kbar-X[0], Lbar-X[1], beta))


# ============================================================================
# Initialize plot style on import
# ============================================================================

setup_plot_style()
