import streamlit as st

st.set_page_config(page_title="Sistema de Validação de Decisão", layout="wide")

st.title("Sistema de Validação de Decisão")
st.write("Protótipo simples para demonstrar um sistema de apoio à decisão com validação humana final.")

# -------------------------
# Funções auxiliares
# -------------------------
def level_to_points(level):
    mapping = {"Low": 0, "Medium": 1, "High": 2}
    return mapping[level]

def risk_label(score):
    if score <= 4:
        return "Green"
    elif score <= 8:
        return "Amber"
    else:
        return "Red"

def proposed_action(score):
    if score <= 4:
        return "Dismiss"
    elif score <= 8:
        return "Monitor"
    else:
        return "Escalate"

# -------------------------
# Layout principal
# -------------------------
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Entradas do sistema")

    st.markdown("**Dados AIS/VMS**")
    posicao = st.selectbox("Posição/Trajetória", ["Normal", "Ligeiramente suspeita", "Muito suspeita"])
    velocidade = st.selectbox("Velocidade/Curso", ["Normal", "Ligeiramente suspeito", "Muito suspeito"])

    st.markdown("**Outputs de detetores**")
    alerta = st.selectbox("Nível de alerta do detetor", ["Sem alerta", "Alerta moderado", "Alerta elevado"])
    score_detector = st.slider("Score do detetor", 0, 100, 50)

    st.markdown("**Outras fontes**")
    radar = st.selectbox("Concordância com radar/outras fontes", ["Concordante", "Parcialmente discordante", "Discordante"])
    contexto = st.selectbox("Contexto operacional", ["Normal", "Pouco habitual", "Muito suspeito"])

with col2:
    st.subheader("2. Indicadores de validação")

    i1 = st.selectbox("I1 - Anomalia de identidade", ["Low", "Medium", "High"])
    i2 = st.selectbox("I2 - Alteração anormal de identidade", ["Low", "Medium", "High"])
    i3 = st.selectbox("I3 - Plausibilidade cinemática", ["Low", "Medium", "High"])
    i4 = st.selectbox("I4 - Consistência espaço-temporal", ["Low", "Medium", "High"])
    i5 = st.selectbox("I5 - Consistência contextual", ["Low", "Medium", "High"])
    i6 = st.selectbox("I6 - Consistência entre fontes", ["Low", "Medium", "High"])

# -------------------------
# Pesos
# -------------------------
weights = {
    "I1": 3,
    "I2": 2,
    "I3": 2,
    "I4": 2,
    "I5": 1,
    "I6": 3
}

# -------------------------
# Cálculo
# -------------------------
if st.button("Gerar recomendação"):

    indicators = {
        "I1": i1,
        "I2": i2,
        "I3": i3,
        "I4": i4,
        "I5": i5,
        "I6": i6
    }

    contributions = {}
    total_score = 0

    for key, value in indicators.items():
        pts = level_to_points(value)
        contrib = pts * weights[key]
        contributions[key] = {
            "level": value,
            "points": pts,
            "weight": weights[key],
            "contribution": contrib
        }
        total_score += contrib

    risk = risk_label(total_score)
    action = proposed_action(total_score)

    st.divider()
    st.subheader("3. Resultado do sistema")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Score total", total_score)
    with c2:
        st.metric("Nível de risco", risk)
    with c3:
        st.metric("Ação proposta", action)

    if action == "Escalate":
        st.error(f"Ação recomendada: {action}")
    elif action == "Monitor":
        st.warning(f"Ação recomendada: {action}")
    else:
        st.success(f"Ação recomendada: {action}")

    st.subheader("4. Evidência e rastreabilidade")

    rows = []
    for ind, data in contributions.items():
        rows.append({
            "Indicador": ind,
            "Nível": data["level"],
            "Pontos": data["points"],
            "Peso": data["weight"],
            "Contributo": data["contribution"]
        })

    st.table(rows)

    # Drivers principais
    ordered = sorted(contributions.items(), key=lambda x: x[1]["contribution"], reverse=True)
    top_drivers = [f"{item[0]} ({item[1]['level']})" for item in ordered[:3]]

    st.markdown("**Principais drivers da decisão:**")
    for driver in top_drivers:
        st.write(f"- {driver}")

    st.markdown("**Resumo da evidência:**")
    st.write(
        f"""
        - Posição/Trajetória: **{posicao}**
        - Velocidade/Curso: **{velocidade}**
        - Alerta do detetor: **{alerta}**
        - Score do detetor: **{score_detector}**
        - Concordância com radar/outras fontes: **{radar}**
        - Contexto operacional: **{contexto}**
        """
    )

    st.subheader("5. Validação humana")

    decisao_utilizador = st.selectbox(
        "Decisão final do utilizador",
        ["Confirmar ação proposta", "Dismiss", "Monitor", "Escalate", "Needs Review"]
    )

    justificacao = st.text_area(
        "Justificação da decisão final",
        placeholder="Explica por que motivo confirmas ou alteras a ação proposta..."
    )

    if st.button("Guardar decisão final"):
        decisao_final = action if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador

        st.divider()
        st.subheader("6. Decisão final justificada")

        st.write(f"**Ação proposta pelo sistema:** {action}")
        st.write(f"**Decisão final do utilizador:** {decisao_final}")
        st.write(f"**Nível de risco:** {risk}")
        st.write(f"**Score total:** {total_score}")

        if justificacao.strip():
            st.write("**Justificação:**")
            st.write(justificacao)
        else:
            st.write("**Justificação:** não fornecida")

        st.info("Registo concluído com recomendação automática + validação humana.")
