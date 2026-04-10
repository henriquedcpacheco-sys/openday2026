import streamlit as st
import numpy as np
from replicator_game1_simple import generate_matrices, invasion_test

st.set_page_config(page_title="Replicator Game", layout="centered")

st.title("👾 Replicator Invasion Game")
st.markdown("""
## O que está a acontecer aqui?

Imagina uma comunidade de espécies (por exemplo bactérias).  
Cada espécie interage com as outras — algumas cooperam, outras competem.

Agora entra um **invasor**   
Será que ele consegue instalar-se?

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
st.subheader("Matriz de interações")
import pandas as pd

df = pd.DataFrame(
    np.round(Payoff, 2),
    index=[1, 2, 3],
    columns=[1, 2, 3]
)

st.dataframe(df)

# =========================
# FITNESS MÉDIO DA COMUNIDADE
# =========================
z0 = np.ones(3) / 3

from replicator_game1_simple import replicator_dynamics

z_res = replicator_dynamics(z0, Payoff)

f_res = z_res @ Payoff @ z_res

st.subheader("Fitness médio da comunidade")
st.write(f"Valor: **{f_res:.4f}**")
st.markdown("""
O invasor consegue invadir se tiver **maior fitness** que o médio da comunidade residente.

Ou seja:

- Se o seu fitness é maior que o médio → invade   
- Caso contrário → desaparece   

---
""")
## Como calculamos isso?

A taxa de crescimento do invasor depende das interações com a comunidade:

""")
st.latex(r"""
r_{\text{invader}} = \sum_{j=1}^{N} z_j \lambda^{j}_{\text{inv}}-\bar{\lambda}
""")
st.markdown(r"""
Onde:

- $z_j$ = abundância da espécie $j$ na comunidade  
- $\lambda^{j}_{\text{inv}}$ = fitness do invasor com a espécie $j$  
- $\bar{\lambda} = \sum_{k<j} (\lambda^{j}_{k}+\lambda^{k}_{j}) z_{j}z_{k}$

Isto diz-nos **o crescimento do invasor dentro da comunidade**
""")

st.markdown("""
 O invasor invade se:

**$r_{invader}$ > 0**

---

## O teu objetivo

Escolhe os traits do invasor cuja soma é igual a 1, compreendidos entre -1 e 1, e tenta:

 **Invadir a comunidade!**

ou

 Falhar a invasão

---

Move os sliders e testa 
""")


# =========================
# SLIDERS
# =========================
st.subheader("Escolhe os traits do invasor (a soma tem de ser 1)")

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
        f_inv, f_res, z_res = values
        st.write(f"Fitness invader: {f_inv:.4f}")
        st.write(f"Fitness médio: {f_res:.4f}")
