import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Sistema de Validação da Decisão",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------
# Estilo visual
# -------------------------
st.markdown("""
<style>
    .bloco {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        border: 1px solid #e9ecef;
        margin-bottom: 20px;
    }
    .bloco-resultado {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #dee2e6;
        margin-top: 10px;
        margin-bottom: 20px;
    }
    .titulo-secao {
        font-size: 1.35rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
        color: #1f2937;
    }
    .subtexto {
        color: #6b7280;
        font-size: 0.95rem;
        margin-bottom: 1rem;
    }
    .etiqueta {
        font-weight: 600;
        margin-top: 8px;
        margin-bottom: 3px;
        color: #1f2937;
    }
    .acao-final {
        padding: 14px;
        border-radius: 12px;
        font-weight: 600;
        text-align: center;
        margin-top: 8px;
        border: 1px solid #d1d5db;
    }
    .caixa-explicacao {
        background-color: #f9fafb;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

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

def cor_risco(risco):
    if risco == "Baixo":
        return "#d1fae5", "#065f46"
    elif risco == "Médio":
        return "#fef3c7", "#92400e"
    return "#fee2e2", "#991b1b"

def calcular_indicadores(posicao, velocidade, radar, contexto):
    if posicao == "Muito suspeita":
        i1 = "Elevado"
    elif posicao == "Ligeiramente suspeita":
        i1 = "Médio"
    else:
        i1 = "Baixo"

    if posicao == "Muito suspeita" and radar == "Discordante":
        i2 = "Elevado"
    elif posicao == "Ligeiramente suspeita" or radar == "Parcialmente discordante":
        i2 = "Médio"
    else:
        i2 = "Baixo"

    if velocidade == "Muito suspeito":
        i3 = "Elevado"
    elif velocidade == "Ligeiramente suspeito":
        i3 = "Médio"
    else:
        i3 = "Baixo"

    if posicao == "Muito suspeita" and velocidade == "Muito suspeito":
        i4 = "Elevado"
    elif posicao == "Ligeiramente suspeita" or velocidade == "Ligeiramente suspeito":
        i4 = "Médio"
    else:
        i4 = "Baixo"

    if contexto == "Muito suspeito":
        i5 = "Elevado"
    elif contexto == "Pouco habitual":
        i5 = "Médio"
    else:
        i5 = "Baixo"

    if radar == "Discordante":
        i6 = "Elevado"
    elif radar == "Parcialmente discordante":
        i6 = "Médio"
    else:
        i6 = "Baixo"

    return {
        "I1": i1,
        "I2": i2,
        "I3": i3,
        "I4": i4,
        "I5": i5,
        "I6": i6
    }

def impacto_textual(contributo):
    if contributo >= 5:
        return "Elevado"
    elif contributo >= 2:
        return "Moderado"
    elif contributo >= 1:
        return "Reduzido"
    return "Muito reduzido"

def gerar_explicacao_decisao(acao, risco, pontuacao_total, fatores):
    nomes = [f["nome"] for f in fatores[:3]]

    if len(nomes) == 1:
        fatores_texto = nomes[0]
    elif len(nomes) == 2:
        fatores_texto = f"{nomes[0]} e {nomes[1]}"
    else:
        fatores_texto = f"{nomes[0]}, {nomes[1]} e {nomes[2]}"

    return (
        f"A recomendação de **{acao.lower()}** foi gerada porque a pontuação total foi "
        f"**{pontuacao_total}**, correspondendo a um nível de risco **{risco.lower()}**. "
        f"Os fatores que mais contribuíram para esta decisão foram **{fatores_texto}**."
    )

nomes_indicadores = {
    "I1": "Anomalia de identidade",
    "I2": "Alteração anormal de identidade",
    "I3": "Plausibilidade cinemática",
    "I4": "Consistência espaço-temporal",
    "I5": "Consistência contextual",
    "I6": "Consistência entre fontes"
}

# -------------------------
# Cabeçalho
# -------------------------
st.title("Sistema de Validação da Decisão")
st.write("Protótipo interativo para demonstrar um sistema de apoio à decisão com recomendação automática e validação humana final.")

with st.expander("ℹ️ Sobre este protótipo"):
    st.write("""
    Este dashboard permite simular um caso a partir de dados AIS/VMS e outras fontes contextuais.
    Com base nessas entradas, o sistema calcula automaticamente indicadores de validação,
    gera uma recomendação e, no final, permite a validação humana da decisão.
    """)

# -------------------------
# Layout principal
# -------------------------
coluna1, coluna2 = st.columns([1, 1], gap="large")

with coluna1:
    st.markdown('<div class="bloco">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">1. Entradas do sistema</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtexto">Nesta secção, o utilizador descreve o caso que pretende analisar.</div>', unsafe_allow_html=True)

    with st.expander("ℹ️ Ver explicação desta secção"):
        st.write("""
        Aqui são introduzidos os dados observados que servem de base à análise.
        Para simplificar o protótipo, apenas são consideradas entradas diretamente observáveis:
        dados AIS/VMS e outras fontes contextuais.
        """)

    st.markdown("### Dados AIS/VMS")

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="etiqueta">Posição/Trajetória</div>', unsafe_allow_html=True)
        posicao = st.selectbox(
            "Posição/Trajetória",
            ["Normal", "Ligeiramente suspeita", "Muito suspeita"],
            label_visibility="collapsed"
        )
    with col_b:
        st.markdown('<div class="etiqueta">Velocidade/Curso</div>', unsafe_allow_html=True)
        velocidade = st.selectbox(
            "Velocidade/Curso",
            ["Normal", "Ligeiramente suspeito", "Muito suspeito"],
            label_visibility="collapsed"
        )

    st.markdown("### Outras fontes")

    col_e, col_f = st.columns(2)
    with col_e:
        st.markdown('<div class="etiqueta">Concordância com radar/outras fontes</div>', unsafe_allow_html=True)
        radar = st.selectbox(
            "Concordância com radar/outras fontes",
            ["Concordante", "Parcialmente discordante", "Discordante"],
            label_visibility="collapsed"
        )
    with col_f:
        st.markdown('<div class="etiqueta">Contexto operacional</div>', unsafe_allow_html=True)
        contexto = st.selectbox(
            "Contexto operacional",
            ["Normal", "Pouco habitual", "Muito suspeito"],
            label_visibility="collapsed"
        )

    gerar = st.button("Gerar recomendação", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with coluna2:
    st.markdown('<div class="bloco">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">2. Lógica interna do sistema</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtexto">Os indicadores de validação são calculados automaticamente a partir das entradas fornecidas.</div>', unsafe_allow_html=True)

    with st.expander("ℹ️ Ver explicação desta secção"):
        st.write("""
        Nesta versão do protótipo, os indicadores de validação não são preenchidos manualmente pelo utilizador.
        Em vez disso, são calculados automaticamente pelo sistema com base nos dados introduzidos.
        """)

    st.info("Após clicar em “Gerar recomendação”, o sistema calcula automaticamente os indicadores de validação, a pontuação total, o nível de risco e a ação proposta.")
    st.markdown('</div>', unsafe_allow_html=True)

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
# Cálculo e apresentação
# -------------------------
if gerar:
    indicadores = calcular_indicadores(posicao, velocidade, radar, contexto)

    contributos = {}
    pontuacao_total = 0

    for chave, valor in indicadores.items():
        pontos = nivel_para_pontos(valor)
        contributo = pontos * pesos[chave]
        contributos[chave] = {
            "Código": chave,
            "Nome": nomes_indicadores[chave],
            "Nível": valor,
            "Pontos": pontos,
            "Peso": pesos[chave],
            "Contributo": contributo
        }
        pontuacao_total += contributo

    risco = nivel_risco(pontuacao_total)
    acao = acao_proposta(pontuacao_total)
    fundo, texto = cor_risco(risco)

    st.markdown('<div class="bloco-resultado">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">3. Resultado do sistema</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtexto">O sistema calcula automaticamente os indicadores, a pontuação total e propõe uma ação inicial.</div>', unsafe_allow_html=True)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Pontuação total", pontuacao_total)
    with m2:
        st.metric("Nível de risco", risco)
    with m3:
        st.metric("Ação proposta", acao)

    st.markdown(
        f"""
        <div class="acao-final" style="background-color:{fundo}; color:{texto};">
            Ação recomendada: {acao}
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

    ordenados = sorted(contributos.items(), key=lambda x: x[1]["Contributo"], reverse=True)
    fatores_principais = [
        {
            "codigo": item[0],
            "nome": item[1]["Nome"],
            "nivel": item[1]["Nível"],
            "contributo": item[1]["Contributo"]
        }
        for item in ordenados[:3]
    ]

    explicacao = gerar_explicacao_decisao(acao, risco, pontuacao_total, fatores_principais)

    st.markdown('<div class="bloco">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">4. Explicação da decisão e rastreabilidade</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtexto">Esta secção mostra, de forma simples, porque razão o sistema gerou esta recomendação.</div>', unsafe_allow_html=True)

    st.markdown(f'<div class="caixa-explicacao">{explicacao}</div>', unsafe_allow_html=True)

    col_resumo1, col_resumo2 = st.columns(2)

    with col_resumo1:
        st.markdown("#### Fatores principais da decisão")
        for fator in fatores_principais:
            st.write(f"• **{fator['nome']}** ({fator['codigo']}) — nível **{fator['nivel']}**")

    with col_resumo2:
        st.markdown("#### Resumo das entradas")
        st.write(f"**Posição/Trajetória:** {posicao}")
        st.write(f"**Velocidade/Curso:** {velocidade}")
        st.write(f"**Concordância com radar/outras fontes:** {radar}")
        st.write(f"**Contexto operacional:** {contexto}")

    st.markdown("#### Detalhe técnico dos indicadores")
    tabela = pd.DataFrame([
        {
            "Código": dados["Código"],
            "Indicador": dados["Nome"],
            "Nível atribuído": dados["Nível"],
            "Impacto na decisão": impacto_textual(dados["Contributo"])
        }
        for _, dados in contributos.items()
    ])

    st.dataframe(tabela, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="bloco">', unsafe_allow_html=True)
    st.markdown('<div class="titulo-secao">5. Validação humana</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtexto">O utilizador pode confirmar ou alterar a recomendação automática com justificação.</div>', unsafe_allow_html=True)

    col_v1, col_v2 = st.columns([1, 2])

    with col_v1:
        decisao_utilizador = st.selectbox(
            "Decisão final do utilizador",
            ["Confirmar ação proposta", "Ignorar", "Monitorizar", "Escalar", "Requer revisão"]
        )

    with col_v2:
        justificacao = st.text_area(
            "Justificação da decisão final",
            placeholder="Explica por que motivo confirmas ou alteras a ação proposta...",
            height=120
        )

    guardar = st.button("Guardar decisão final", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if guardar:
        decisao_final = acao if decisao_utilizador == "Confirmar ação proposta" else decisao_utilizador

        st.markdown('<div class="bloco-resultado">', unsafe_allow_html=True)
        st.markdown('<div class="titulo-secao">6. Decisão final justificada</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtexto">Registo final da decisão humana apoiada pelo sistema.</div>', unsafe_allow_html=True)

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.metric("Ação proposta", acao)
        with r2:
            st.metric("Decisão final", decisao_final)
        with r3:
            st.metric("Nível de risco", risco)
        with r4:
            st.metric("Pontuação total", pontuacao_total)

        st.markdown("#### Justificação")
        if justificacao.strip():
            st.write(justificacao)
        else:
            st.write("Não foi fornecida justificação.")

        st.success("Registo concluído com recomendação automática e validação humana.")
        st.markdown('</div>', unsafe_allow_html=True)
