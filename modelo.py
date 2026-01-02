import re
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score

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

# def zipf_law(file_path):
#     with open(file_path, 'r') as file:
#         text = file.read()
#         text = re.sub(r'[^\w]', ' ', text, flags=re.UNICODE)
#         text = text.lower()
#     words = text.split()
    
#     word_freq = {}
#     for word in words:
#         if word in word_freq:
#             word_freq[word] += 1
#         else:
#             word_freq[word] = 1

#     sorted_freq = sorted(word_freq.values(), reverse=True)
#     ranks = np.arange(1, len(sorted_freq) + 1)
    
#     plt.figure(figsize=(10, 6))
#     plt.loglog(ranks, sorted_freq, marker=".")
#     plt.title("Ley de Zipf")
#     plt.xlabel("Rango")
#     plt.ylabel("Frecuencia")
#     plt.grid(True)
#     plt.savefig("zipf_output.png")
    
#     return ranks, sorted_freq

def zipf_law():
    zipfs_law = lambda r, c, k: c*(r**-k) 

    r = np.arange(1,51,1) # 1 to 50 ranking
    n_words = 0 # number of words

    files = [f for f in os.listdir('txts') if f.endswith('.txt')] #search all files that endswith .txt
    d = {} 

    for file in files:
        with open(f'txts/{file}', 'r') as f:
            text = f.read() #read text
            text = re.sub(r'[^\w]', ' ', text, flags=re.UNICODE)

            text = text.lower()
            wds = text.split() # split a string into a list
            if len(wds)<1000: # check if the file contains less than 1000 words
                print(f'DISCARDED FILE! {file} contains less than 1000 words')
                continue
            n_words += len(wds)

            for w in wds: #words counter
                d[w] = d.get(w,0)+1

    sort_w = sorted(d.items(), key=lambda x: x[1], reverse=True)[:50] # get  the 50 most common words 

    mst_cmmn_wrds_df = pd.DataFrame(sort_w, columns=['Word', 'N_times'])

    mst_cmmn_wrds_df.index = range(1,51)
    mst_cmmn_wrds_df['Pr[%]'] = mst_cmmn_wrds_df['N_times']/n_words*100
    mst_cmmn_wrds_df['Word'] = mst_cmmn_wrds_df['Word'].str.upper()

    print(mst_cmmn_wrds_df)

    c, cov = curve_fit(zipfs_law,r,mst_cmmn_wrds_df['Pr[%]'])
    R2 = r2_score(mst_cmmn_wrds_df['Pr[%]'],zipfs_law(r, c[0], c[1]))
    print(f'R2: {R2:.2%}')

    f, ax = plt.subplots(figsize=(10,10),facecolor='.85')
    ax.bar(mst_cmmn_wrds_df['Word'], mst_cmmn_wrds_df['Pr[%]'], alpha=.3)
    ax.plot(mst_cmmn_wrds_df.index-1, zipfs_law(r, c[0], c[1]), linewidth=4, color='k')
    # ax.set_ylim([0,7])
    plt.xticks(fontsize=8,rotation=90)
    ax.set_xlabel('Words', fontsize=15)
    ax.set_ylabel('Probability [%]', fontsize=15)
    plt.title(f"Zipf's law | Nº of words used: {n_words}", fontsize=16)
    plt.savefig('zipfs_law_image.png')
    plt.show()