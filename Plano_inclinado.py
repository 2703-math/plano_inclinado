import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

# ============================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================
st.set_page_config(
    page_title="Física Visual: Dinâmica",
    page_icon="🍎",
    layout="wide"
)

# ============================================
# CSS PERSONALIZADO (Mantendo o seu estilo)
# ============================================
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        text-align: center;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #555;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .concept-card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1.2rem;
        border-left: 4px solid;
        margin-bottom: 1rem;
    }
    .formula-box {
        background: #1a1a2e;
        color: #fff;
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        font-family: 'Courier New', monospace;
        font-size: 1.1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    .step-box {
        background: #fff8e1;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #ffc107;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# FUNÇÕES DE PLOTAGEM (PLOTLY)
# ============================================
def plot_plano_horizontal(massa, forca_aplicada, atrito):
    """Desenha um bloco no plano horizontal com vetores de força"""
    fig = go.Figure()

    # Chão
    fig.add_shape(type="rect", x0=-5, y0=-1, x1=5, y1=0,
                  fillcolor="#bdc3c7", line=dict(width=0))
    
    # Bloco
    fig.add_shape(type="rect", x0=-1, y0=0, x1=1, y1=2,
                  fillcolor="#3498db", line=dict(color="#2980b9", width=2))
    
    # Vetor Força Aplicada (Direita)
    if forca_aplicada > 0:
        fig.add_annotation(
            x=1 + (forca_aplicada/20), y=1, ax=1, ay=1,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="#2ecc71",
            text=f"F = {forca_aplicada} N", font=dict(color="#2ecc71", size=14, family="Arial Black"),
            yshift=10
        )
    
    # Vetor Força de Atrito (Esquerda)
    if atrito > 0:
        fig.add_annotation(
            x=-1 - (atrito/20), y=0.5, ax=-1, ay=0.5,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1.5, arrowwidth=3, arrowcolor="#e74c3c",
            text=f"Fat = {atrito} N", font=dict(color="#e74c3c", size=14, family="Arial Black"),
            yshift=10
        )

    # Vetor Peso e Normal
    fig.add_annotation(
        x=0, y=-1.5, ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#9b59b6", text="P", yshift=-10
    )
    fig.add_annotation(
        x=0, y=3.5, ax=0, ay=2, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#f39c12", text="N", yshift=10
    )

    fig.update_layout(
        xaxis=dict(range=[-5, 5], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-2, 4], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0), height=300
    )
    return fig

def plot_plano_inclinado(massa, angulo_deg):
    """Desenha um plano inclinado e os vetores decompostos"""
    fig = go.Figure()
    
    ang_rad = math.radians(angulo_deg)
    peso = massa * 9.8
    px = peso * math.sin(ang_rad)
    py = peso * math.cos(ang_rad)
    
    # Geometria do triângulo da rampa
    L = 8  # Comprimento da base
    H = L * math.tan(ang_rad)  # Altura
    
    # Desenhar Rampa
    fig.add_trace(go.Scatter(
        x=[0, L, L, 0], y=[0, 0, H, 0],
        fill="toself", fillcolor="#ecf0f1", line=dict(color="#bdc3c7", width=2),
        showlegend=False, hoverinfo="skip"
    ))
    
    # Centro do bloco no meio da rampa
    cx = L / 2
    cy = (H / 2) + 0.8  # Deslocamento vertical para apoiar na rampa
    
    # Coordenadas do bloco rotacionado (Aproximado para visualização)
    S = 1.5 # Tamanho do bloco
    dx1, dy1 = S * math.cos(ang_rad), S * math.sin(ang_rad)
    dx2, dy2 = -S * math.sin(ang_rad), S * math.cos(ang_rad)
    
    fig.add_trace(go.Scatter(
        x=[cx - dx1/2 - dx2/2, cx + dx1/2 - dx2/2, cx + dx1/2 + dx2/2, cx - dx1/2 + dx2/2, cx - dx1/2 - dx2/2],
        y=[cy - dy1/2 - dy2/2, cy + dy1/2 - dy2/2, cy + dy1/2 + dy2/2, cy - dy1/2 + dy2/2, cy - dy1/2 - dy2/2],
        fill="toself", fillcolor="#3498db", line=dict(color="#2980b9", width=2),
        showlegend=False, hoverinfo="skip"
    ))
    
    # Escala visual para os vetores
    escala = 0.05
    
    # P (Peso total - aponta para baixo)
    fig.add_annotation(
        x=cx, y=cy - (peso * escala), ax=cx, ay=cy,
        xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#9b59b6",
        text=f"P = {peso:.1f}N", font=dict(color="#9b59b6", size=12)
    )
    
    # Py (Perpendicular à rampa)
    fig.add_annotation(
        x=cx + (py * escala * math.sin(ang_rad)), y=cy - (py * escala * math.cos(ang_rad)),
        ax=cx, ay=cy, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#e74c3c",
        text=f"Py = {py:.1f}N", font=dict(color="#e74c3c", size=12)
    )
    
    # Px (Paralelo à rampa, descendo)
    fig.add_annotation(
        x=cx - (px * escala * math.cos(ang_rad)), y=cy - (px * escala * math.sin(ang_rad)),
        ax=cx, ay=cy, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#2ecc71",
        text=f"Px = {px:.1f}N", font=dict(color="#2ecc71", size=12)
    )
    
    # N (Normal - Perpendicular à rampa, para cima)
    fig.add_annotation(
        x=cx - (py * escala * math.sin(ang_rad)), y=cy + (py * escala * math.cos(ang_rad)),
        ax=cx, ay=cy, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#f39c12",
        text="Normal", font=dict(color="#f39c12", size=12)
    )

    fig.update_layout(
        xaxis=dict(range=[-1, 10], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-3, max(6, H+3)], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0), height=400
    )
    return fig

# ============================================
# TÍTULO E MENU LATERAL
# ============================================
st.markdown('<div class="main-title">🍎 Física Visual: Dinâmica</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Entendendo as Leis de Newton e a Decomposição de Forças de forma interativa</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("⚙️ Configurações")
    st.markdown("---")
    topico = st.radio(
        "📚 Escolha o cenário:",
        ["2ª Lei de Newton (Horizontal)", "Plano Inclinado (Decomposição)"],
        index=0
    )
    st.markdown("---")

# ============================================
# 1. SEGUNDA LEI DE NEWTON (HORIZONTAL)
# ============================================
if topico == "2ª Lei de Newton (Horizontal)":
    st.header("➡️ Princípio Fundamental da Dinâmica")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #3498db;">
        <b>Definição:</b> A aceleração de um corpo é diretamente proporcional à força resultante que atua sobre ele e inversamente proporcional à sua massa.
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Parâmetros do Bloco")
        massa = st.slider("Massa (kg)", 1.0, 50.0, 10.0, step=1.0)
        forca = st.slider("Força Aplicada (N)", 0.0, 200.0, 50.0, step=5.0)
        atrito = st.slider("Força de Atrito (N)", 0.0, 100.0, 10.0, step=1.0)
    
    # Cálculos
    forca_resultante = forca - atrito
    if forca_resultante < 0:
        forca_resultante = 0  # O bloco não se move se o atrito for maior que a força
    
    aceleracao = forca_resultante / massa
    
    st.markdown(f"""
    <div class="formula-box">
        F_R = m \cdot a \implies a = \frac{{F_R}}{{m}}
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_plano_horizontal(massa, forca, atrito), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Raciocínio")
        st.markdown(f"""
        <div style="font-size:1.1rem;line-height:2;">
        1. <b>Força a favor do movimento:</b> {forca} N <br>
        2. <b>Força contra o movimento (Atrito):</b> {atrito} N <br>
        3. <b>Força Resultante ($F_R$):</b> {forca} - {atrito} = <b>{forca_resultante} N</b><br>
        <br>
        <b>Aceleração gerada:</b><br>
        $a = \frac{{{forca_resultante}}}{{{massa}}}$ = <b>{aceleracao:.2f} m/s²</b>
        </div>
        """, unsafe_allow_html=True)
        
        if forca_resultante == 0:
            st.warning("A força aplicada não é suficiente para vencer o atrito (ou é anulada por ele). O bloco permanece em repouso ou em Movimento Retilíneo Uniforme (MRU).")

# ============================================
# 2. PLANO INCLINADO
# ============================================
elif topico == "Plano Inclinado (Decomposição)":
    st.header("📐 Decomposição de Forças no Plano Inclinado")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Definição:</b> Em um plano inclinado, a força <b>Peso (P)</b>, que sempre aponta para o centro da Terra, é decomposta em duas direções: 
        uma paralela ao plano ($P_x$) que causa o deslizamento, e outra perpendicular ($P_y$) que pressiona a superfície.
    </div>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Parâmetros do Plano")
        massa_plano = st.slider("Massa do Bloco (kg)", 1.0, 50.0, 10.0, step=1.0)
        angulo = st.slider("Ângulo de Inclinação (°)", 0, 80, 30, step=1)
        st.info("Gravidade (g) adotada: **9.8 m/s²**")
    
    # Cálculos
    g = 9.8
    p = massa_plano * g
    ang_rad = math.radians(angulo)
    px = p * math.sin(ang_rad)
    py = p * math.cos(ang_rad)
    
    st.markdown(f"""
    <div class="formula-box">
        P = m \cdot g \quad | \quad P_x = P \cdot \sin(\\theta) \quad | \quad P_y = P \cdot \cos(\\theta)
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_plano_inclinado(massa_plano, angulo), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Decomposição")
        st.markdown(f"""
        <div style="font-size:1.1rem;line-height:2;">
        <b>Dados Iniciais:</b><br>
        Massa ($m$) = {massa_plano} kg<br>
        Ângulo ($\\theta$) = {angulo}°<br>
        Peso Total ($P$) = {massa_plano} $\\times$ {g} = <b>{p:.1f} N</b><br>
        <hr>
        <b>Componente Paralela ($P_x$):</b><br>
        Responsável por puxar o bloco para baixo da rampa.<br>
        $P_x = {p:.1f} \cdot \sin({angulo}^\circ)$ = <b>{px:.1f} N</b><br>
        <hr>
        <b>Componente Perpendicular ($P_y$):</b><br>
        Pressiona o bloco contra a superfície (igual à Normal em módulos se não houver outras forças verticais).<br>
        $P_y = {p:.1f} \cdot \cos({angulo}^\circ)$ = <b>{py:.1f} N</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="step-box">
            <b>💡 Observação:</b> Note que se o ângulo for <b>0°</b>, $P_x$ se torna zero e $P_y$ assume o valor total do Peso. 
            Se o ângulo for <b>90°</b> (queda livre), $P_x$ vira o peso total e $P_y$ é zero!
        </div>
        """, unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.85rem; padding: 1rem;">
    🍎 <b>Física Visual</b> — Ferramenta educacional para o ensino de Dinâmica<br>
    Altere as configurações na barra lateral para interagir com o sistema.
</div>
""", unsafe_allow_html=True)