import streamlit as st

st.set_page_config(page_title="Sistema de Validação da Decisão", layout="wide")

st.title("Sistema de Validação da Decisão")
st.write("Protótipo simples para demonstrar um sistema de apoio à decisão com validação humana final.")

# -------------------------
# Funções auxiliares
# -------------------------
def nivel_para_pontos(nivel):
    mapeamento = {"Baixo": 0, "Médio": 1, "Elevado": 2}
    return mapeamento[nivel]

def nivel_risco(pontuacao):
    if pontuacao <= 4:
        return "Baixo"
    elif pontuacao <= 8:
        return "Médio"
    else:
        return "Elevado"

def acao_proposta(pontuacao):
    if pontuacao <= 4:
        return "Ignorar"
    elif pontuacao <= 8:
        return "Monitorizar"
    else:
        return "Escalar"

# -------------------------
# Layout principal
# -------------------------
coluna1, coluna2 = st.columns([1, 1])

with coluna1:
    st.subheader("1. Entradas do sistema")

    st.markdown("**Dados AIS/VMS**")
    posicao = st.selectbox("Posição/Trajetória", ["Normal", "Ligeiramente suspeita", "Muito suspeita"])
    velocidade = st.selectbox("Velocidade/Curso", ["Normal", "Ligeiramente suspeito", "Muito suspeito"])

    st.markdown("**Saídas dos detetores**")
    alerta = st.selectbox("Nível de alerta do detetor", ["Sem alerta", "Alerta moderado", "Alerta elevado"])
    pontuacao_detetor = st.slider("Pontuação do detetor", 0, 100, 50)

    st.markdown("**Outras fontes**")
    radar = st.selectbox("Concordância com radar/outras fontes", ["Concordante", "Parcialmente discordante", "Discordante"])
    contexto = st.selectbox("Contexto operacional", ["Normal", "Pouco habitual", "Muito suspeito"])

with coluna2:
    st.subheader("2. Indicadores de validação")

    i1 = st.selectbox("I1 - Anomalia de identidade", ["Baixo", "Médio", "Elevado"])
    i2 = st.selectbox("I2 - Alteração anormal de identidade", ["Baixo", "Médio", "Elevado"])
    i3 = st.selectbox("I3 - Plausibilidade cinemática", ["Baixo", "Médio", "Elevado"])
    i4 = st.selectbox("I4 - Consistência espaço-temporal", ["Baixo", "Médio", "Elevado"])
    i5 = st.selectbox("I5 - Consistência contextual", ["Baixo", "Médio", "Elevado"])
    i6 = st.selectbox("I6 - Consistência entre fontes", ["Baixo", "Médio", "Elevado"])

# -------------------------
# Pesos
# -------------------------
pesos = {
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

    indicadores = {
        "I1": i1,
        "I2": i2,
        "I3": i3,
        "I4": i4,
        "I5": i5,
        "I6": i6
    }

    contributos = {}
    pontuacao_total = 0

    for chave, valor in indicadores.items():
        pontos = nivel_para_pontos(valor)
        contributo = pontos * pesos[chave]
        contributos[chave] = {
            "nivel": valor,
            "pontos": pontos,
            "peso": pesos[chave],
            "contributo": contributo
        }
        pontuacao_total += contributo

    risco = nivel_risco(pontuacao_total)
    acao = acao_proposta(pontuacao_total)

    st.divider()
    st.subheader("3. Resultado do sistema")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pontuação total", pontuacao_total)
    with c2:
        st.metric("Nível de risco", risco)
    with c3:
        st.metric("Ação proposta", acao)

    if acao == "Escalar":
        st.error(f"Ação recomendada: {acao}")
    elif acao == "Monitorizar":
        st.warning(f"Ação recomendada: {acao}")
    else:
        st.success(f"Ação recomendada: {acao}")

    st.subheader("4. Evidência e rastreabilidade")

    linhas = []
    for indicador, dados in contributos.items():
        linhas.append({
            "Indicador": indicador,
            "Nível": dados["nivel"],
            "Pontos": dados["pontos"],
            "Peso": dados["peso"],
            "Contributo": dados["contributo"]
        })

    st.table(linhas)

    # Fatores principais da decisão
    ordenados = sorted(contributos.items(), key=lambda x: x[1]["contributo"], reverse=True)
    principais_fatores = [f"{item[0]} ({item[1]['nivel']})" for item in ordenados[:3]]

    st.markdown("**Principais fatores da decisão:**")
    for fator in principais_fatores:
        st.write(f"- {fator}")

    st.markdown("**Resumo da evidência:**")
    st.write(
        f"""
        - Posição/Trajetória: **{posicao}**
        - Velocidade/Curso: **{velocidade}**
        - Alerta do detetor: **{alerta}**
        - Pontuação do detetor: **{pontuacao_detetor}**
        - Concordância com radar/outras fontes: **{radar}**
        - Contexto operacional: **{contexto}**
        """
    )

    st.subheader("5. Validação humana")

    decisao_utilizador = st.selectbox(
        "Decisão final do utilizador",
        ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"]
    )

    justificacao = st.text_area(
        "Justificação da decisão final",
        placeholder="Explica por que motivo confirmas ou alteras a ação proposta..."
    )

    if st.button("Guardar decisão final"):
        decisao_final = acao if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador

        st.divider()
        st.subheader("6. Decisão final justificada")

        st.write(f"**Ação proposta pelo sistema:** {acao}")
        st.write(f"**Decisão final do utilizador:** {decisao_final}")
        st.write(f"**Nível de risco:** {risco}")
        st.write(f"**Pontuação total:** {pontuacao_total}")

        if justificacao.strip():
            st.write("**Justificação:**")
            st.write(justificacao)
        else:
            st.write("**Justificação:** não fornecida")

        st.info("Registo concluído com recomendação automática e validação humana.")
