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
# CSS PERSONALIZADO
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
def plot_plano_horizontal(massa, forca_aplicada, mu):
    """Desenha um bloco no plano horizontal com vetores de força ajustados"""
    fig = go.Figure()
    g = 10
    normal = massa * g
    atrito = normal * mu

    # Chão
    fig.add_shape(type="rect", x0=-6, y0=-1, x1=6, y1=0,
                  fillcolor="#bdc3c7", line=dict(width=0))
    
    # Bloco (centro em x=0, y=1)
    fig.add_shape(type="rect", x0=-1.5, y0=0, x1=1.5, y1=2,
                  fillcolor="#3498db", line=dict(color="#2980b9", width=2))
    
    # Vetor Força Aplicada (Direita)
    if forca_aplicada > 0:
        fig.add_annotation(
            x=4, y=1, ax=1.5, ay=1,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="#2ecc71"
        )
        fig.add_annotation(x=4.5, y=1, text=f"F = {forca_aplicada:.1f} N", showarrow=False, font=dict(color="#2ecc71", size=14))
    
    # Vetor Força de Atrito (Esquerda)
    if atrito > 0:
        fig.add_annotation(
            x=-4, y=0.5, ax=-1.5, ay=0.5,
            xref='x', yref='y', axref='x', ayref='y',
            showarrow=True, arrowhead=2, arrowsize=1, arrowwidth=3, arrowcolor="#e74c3c"
        )
        fig.add_annotation(x=-4.5, y=0.5, text=f"Fat = {atrito:.1f} N", showarrow=False, font=dict(color="#e74c3c", size=14))

    # Vetor Peso (Baixo)
    fig.add_annotation(
        x=0, y=-3, ax=0, ay=0, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#9b59b6"
    )
    fig.add_annotation(x=0, y=-3.5, text=f"P = {normal:.1f} N", showarrow=False, font=dict(color="#9b59b6", size=14))

    # Vetor Normal (Cima)
    fig.add_annotation(
        x=0, y=5, ax=0, ay=2, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#f39c12"
    )
    fig.add_annotation(x=0, y=5.5, text=f"N = {normal:.1f} N", showarrow=False, font=dict(color="#f39c12", size=14))

    # Ajuste de layout para evitar sobreposições
    fig.update_layout(
        xaxis=dict(range=[-6, 6], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-4, 6], showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=10, b=10), height=350
    )
    return fig

def plot_plano_inclinado(massa, angulo_deg):
    """Desenha um plano inclinado até 90º com vetores de tamanho visual fixo para legibilidade"""
    fig = go.Figure()
    
    g = 10
    peso = massa * g
    ang_rad = math.radians(angulo_deg)
    px = peso * math.sin(ang_rad)
    py = peso * math.cos(ang_rad)
    
    # Geometria do triângulo da rampa usando raio fixo para não quebrar nos 90º
    R = 10 
    L = R * math.cos(ang_rad)
    H = R * math.sin(ang_rad)
    
    # Desenhar Rampa: Começa alto na esquerda e desce até a direita
    # Coordenadas: (0,0) -> (L,0) -> (0,H) -> (0,0)
    fig.add_trace(go.Scatter(
        x=[0, L, 0, 0], y=[0, 0, H, 0],
        fill="toself", fillcolor="#ecf0f1", line=dict(color="#bdc3c7", width=2),
        showlegend=False, hoverinfo="skip"
    ))
    
    # Centro da rampa
    cx = L / 2
    cy = H / 2
    
    # Offset para colocar o bloco sobre a superfície
    s = 1.0 # Tamanho base do bloco
    bx = cx + s * math.sin(ang_rad)
    by = cy + s * math.cos(ang_rad)
    
    # Coordenadas do bloco rotacionado
    def rot(px, py):
        # Rotacionar por -ang_rad
        rx = px * math.cos(-ang_rad) - py * math.sin(-ang_rad)
        ry = px * math.sin(-ang_rad) + py * math.cos(-ang_rad)
        return bx + rx, by + ry

    p1, p2, p3, p4 = rot(-s, -s), rot(s, -s), rot(s, s), rot(-s, s)
    
    fig.add_trace(go.Scatter(
        x=[p1[0], p2[0], p3[0], p4[0], p1[0]],
        y=[p1[1], p2[1], p3[1], p4[1], p1[1]],
        fill="toself", fillcolor="#3498db", line=dict(color="#2980b9", width=2),
        showlegend=False, hoverinfo="skip"
    ))
    
    # Escala fixa para os vetores desenhados (evita que invadam o bloco)
    v_len = 3.5 
    
    # P (Peso total - apontando reto para baixo)
    fig.add_annotation(
        x=bx, y=by - v_len, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=3, arrowcolor="#9b59b6"
    )
    fig.add_annotation(x=bx, y=by - v_len - 0.8, text=f"P={peso:.1f}N", showarrow=False, font=dict(color="#9b59b6", size=13))
    
    # Normal (Perpendicular à rampa, para cima e para direita)
    nx = bx + v_len * math.sin(ang_rad)
    ny = by + v_len * math.cos(ang_rad)
    fig.add_annotation(
        x=nx, y=ny, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#f39c12"
    )
    fig.add_annotation(x=nx + 0.8*math.sin(ang_rad), y=ny + 0.8*math.cos(ang_rad), text=f"N={py:.1f}N", showarrow=False, font=dict(color="#f39c12", size=13))
    
    # Py (Perpendicular à rampa, para baixo e para esquerda)
    pyx = bx - v_len * math.sin(ang_rad)
    pyy = by - v_len * math.cos(ang_rad)
    fig.add_annotation(
        x=pyx, y=pyy, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#e74c3c"
    )
    fig.add_annotation(x=pyx - 0.8*math.sin(ang_rad), y=pyy - 0.8*math.cos(ang_rad), text=f"Py={py:.1f}N", showarrow=False, font=dict(color="#e74c3c", size=13))
    
    # Px (Paralelo à rampa, deslizando para baixo e para direita)
    pxx = bx + v_len * math.cos(ang_rad)
    pxy = by - v_len * math.sin(ang_rad)
    fig.add_annotation(
        x=pxx, y=pxy, ax=bx, ay=by, xref='x', yref='y', axref='x', ayref='y',
        showarrow=True, arrowhead=2, arrowwidth=2, arrowcolor="#2ecc71"
    )
    fig.add_annotation(x=pxx + 0.8*math.cos(ang_rad), y=pxy - 0.8*math.sin(ang_rad), text=f"Px={px:.1f}N", showarrow=False, font=dict(color="#2ecc71", size=13))

    fig.update_layout(
        xaxis=dict(range=[-4, 14], showgrid=False, zeroline=False, visible=False),
        yaxis=dict(range=[-5, 13], scaleanchor="x", scaleratio=1, showgrid=False, zeroline=False, visible=False),
        plot_bgcolor='white', margin=dict(l=0, r=0, t=0, b=0), height=450
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
    
    g = 10  # Gravidade local
    
    with st.sidebar:
        st.subheader("Parâmetros do Bloco")
        massa = st.slider("Massa (kg)", 1.0, 50.0, 10.0, step=1.0)
        forca = st.slider("Força Aplicada (N)", 0.0, 200.0, 80.0, step=5.0)
        mu = st.slider("Coeficiente de Atrito (μ)", 0.0, 1.0, 0.3, step=0.05)
        
        st.markdown("---")
        st.markdown(f"**Gravidade (g):** {g} m/s²")
        st.markdown(f"**Força Normal (N):** {massa * g} N")
    
    # Cálculos
    normal = massa * g
    atrito = mu * normal
    forca_resultante = forca - atrito
    
    if forca_resultante < 0:
        forca_resultante = 0  # O bloco não se move se a força aplicada não vencer o atrito estático (simplificação didática)
    
    aceleracao = forca_resultante / massa
    
    st.markdown(r"$$ F_R = m \cdot a \implies a = \frac{F_R}{m} $$")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_plano_horizontal(massa, forca, mu), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Raciocínio")
        
        st.markdown(f"""
        1. **Força Normal ($N$):** $m \cdot g$ = {massa} $\cdot$ {g} = **{normal} N**
        2. **Força de Atrito ($F_{{at}}$):** $\mu \cdot N$ = {mu:.2f} $\cdot$ {normal} = **{atrito:.1f} N**
        3. **Força Aplicada ($F$):** **{forca:.1f} N**
        4. **Força Resultante ($F_R$):** {forca} - {atrito:.1f} = **{forca_resultante:.1f} N**
        """)
        
        st.markdown("---")
        st.markdown("**Aceleração gerada:**")
        st.markdown(rf"$$ a = \frac{{{forca_resultante:.1f}}}{{{massa}}} = {aceleracao:.2f} \text{{ m/s}}^2 $$")
        
        if forca_resultante == 0:
            st.warning("A força aplicada não é suficiente para vencer o atrito (ou é anulada por ele). O bloco permanece em repouso ou em Movimento Retilíneo Uniforme (MRU).")

# ============================================
# 2. PLANO INCLINADO
# ============================================
elif topico == "Plano Inclinado (Decomposição)":
    st.header("📐 Decomposição de Forças no Plano Inclinado")
    
    st.markdown("""
    <div class="concept-card" style="border-left-color: #2ecc71;">
        <b>Definição:</b> Em um plano inclinado, a força <b>Peso (P)</b> é decomposta em duas direções: 
        uma paralela ao plano ($P_x$) que causa o deslizamento, e outra perpendicular ($P_y$) que pressiona a superfície.
    </div>
    """, unsafe_allow_html=True)
    
    g = 10  # Gravidade local
    
    with st.sidebar:
        st.subheader("Parâmetros do Plano")
        massa_plano = st.slider("Massa do Bloco (kg)", 1.0, 50.0, 10.0, step=1.0)
        angulo = st.slider("Ângulo de Inclinação (°)", 0, 90, 30, step=1)
        st.info(f"Gravidade (g) adotada: **{g} m/s²**")
    
    # Cálculos
    p = massa_plano * g
    ang_rad = math.radians(angulo)
    px = p * math.sin(ang_rad)
    py = p * math.cos(ang_rad)
    
    # Equação principal com LaTeX limpo
    st.markdown(r"$$ P = m \cdot g \quad | \quad P_x = P \cdot \sin(\theta) \quad | \quad P_y = P \cdot \cos(\theta) $$")
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(plot_plano_inclinado(massa_plano, angulo), use_container_width=True)
    
    with col2:
        st.subheader("🧮 Decomposição Matemática")
        
        st.markdown(f"""
        **Dados Iniciais:**
        * Massa ($m$) = {massa_plano} kg
        * Ângulo ($\theta$) = {angulo}°
        * Peso Total ($P$) = {massa_plano} $\cdot$ {g} = **{p:.1f} N**
        
        ---
        **Componente Paralela ($P_x$):**
        Responsável por puxar o bloco para baixo da rampa.
        """)
        st.markdown(rf"$$ P_x = {p:.1f} \cdot \sin({angulo}^\circ) = {px:.1f} \text{{ N}} $$")
        
        st.markdown(f"""
        ---
        **Componente Perpendicular ($P_y$):**
        Pressiona o bloco contra a superfície (equivalente à Normal em módulos).
        """)
        st.markdown(rf"$$ P_y = {p:.1f} \cdot \cos({angulo}^\circ) = {py:.1f} \text{{ N}} $$")
        
        st.markdown("""
        <div class="step-box">
            <b>💡 Tente ajustar para os extremos:</b><br>
            Em <b>0°</b>, $P_x$ zera e todo o Peso vai para $P_y$. <br>
            Em <b>90°</b> (queda livre), $P_y$ zera e todo o Peso vai para $P_x$!
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
