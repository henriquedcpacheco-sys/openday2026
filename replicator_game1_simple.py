import numpy as np

# =========================
# MATRIZES
# =========================
def generate_matrices(seed=22):
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
# DISPLAY MATRIX
# =========================
def format_matrix(M):
    return "\n".join(
        ["  ".join([f"{val:.2f}" for val in row]) for row in M]
    )

# =========================
# REPLICATOR DYNAMICS
# =========================
def replicator_dynamics(x0, A, T=50, dt=0.01):
    x = x0.copy()

    for _ in range(int(T/dt)):
        fitness = A @ x
        avg = x @ fitness
        dx = x * (fitness - avg)

        x = x + dt * dx

        # evitar problemas numéricos
        x = np.maximum(x, 1e-12)
        x = x / np.sum(x)

    return x


# =========================
# INVASION TEST (COM EQUILÍBRIO)
# =========================
def invasion_test(z1, z2, payoff):

    z3 = 1 - z1 - z2

    # validar intervalo
    if any(v < -1 or v > 1 for v in [z1, z2, z3]):
        return "Valores fora do intervalo!", None

    z = np.array([z1, z2, z3])

    # =========================
    # PASSO 1: dinâmica residentes
    # =========================
    z0 = np.ones(3) / 3
    z_res = replicator_dynamics(z0, payoff)

    # =========================
    # PASSO 2: fitness no equilíbrio
    # =========================
    f_inv = z @ z_res
    f_res = z_res @ payoff @ z_res

    if f_inv > f_res:
        return " Conseguiste invadir!", (f_inv, f_res, z_res)
    else:
        return " Não conseguiste...", (f_inv, f_res, z_res)


# =========================
# MAIN (para testes locais)
# =========================
if __name__ == "__main__":

    A, B, C = generate_matrices()

    print("Escolhe matriz: A, B ou C")
    choice = input(">> ").strip().upper()

    if choice == "A":
        Payoff = A
    elif choice == "B":
        Payoff = B
    else:
        Payoff = C

    print("\nMatriz escolhida:")
    print(format_matrix(Payoff))

    z1 = float(input("\nTrait 1 (-1 a 1): "))
    z2 = float(input("Trait 2 (-1 a 1): "))

    result, values = invasion_test(z1, z2, Payoff)

    print("\nResultado:")
    print(result)

    if values:
        print(f"Fitness invader: {values[0]:.4f}")
        print(f"Fitness resident: {values[1]:.4f}")
