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
    st.markdown("ℹ️ Nesta secção, o utilizador descreve o caso que pretende analisar, introduzindo os dados disponíveis e o contexto observado.")

    st.markdown("### Dados AIS/VMS")

    st.markdown("**Posição/Trajetória**")
    st.markdown("ℹ️ Informação sobre o percurso observado da embarcação. Deve indicar se a trajetória parece normal ou suspeita.")
    posicao = st.selectbox(
        "Selecione a avaliação da posição/trajetória",
        ["Normal", "Ligeiramente suspeita", "Muito suspeita"],
        label_visibility="collapsed"
    )

    st.markdown("**Velocidade/Curso**")
    st.markdown("ℹ️ Avaliação da coerência da velocidade e da direção da embarcação ao longo do tempo.")
    velocidade = st.selectbox(
        "Selecione a avaliação da velocidade/curso",
        ["Normal", "Ligeiramente suspeito", "Muito suspeito"],
        label_visibility="collapsed"
    )

    st.markdown("### Saídas dos detetores")

    st.markdown("**Nível de alerta do detetor**")
    st.markdown("ℹ️ Classificação qualitativa do alerta gerado pelo sistema automático. Indica se o caso parece pouco, moderadamente ou muito suspeito.")
    alerta = st.selectbox(
        "Selecione o nível de alerta do detetor",
        ["Sem alerta", "Alerta moderado", "Alerta elevado"],
        label_visibility="collapsed"
    )

    st.markdown("**Pontuação do detetor**")
    st.markdown("ℹ️ Valor numérico associado ao grau de suspeita identificado pelo detetor. Quanto maior a pontuação, maior a suspeita.")
    pontuacao_detetor = st.slider(
        "Selecione a pontuação do detetor",
        0, 100, 50,
        label_visibility="collapsed"
    )

    st.markdown("### Outras fontes")

    st.markdown("**Concordância com radar/outras fontes**")
    st.markdown("ℹ️ Indica se outras fontes de informação confirmam ou contradizem os dados principais observados.")
    radar = st.selectbox(
        "Selecione a concordância com radar/outras fontes",
        ["Concordante", "Parcialmente discordante", "Discordante"],
        label_visibility="collapsed"
    )

    st.markdown("**Contexto operacional**")
    st.markdown("ℹ️ Representa se a situação observada é normal ou invulgar no contexto operacional em análise.")
    contexto = st.selectbox(
        "Selecione o contexto operacional",
        ["Normal", "Pouco habitual", "Muito suspeito"],
        label_visibility="collapsed"
    )

with coluna2:
    st.subheader("2. Indicadores de validação")
    st.markdown("ℹ️ Nesta secção, o utilizador avalia os principais indicadores que ajudam o sistema a interpretar a situação e a propor uma recomendação.")

    st.markdown("**I1 - Anomalia de identidade**")
    st.markdown("ℹ️ Avalia se existem sinais de inconsistência na identificação da embarcação.")
    i1 = st.selectbox(
        "Selecione o nível de I1",
        ["Baixo", "Médio", "Elevado"],
        label_visibility="collapsed"
    )

    st.markdown("**I2 - Alteração anormal de identidade**")
    st.markdown("ℹ️ Avalia mudanças inesperadas ou incoerentes nos elementos de identidade.")
    i2 = st.selectbox(
        "Selecione o nível de I2",
        ["Baixo", "Médio", "Elevado"],
        label_visibility="collapsed"
    )

    st.markdown("**I3 - Plausibilidade cinemática**")
    st.markdown("ℹ️ Verifica se o comportamento do movimento da embarcação é fisicamente plausível.")
    i3 = st.selectbox(
        "Selecione o nível de I3",
        ["Baixo", "Médio", "Elevado"],
        label_visibility="collapsed"
    )

    st.markdown("**I4 - Consistência espaço-temporal**")
    st.markdown("ℹ️ Verifica se a evolução da posição e do tempo faz sentido de forma coerente.")
    i4 = st.selectbox(
        "Selecione o nível de I4",
        ["Baixo", "Médio", "Elevado"],
        label_visibility="collapsed"
    )

    st.markdown("**I5 - Consistência contextual**")
    st.markdown("ℹ️ Analisa se o comportamento observado é coerente com o contexto operacional.")
    i5 = st.selectbox(
        "Selecione o nível de I5",
        ["Baixo", "Médio", "Elevado"],
        label_visibility="collapsed"
    )

    st.markdown("**I6 - Consistência entre fontes**")
    st.markdown("ℹ️ Avalia se diferentes fontes de informação apresentam uma interpretação consistente do caso.")
    i6 = st.selectbox(
        "Selecione o nível de I6",
        ["Baixo", "Médio", "Elevado"],
        label_visibility="collapsed"
    )

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
    st.markdown("ℹ️ O sistema agrega os indicadores selecionados, calcula uma pontuação total e propõe uma ação inicial.")

    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Pontuação total", pontuacao_total)
        st.markdown("ℹ️ Resultado agregado da avaliação dos indicadores.")

    with c2:
        st.metric("Nível de risco", risco)
        st.markdown("ℹ️ Classificação global do risco com base na pontuação obtida.")

    with c3:
        st.metric("Ação proposta", acao)
        st.markdown("ℹ️ Recomendação inicial gerada pelo sistema para apoiar a decisão humana.")

    if acao == "Escalar":
        st.error(f"Ação recomendada: {acao}")
    elif acao == "Monitorizar":
        st.warning(f"Ação recomendada: {acao}")
    else:
        st.success(f"Ação recomendada: {acao}")

    st.subheader("4. Evidência e rastreabilidade")
    st.markdown("ℹ️ Esta secção mostra como a decisão foi construída, indicando os contributos de cada indicador e os principais fatores que influenciaram a recomendação.")

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
    st.markdown("ℹ️ O utilizador analisa a recomendação do sistema e pode confirmá-la ou alterá-la com base na evidência apresentada.")

    st.markdown("**Decisão final do utilizador**")
    st.markdown("ℹ️ Permite ao utilizador confirmar ou alterar a recomendação proposta pelo sistema.")
    decisao_utilizador = st.selectbox(
        "Selecione a decisão final do utilizador",
        ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"],
        label_visibility="collapsed"
    )

    st.markdown("**Justificação da decisão final**")
    st.markdown("ℹ️ Campo destinado à justificação da decisão final tomada pelo utilizador.")
    justificacao = st.text_area(
        "Introduza a justificação da decisão final",
        placeholder="Explica por que motivo confirmas ou alteras a ação proposta...",
        label_visibility="collapsed"
    )

    if st.button("Guardar decisão final"):
        decisao_final = acao if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador

        st.divider()
        st.subheader("6. Decisão final justificada")
        st.markdown("ℹ️ Nesta secção é apresentado o registo final da decisão, incluindo a recomendação do sistema, a decisão do utilizador e a respetiva justificação.")

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
