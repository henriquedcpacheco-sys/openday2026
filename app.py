import streamlit as st
from scipy.integrate import solve_ivp
import numpy as np
from replicator_game1_simple import generate_matrices, invasion_test


def replicator_rhs(t, x, A):
    x = np.maximum(x, 1e-12)
    x = x / np.sum(x)

    fitness = A @ x
    avg = x @ fitness

    return x * (fitness - avg)

st.set_page_config(page_title="Replicator Game", layout="centered")

st.title("👾 Invasion Game - Dinâmicas de Curto Prazo")

st.markdown("""
Henrique Pacheco, CEMAT henrique.v.pacheco@tecnico.ulisboa.pt

Erida Gjini, CEMAT erida.gjini@tecnico.ulisboa.pt
""")

st.markdown("""
## O que está a acontecer aqui?

Imagina uma comunidade de espécies (por exemplo bactérias).  
Cada espécie interage com as outras — algumas cooperam, outras competem.

Agora entra um **invasor**   
Será que ele consegue instalar-se no **curto prazo**?

---

## Regra do jogo

Começamos por escolher um tipo de microbioma (se as espécies residentes cooperam, competem ou ambos):
""")
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
st.subheader("Matriz de interações da comunidade residente")
import pandas as pd

df = pd.DataFrame(
    np.round(Payoff, 2),
    index=[1, 2, 3],
    columns=[1, 2, 3]
)

max_val = np.max(np.abs(df.values))

max_val = np.max(np.abs(df.values))

max_val = np.max(np.abs(df.values))

def color_matrix(val):
    if max_val == 0:
        return ''
    
    intensity = abs(val) / max_val
    
    # 🔥 limitar intensidade
    intensity = 0.2 + 0.2*intensity  # entre 0.2 e 0.8

    if val > 0:
        return f'background-color: rgba(255, 0, 0, {intensity})'
    elif val < 0:
        return f'background-color: rgba(0, 0, 255, {intensity})'
    else:
        return 'background-color: white'

styled_df = df.style.map(color_matrix)

st.write(styled_df)

# =========================
# DINÂMICA DOS RESIDENTES
# =========================
x0 = np.ones(3) / 3

sol = solve_ivp(
    lambda t, x: replicator_rhs(t, x, Payoff),
    [0, 20],
    x0,
    t_eval=np.linspace(0, 20, 100)
)

t = sol.t
x = sol.y.T

import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(4, 2))

ax.plot(t, x[:, 0], 'r', label="Espécie 1")
ax.plot(t, x[:, 1], 'g', label="Espécie 2")
ax.plot(t, x[:, 2], 'b', label="Espécie 3")

ax.set_xlabel("Tempo")
ax.set_ylabel("Densidade relativa")
ax.set_title("Dinâmica da comunidade (antes da invasão)")
ax.legend(fontsize=6)

st.pyplot(fig)


## Como calculamos isso?

st.markdown("""A taxa de crescimento do invasor no momento de invasão depende das suas interações com a comunidade:

""")
st.latex(r"""
r_{\text{invader}} = \sum_{j=1}^{N} z_j \lambda^{j}_{\text{inv}}-\bar{\lambda}
""")
st.markdown(r"""
Onde:

- $z_j$ = abundância da espécie $j$ na comunidade  
- $\lambda^{j}_{\text{inv}}$ = fitness do invasor com a espécie $j$  
- $\bar{\lambda} = \sum_{k<j} (\lambda^{j}_{k}+\lambda^{k}_{j}) z_{j}z_{k}$ fitness médio

Isto diz-nos **o crescimento do invasor dentro da comunidade**
""")

st.markdown("""
 O invasor invade se:

**$r_{invader}$ > 0**
""")
# =========================
# FITNESS MÉDIO DA COMUNIDADE
# =========================
z0 = np.ones(3) / 3

from replicator_game1_simple import replicator_dynamics

z_res = replicator_dynamics(z0, Payoff)

f_res = z_res @ Payoff @ z_res

st.write(f"**Fitness médio da comunidade**: {f_res:.4f}")

st.markdown("""
O invasor consegue invadir se tiver **maior fitness** que o médio da comunidade residente.

Ou seja:

- Se o seu fitness é maior que o médio → invade   
- Caso contrário → desaparece   

""")
---
st.markdown("""
## O teu objetivo

Escolhe o vetor de fitness do invasor cuja soma é igual a 1, cujos elementos estão compreendidos entre -1 e 1, e tenta:

 **Invadir a comunidade!**

ou

 Falhar a invasão

---

Move os sliders e testa 
""")


# =========================
# SLIDERS
# =========================
st.subheader("Escolhe o vetor de fitness do invasor (a soma tem de ser 1)")

z1 = st.slider("invasor→1", -1.0, 1.0, 0.3)
z2 = st.slider("invasor→2", -1.0, 1.0, 0.3)

z3 = 1 - z1 - z2

st.write(f"invasor→3 (automático): **{z3:.2f}**")

if z3 < -1 or z3 > 1:
    st.error("⚠️ Valores inválidos!")

# =========================
# BOTÃO
# =========================
if st.button("🚀Testar invasão"):

    result, values = invasion_test(z1, z2, Payoff)

    st.subheader("Resultado")

    if "Conseguiste" in result:
        st.success(result)
    else:
        st.error(result)

    if values:
        f_inv, f_res, z_res = values
        st.write(f"Fitness invader: {f_inv:.4f}")
        st.write(f"Fitness médio: {f_res:.4f}")

