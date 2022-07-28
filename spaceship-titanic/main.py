# -*- coding: utf-8 -*-
"""
Created on Thu Jul  7 21:35:05 2022

@author: act-3431
"""

import pandas as pd

df = pd.read_csv("train.csv")
df.info()

df["Transported"].head()

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
    
    
# Criar função pra gerar gráfico de barras e linhas pra cada variável
def gerarPlot(colunaParaComparar, df):
    df.dropna(inplace=True)
    
    if((df[colunaParaComparar].dtype is not np.dtype('O')) and (df[colunaParaComparar].dtype is not np.dtype('bool') )):
        hist, bins = np.histogram(df[colunaParaComparar],5)
        labels = list()
        
        for i in range(len(bins)-1):
            labels.append("{:.0f}-{:.0f}".format(bins[i],bins[i+1]))
            
        df[colunaParaComparar] = pd.cut(df[colunaParaComparar], bins, labels=labels)
    
    crosstab = pd.crosstab(index=df["Transported"], columns=df[colunaParaComparar]) # é um pandas dataframe
    labels = [str(x) if type(x) == type(True) else x for x in list(df[colunaParaComparar].value_counts().index)] # é preciso converter bool em str pra definir os labels corretamente
    width = 0.35
    
    # Substituir os valores por freq. relativa, invés de freq. absoluta
    for col in crosstab:
        crosstab[col] = crosstab[col]/crosstab[col].sum()    
    
    trueValues = list(crosstab.loc[True])
    
    fig, ax = plt.subplots()
    ax2 = ax.twinx()
    ax.bar(labels, df[colunaParaComparar].value_counts(), width)
    ax2.plot(trueValues,'go-')
    ax.legend()
    ax.set_title("Combination Chart")
    ax.set_xlabel(colunaParaComparar)
    ax.set_ylabel("Count")
    ax2.set_ylabel("Transported")
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0))
    plt.show()

gerarPlot("CryoSleep", df) 