import streamlit as st
from modelo import ejecutar_modelo, ejecutar_modelo_lento
import time
from PIL import Image
from modelo import count_words
import os

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

def analyze_word_count():
    st.title("Contador de palabras en archivo de texto")
    uploaded_file = st.file_uploader("Sube un archivo de texto", type=["txt"])
    
    if uploaded_file is not None:
        with open("temp.txt", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        num_words = count_words("temp.txt")
        st.success(f"Número de palabras en el archivo: {num_words}")
    os.remove("temp.txt")


op = st.selectbox("Elige programa", ['Contar numero de palabras',"Modelo con parametros a y b", "Modelo mucho más complejo | lento"])

if op == "Modelo con parametros a y b":
    analizar()

elif op == "Modelo mucho más complejo | lento":
    analizar_modelo_lento()
    
elif op == "Contar numero de palabras":
    analyze_word_count()

# streamlit run pruebita.py