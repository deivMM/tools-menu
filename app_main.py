import streamlit as st
from modelo import ejecutar_modelo, ejecutar_modelo_lento, zipf_law
import time
from PIL import Image
from modelo import count_words
import os
import zipfile
from io import BytesIO

def analizar():
    st.title("Modelo tipo simulación")
    a = st.slider("Amplitud (a)", 0.1, 5.0, 1.0)
    b = st.slider("Frecuencia (b)", 0.5, 5.0, 1.0)
    
    if st.button("Run"):
        x, y = ejecutar_modelo(a, b)
        # st.line_chart(y)
        img = Image.open("output.png")
        st.image(img, caption="Resultado del modelo", use_container_width=True)

def analizar_modelo_lento():
    st.title("Modelo tipo simulación (lento)")

    # --- Inicializar estado ---
    if "resultado" not in st.session_state:
        st.session_state.resultado = None

    if "running" not in st.session_state:
        st.session_state.running = False

    a = st.slider("Amplitud (a)", 0.1, 5.0, 1.0)
    b = st.slider("Frecuencia (b)", 0.5, 5.0, 1.0)

    st.info("Modelo lento. Ajusta parámetros y pulsa Run.")

    # --- Botón Run ---
    if st.button("Run", disabled=st.session_state.running):
        st.session_state.running = True

        t0 = time.time()
        with st.spinner("Ejecutando modelo (≈5 s)..."):
            st.session_state.resultado = ejecutar_modelo_lento(a, b)

        st.session_state.running = False
        st.success(f"Cálculo terminado en {time.time() - t0:.2f} s")

    # --- Mostrar resultado ---
    if st.session_state.resultado is not None:
        x, y = st.session_state.resultado
        st.line_chart(y)


def zipf_model():
    st.title("Modelo de Ley de Zipf")
    
    uploaded_files = st.file_uploader("Sube un archivo de texto o un ZIP",type=["txt"], accept_multiple_files=True)
    os.makedirs("txts", exist_ok=True)

    if st.button("Calcular"):
        if not uploaded_files:
            st.warning("Primero sube al menos un archivo TXT")
        else:
            saved_files = []

            for i, uploaded_file in enumerate(uploaded_files, start=1):
                filename = f"temp_zipf_{i}.txt"
                filepath = os.path.join("txts", filename)

                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                saved_files.append(filepath)

            st.success(f"{len(saved_files)} archivos guardados. Ejecutando cálculo...")
        
    zipf_law()
    img = Image.open("zipfs_law_image.png")
    st.image(img, caption="Gráfico de la Ley de Zipf", use_container_width=True)
    
    files = [f for f in os.listdir('txts') if f.endswith('.txt')]
    for file in files:
        os.remove(os.path.join("txts", file))

op = st.selectbox("Elige programa", ["Zipf law",
                                     "Modelo pendulo amortiguado",
                                     "Transformada de fourier"])

if 'zipf' in op.lower():
    zipf_model()
    
elif 'pendulo' in op.lower():
    analizar_modelo_lento()
    
elif 'fourier' in op.lower():
    analizar()

# Quiero lanzar tres modelos diferentes antes de empezar a currar 
# 1. Modelo para contar palabras en archivo de texto (zipf)
# 2. Modelo de pendulo amortiguado 
# 3. Modelo con transforada de fourier

# streamlit run app_main.py