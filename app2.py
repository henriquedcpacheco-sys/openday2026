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

st.title("🧬 Replicator Dynamics — Invasion Game")

st.markdown("""
Agora o jogo é:

1. A comunidade evolui até equilíbrio  
2. O invasor entra com baixa abundância  
3. Vemos a dinâmica completa  

Será que ele consegue instalar-se?
""")

# =========================
# MATRIZES
# =========================
@st.cache_data
def get_matrices():
    return generate_matrices()

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

# mostrar matriz bonita
import pandas as pd
df = pd.DataFrame(np.round(Payoff, 2), index=[1,2,3], columns=[1,2,3])
st.subheader("Matriz de interações")
st.dataframe(df)

# =========================
# SLIDERS
# =========================
st.subheader("Escolhe os traits de fitness do invasor (linha)")

z1 = st.slider("Invader trait 1", -1.0, 1.0, 0.2)
z2 = st.slider("Invader trait 2", -1.0, 1.0, 0.2)
inv = build_traits(z1, z2)

st.write(f"Trait 3: **{inv[2]:.2f}**")

st.subheader(" Escolhe como a comunidade reage ao invasor (coluna)")

r1 = st.slider("Resident response 1", -1.0, 1.0, 0.4)
r2 = st.slider("Resident response 2", -1.0, 1.0, 0.3)
res = build_traits(r1, r2)

st.write(f"Response 3: **{res[2]:.2f}**")

# =========================
# BOTÃO
# =========================
if st.button(" Simular dinâmica"):

    # correr simulação
    t1, x1, t2, x2, eq = run_dynamics(inv, res, Payoff)

    st.subheader("Equilíbrio antes da invasão")
    st.write(np.round(eq, 3))

    # =========================
    # PLOT ANIMADO
    # =========================
    fig, ax = plt.subplots()

    ax.set_xlim(0, max(t1)+max(t2))
    ax.set_ylim(0, 1)

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Densidade")

    line1, = ax.plot([], [], 'r', label="Res1")
    line2, = ax.plot([], [], 'g', label="Res2")
    line3, = ax.plot([], [], 'b', label="Res3")
    line4, = ax.plot([], [], 'k', label="Invader")

    ax.legend()

    plot_placeholder = st.pyplot(fig)

    # =========================
    # FASE 1 (pré-invasão)
    # =========================
    for k in range(len(t1)):
        line1.set_data(t1[:k], x1[:k, 0])
        line2.set_data(t1[:k], x1[:k, 1])
        line3.set_data(t1[:k], x1[:k, 2])

        plot_placeholder.pyplot(fig)
        time.sleep(0.02)

    # =========================
    # FASE 2 (com invasor)
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
        time.sleep(0.02)

    # =========================
    # RESULTADO FINAL
    # =========================
    final_inv = x2[-1, 3]

    if final_inv > 1e-4:
        st.success(" O invasor instalou-se!")
    else:
        st.error(" O invasor falhou!")
