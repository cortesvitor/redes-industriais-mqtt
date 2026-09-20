#!/usr/bin/env python3

import streamlit as st
import pandas as pd
import numpy as np
import paho.mqtt.client as mqtt

# 1. Estado da sessão para armazenar histórico
if "mensagens_mqtt" not in st.session_state:
    st.session_state.mensagens_mqtt = []

# 2. Conexão MQTT mantida em cache (rodata apenas uma vez)
@st.cache_resource
def iniciar_mqtt():
    def on_connect(client, userdata, flags, rc, properties=None):
        if rc == 0:
            print("Conectado ao Broker MQTT!")
            client.subscribe("test/debug")

    def on_message(client, userdata, msg):
        conteudo = msg.payload.decode('utf-8')
        texto = f"[{msg.topic}] {conteudo}"
        
        # Insere a mensagem no estado da sessão
        st.session_state.mensagens_mqtt.append(texto)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("localhost", 1883, keepalive=60)
    client.loop_start() 
    return client

iniciar_mqtt()

# --- INTERFACE PRINCIPAL ---

st.title("Dashboard MQTT em Tempo Real")
st.write("Exemplo de atualização automática com `@st.fragment`.")

# 3. FRAGMENTO AUTO-REFRESH: Atualiza só este bloco a cada 1 segundo
@st.fragment(run_every="1s")
def renderizar_painel_mqtt():
    st.subheader("Últimas Mensagens Recebidas (Auto-Update)")
    
    if st.session_state.mensagens_mqtt:
        # Exibe as últimas 5 mensagens
        for msg in reversed(st.session_state.mensagens_mqtt[-5:]):
            st.code(msg)
    else:
        st.info("Aguardando dados no tópico 'meu_topico/teste/#'...")

# Executa o fragmento com auto-refresh
renderizar_painel_mqtt()

st.divider()

# --- DEMAIS COMPONENTES (NÃO RECARREGAM A CADA SEGUNDO) ---

nome = st.text_input("Seu Nome")
if nome:
    st.success(f"Olá, {nome}!")

idade = st.slider("Idade", 0, 100, 25)
st.write(f"Idade: {idade}")