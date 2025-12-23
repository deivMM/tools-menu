import re
import time
import numpy as np
import matplotlib.pyplot as plt

def count_words(file_path):
    with open(file_path, 'r') as file:
        text = file.read()
        text = re.sub(r'[^\w]', ' ', text, flags=re.UNICODE)
        text = text.lower()
    words = text.split()
    return len(words) 


def ejecutar_modelo(a, b):
    x = np.linspace(0, 10, 200)
    y = a * np.sin(b * x)
    plt.plot(x, y)
    plt.savefig("output.png")
    return x, y

def ejecutar_modelo_lento(a, b):
    time.sleep(5)  # Simula cálculo pesado

    x = np.linspace(0, 10, 200)
    y = a * np.sin(b * x)

    return x, y