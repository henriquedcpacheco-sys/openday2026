import streamlit as st
import numpy as np
from replicator_game1_simple import generate_matrices, invasion_test

st.set_page_config(page_title="Replicator Game", layout="centered")

st.title("🧬 Replicator Invasion Game")

# =========================
# MATRIZES (fixas)
# =========================
@st.cache_data
def get_matrices():
    return generate_matrices()

A, B, C = get_matrices()

matrix_choice = st.selectbox(
    "Escolhe a matriz:",
    ["A (simétrica)", "B (antissimétrica)", "C (aleatória)"]
)

if "A" in matrix_choice:
    Payoff = A
elif "B" in matrix_choice:
    Payoff = B
else:
    Payoff = C

# =========================
# MOSTRAR MATRIZ
# =========================
st.subheader("Matriz selecionada")
st.dataframe(np.round(Payoff, 2))

# =========================
# SLIDERS
# =========================
st.subheader("Escolhe os traits do invasor")

z1 = st.slider("Trait 1", -1.0, 1.0, 0.3)
z2 = st.slider("Trait 2", -1.0, 1.0, 0.3)

z3 = 1 - z1 - z2

st.write(f"Trait 3 (automático): **{z3:.2f}**")

if z3 < -1 or z3 > 1:
    st.error("⚠️ Valores inválidos!")

# =========================
# BOTÃO
# =========================
if st.button("Testar invasão"):

    result, values = invasion_test(z1, z2, Payoff)

    st.subheader("Resultado")

    if "Conseguiste" in result:
        st.success(result)
    else:
        st.error(result)

    if values:
        f_inv, f_res = values
        st.write(f"Fitness invader: {f_inv:.4f}")
        st.write(f"Fitness resident: {f_res:.4f}")