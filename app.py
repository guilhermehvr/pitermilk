import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="#filtros - Processamento de Imagens", layout="wide")

st.title("🖼️ Filtros de Processamento de Imagem com Streamlit")

st.write(
    "Envie uma imagem, escolha um filtro na barra lateral e veja o resultado em tempo real."
)

uploaded_file = st.file_uploader("Envie uma imagem (JPG, PNG)", type=["jpg", "jpeg", "png"])

def to_opencv(image_pil):
    """Converte imagem PIL para formato OpenCV (BGR)."""
    img = np.array(image_pil.convert("RGB"))
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    return img

def to_streamlit(img_cv):
    """Converte imagem OpenCV (BGR) para formato exibível no Streamlit (RGB)."""
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    return img_rgb

def aplicar_filtro(img_cv, filtro, params):
    if filtro == "Original":
        return img_cv

    elif filtro == "Escala de Cinza":
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    elif filtro == "Desfoque (Blur)":
        k = params.get("kernel", 5)
        if k % 2 == 0:
            k += 1  
        return cv2.GaussianBlur(img_cv, (k, k), 0)

    elif filtro == "Detecção de Bordas (Canny)":
        limiar1 = params.get("limiar1", 100)
        limiar2 = params.get("limiar2", 200)
        edges = cv2.Canny(img_cv, limiar1, limiar2)
        return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

    elif filtro == "Ajuste de Brilho/Contraste":
        alpha = params.get("alpha", 1.0)  
        beta = params.get("beta", 0)      
        ajustada = cv2.convertScaleAbs(img_cv, alpha=alpha, beta=beta)
        return ajustada

    elif filtro == "Sépia":
        kernel_sepia = np.array(
            [[0.272, 0.534, 0.131],
             [0.349, 0.686, 0.168],
             [0.393, 0.769, 0.189]]
        )
        sepia = cv2.transform(img_cv, kernel_sepia)
        sepia = np.clip(sepia, 0, 255).astype(np.uint8)
        return sepia

    elif filtro == "Negativo (Inverter Cores)":
        return cv2.bitwise_not(img_cv)

    else:
        return img_cv


if uploaded_file is not None:
    image_pil = Image.open(uploaded_file)
    img_cv = to_opencv(image_pil)

    st.sidebar.header("Configurações de Filtro")

    filtro = st.sidebar.selectbox(
        "Escolha um filtro:",
        [
            "Original",
            "Escala de Cinza",
            "Desfoque (Blur)",
            "Detecção de Bordas (Canny)",
            "Ajuste de Brilho/Contraste",
            "Sépia",
            "Negativo (Inverter Cores)",
        ],
    )

    params = {}

    if filtro == "Desfoque (Blur)":
        params["kernel"] = st.sidebar.slider(
            "Intensidade do desfoque (kernel)", min_value=3, max_value=51, value=9, step=2
        )

    elif filtro == "Detecção de Bordas (Canny)":
        params["limiar1"] = st.sidebar.slider(
            "Limiar 1", min_value=0, max_value=255, value=100
        )
        params["limiar2"] = st.sidebar.slider(
            "Limiar 2", min_value=0, max_value=255, value=200
        )

    elif filtro == "Ajuste de Brilho/Contraste":
        params["alpha"] = st.sidebar.slider(
            "Contraste (alpha)", min_value=0.5, max_value=3.0, value=1.0, step=0.1
        )
        params["beta"] = st.sidebar.slider(
            "Brilho (beta)", min_value=-100, max_value=100, value=0, step=5
        )

    img_processada = aplicar_filtro(img_cv, filtro, params)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Imagem Original")
        st.image(to_streamlit(img_cv), use_column_width=True)

    with col2:
        st.subheader(f"Imagem com filtro: {filtro}")
        st.image(to_streamlit(img_processada), use_column_width=True)

else:
    st.info("👆 Envie uma imagem na caixa acima para começar.")
