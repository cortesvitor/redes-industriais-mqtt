#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt




# Executado quando conecta ao Broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Conectado ao Broker MQTT com sucesso!")
        # Inscreve-se no tópico (# é wildcard para pegar todos os sub-tópicos)
        client.subscribe("meu_topico/teste/#")
    else:
        print(f"Falha na conexão. Código: {rc}")

# Executado sempre que uma mensagem chega
def on_message(client, userdata, msg):
    topico = msg.topic
    conteudo = msg.payload.decode('utf-8')
    print(f"[NOVA MENSAGEM] Tópico: '{topico}' | Dado: '{conteudo}'")

# Inicializa o cliente (usando a versão da API Paho v2)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

# Define as funções de callback
client.on_connect = on_connect
client.on_message = on_message

# Conecta ao broker (Ex: EMQX público na porta padrão 1883)
client.connect("broker.emqx.io", 1883, keepalive=60)

# Mantém o script rodando e escutando conexões
print("Iniciando loop de escuta. Pressione Ctrl+C para sair.")
client.loop_forever()







# Título e texto explicativo
st.title("Meu Primeiro App com Streamlit")
st.write("Esta é uma interface interativa construída puramente em Python.")

# Entrada de texto do usuário
nome = st.text_input("Qual é o seu nome?")
if nome:
    st.success(f"Olá, {nome}! Bem-vindo ao Streamlit.")

# Slider numérico
idade = st.slider("Selecione sua idade", 0, 100, 25)
st.write(f"Idade selecionada: **{idade} anos**")

# Exibição de tabela e gráfico simples
st.subheader("Visualização de Dados")
df = pd.DataFrame(
    np.random.randn(10, 2),
    columns=['Métrica A', 'Métrica B']
)

st.dataframe(df)
st.line_chart(df)
