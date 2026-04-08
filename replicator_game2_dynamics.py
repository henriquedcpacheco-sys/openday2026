import numpy as np
from scipy.integrate import solve_ivp

# =========================
# MATRIZES
# =========================
def generate_matrices(seed=2):
    np.random.seed(seed)

    # A simétrica
    M = np.random.rand(3, 3)
    A = (M + M.T) / 2
    np.fill_diagonal(A, 0)

    # B antissimétrica
    M = np.random.rand(3, 3)
    B = M - M.T
    np.fill_diagonal(B, 0)

    # C aleatória [-1,1]
    C = 2 * np.random.rand(3, 3) - 1
    np.fill_diagonal(C, 0)

    return A, B, C


# =========================
# REPLICATOR RHS
# =========================
def replicator_rhs(t, x, A, theta=1):

    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)

    fitness = A @ x
    avg = x @ fitness

    dx = theta * x * (fitness - avg)

    return dx


# =========================
# SIMULAÇÃO
# =========================
def run_dynamics(inv, res, payoff, theta=1):

    # =========================
    # FASE 1: residentes
    # =========================
    x0 = np.ones(3) / 3

    sol1 = solve_ivp(
        lambda t, x: replicator_rhs(t, x, payoff, theta),
        [0, 100],
        x0,
        t_eval=np.linspace(0, 100, 50)
    )

    t1 = sol1.t
    x1 = sol1.y.T

    eq = x1[-1]

    # =========================
    # FASE 2: invasão
    # =========================
    eps = 1e-4

    x_init4 = np.zeros(4)
    x_init4[:3] = eq * (1 - eps)
    x_init4[3] = eps

    x_init4 = x_init4 / np.sum(x_init4)

    # matriz 4x4
    A4 = np.zeros((4, 4))
    A4[:3, :3] = payoff

    A4[3, :3] = inv
    A4[:3, 3] = res

    # simulação
    sol2 = solve_ivp(
        lambda t, x: replicator_rhs(t, x, A4, theta),
        [0, 500],
        x_init4,
        t_eval=np.linspace(0, 400, 75)
    )

    t2 = sol2.t
    x2 = sol2.y.T

    return t1, x1, t2, x2, eq


# =========================
# HELPERS (traits)
# =========================
def build_traits(z1, z2):
    z3 = 1 - z1 - z2
    return np.array([z1, z2, z3])
