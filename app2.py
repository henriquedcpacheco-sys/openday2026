import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time

from replicator_game2_dynamics import (
    generate_matrices,
    run_dynamics,
    build_traits
)

st.set_page_config(page_title="Replicator Dynamics Game", layout="centered")

st.title("👾 Invasion Game - Dinâmicas de Longo Prazo")

st.markdown("""
Henrique Pacheco, CEMAT henrique.v.pacheco@tecnico.ulisboa.pt  
Erida Gjini, CEMAT erida.gjini@tecnico.ulisboa.pt
""")

st.markdown("""
Agora o jogo é:

1. A comunidade evolui até equilíbrio  
2. O invasor entra com baixa abundância  
3. Vemos a dinâmica completa  

Será que ele consegue instalar-se no **longo prazo**?
""")

st.markdown("""
## Regra do jogo

Agora em vez de escolheres apenas os parâmetros fitness do invasor, terás de escolher também como as espécies residentes reagem 
""")

# =========================
# MATRIZES
# =========================
@st.cache_data
def get_matrices():
    return generate_matrices(seed=22)

A, B, C = get_matrices()

choice = st.selectbox(
    "Escolhe a matriz:",
    ["A (simétrica)", "B (antissimétrica)", "C (aleatória)"]
)

if "A" in choice:
    Payoff = A
elif "B" in choice:
    Payoff = B
else:
    Payoff = C

# =========================
# MOSTRAR MATRIZ
# =========================
import pandas as pd

df = pd.DataFrame(np.round(Payoff, 2), index=[1,2,3], columns=[1,2,3])
st.subheader("Matriz de interações")
st.dataframe(df)

# =========================
# SLIDERS
# =========================
st.subheader("Escolhe os traits de fitness do invasor (linha)")

z1 = st.slider("invasor→1", -1.0, 1.0, 0.2)
z2 = st.slider("invasor→2", -1.0, 1.0, 0.2)
inv = build_traits(z1, z2)

st.write(f"invasor→3: **{inv[2]:.2f}**")

st.subheader("Escolhe como a comunidade reage ao invasor (coluna)")

r1 = st.slider("1→invasor", -1.0, 1.0, 0.4)
r2 = st.slider("2→invasor", -1.0, 1.0, 0.3)
res = build_traits(r1, r2)

st.write(f"3→invasor: **{res[2]:.2f}**")

# =========================
# BOTÃO
# =========================
if st.button("🚀 Simular dinâmica"):

    t1, x1, t2, x2, eq = run_dynamics(inv, res, Payoff)

    st.subheader("Equilíbrio antes da invasão")
    st.write(np.round(eq, 3))

    # =========================
    # PLOT
    # =========================
    fig, ax = plt.subplots(figsize=(5, 3))

    ax.set_xlim(0, max(t1) + max(t2))
    ax.set_ylim(0, 1)

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Densidade")

    # 🔥 linha de invasão
    t_invasion = max(t1)
    ax.axvline(
        x=t_invasion,
        linestyle='--',
        linewidth=2,
        color='black',
        label="Invasão"
    )

    # linhas
    line1, = ax.plot([], [], 'r', label="Res1")
    line2, = ax.plot([], [], 'g', label="Res2")
    line3, = ax.plot([], [], 'b', label="Res3")
    line4, = ax.plot([], [], 'k', label="Invader")

    ax.legend(fontsize=7, frameon=False)

    plot_placeholder = st.pyplot(fig)

    # =========================
    # FASE 1
    # =========================
    for k in range(len(t1)):
        line1.set_data(t1[:k], x1[:k, 0])
        line2.set_data(t1[:k], x1[:k, 1])
        line3.set_data(t1[:k], x1[:k, 2])

        plot_placeholder.pyplot(fig)
        time.sleep(0.01)

    # =========================
    # FASE 2
    # =========================
    t_shift = t2 + max(t1)

    for k in range(len(t2)):

        line1.set_data(
            np.concatenate([t1, t_shift[:k]]),
            np.concatenate([x1[:, 0], x2[:k, 0]])
        )

        line2.set_data(
            np.concatenate([t1, t_shift[:k]]),
            np.concatenate([x1[:, 1], x2[:k, 1]])
        )

        line3.set_data(
            np.concatenate([t1, t_shift[:k]]),
            np.concatenate([x1[:, 2], x2[:k, 2]])
        )

        line4.set_data(
            t_shift[:k],
            x2[:k, 3]
        )

        plot_placeholder.pyplot(fig)
        time.sleep(0.01)

    # =========================
    # RESULTADO
    # =========================
    final_inv = x2[-1, 3]

    if final_inv > 1e-4:
        st.success("O invasor instalou-se!")
    else:
        st.error("O invasor falhou!")
