#!/usr/bin/env python3

"""
O Paho roda em uma thread em backgroud para interagir com o Broker MQTT.
O Streamlit roda este script em loop (o decorador @st.cache_resource
evita que os recursos sejam redefinidos).

Direcao dos topicos:
  XP340/I_00, I_01  -> publicado pelo CLP (entrada fisica) e tambem
                       pelo dashboard (entrada virtual). Ambos assinam.
  XP340/Q_00, Q_01  -> publicado pelo dashboard (comando de saida).
                       O CLP assina e aciona a saida fisica.

Payload: "ON" / "OFF" em todos os topicos.
"""

import streamlit as st
import paho.mqtt.client as mqtt
import json

# Variáveis compartilhadas entre o Paho e o Streamlit
@st.cache_resource
def get_state():
    return {
        # "MQTT_BROKER_HOST": "10.0.0.90",
        "MQTT_BROKER_HOST": "mosquitto",
        "MQTT_BROKER_PORT": 1883,
        "counter": 0,
        "I_00": "OFF",
        "I_01": "OFF",
        "Q_00": "OFF",
        "Q_01": "OFF",
    }



# MQTT (Paho) -----------------------------------------------------------------

# Tópicos do Broker MQTT
class Topics:
    TOPIC_COUNTER = "XP340/counter"
    TOPIC_I_00 = "XP340/I_00"
    TOPIC_I_01 = "XP340/I_01"
    TOPIC_Q_00 = "XP340/Q_00"
    TOPIC_Q_01 = "XP340/Q_01"


# Streamlit obtém valores atualizados pelo Paho.
state = get_state()

# Inicializa variáveis internas do Streamlit (usadas para renderização)
# Os recursos visuais usam tipos específicos que não devem ser
# sobrescritos com tipos diferentes vindos do get_state()
st.session_state.counter = 0
st.session_state.I_00 = False
st.session_state.I_01 = False
st.session_state.Q_00 = False
st.session_state.Q_01 = False

# Configuração do MQTT executada apenas 1 vez (decorador @st.cache_resources)
@st.cache_resource()
def iniciar_mqtt():

    # Configurações inicias de conexão ao Broker. Basicamente assina tópicos MQTT.
    def on_connect(client, userdata, flags, reason_code, properties=None):
        if reason_code == 0:
            print("Conectado ao Broker MQTT com sucesso!")
            client.subscribe([
                (Topics.TOPIC_COUNTER, 0),
                (Topics.TOPIC_I_00, 0),
                (Topics.TOPIC_I_01, 0),
                (Topics.TOPIC_Q_00, 0),
                (Topics.TOPIC_Q_01, 0)
            ])

    # Callback do MQTT para novas mensagens.
    def on_message(client, userdata, msg):

        # Mensagens MQTT são sempre transmitidas com tipo 'bytes'!
        # Sempre é necessário decodificar com o decode('utf-8')  e depois analisar o tipo interno.
        payload = msg.payload.decode('utf-8').strip()

        match msg.topic:

            case Topics.TOPIC_COUNTER:
                try:
                    # A mensagem de TOPIC_COUNTER espera tipo interno 'dict'.
                    # payload_json (counter) = {"counter": value (int), "status": value (str)}.
                    payload_json = json.loads(payload)
                    state['counter'] = payload_json['counter']
                    print(payload_json['counter'])
                except Exception as e:
                    print(e)

            # As mensagens de TOPIC_I_XX e TOPIC_Q_XX esperam tipo interno 'string'.
            case Topics.TOPIC_I_00:
                state["I_00"] = payload
            case Topics.TOPIC_I_01:
                state["I_01"] = payload
            case Topics.TOPIC_Q_00:
                state["Q_00"] = payload
            case Topics.TOPIC_Q_01:
                state["Q_01"] = payload

    # Cliente MQTT que se conectará ao Broker MQTT
    client = mqtt.Client(
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id="paho-client-01",
    )

    # Certificados mTLS desabilitados neste teste (broker escutando 1883 sem TLS).
    # Para religar: voltar o listener 8883 com cafile/certfile/keyfile no
    # mosquitto.conf, reabrir a porta no compose e descomentar o bloco abaixo.
    # client.tls_set(
    #     ca_certs="certs/ca.crt",
    #     certfile="certs/paho_client.crt",
    #     keyfile="certs/paho_client.key",
    # )
    # client.tls_insecure_set(True)  # Habilitar em caso de problemas de CN na autenticação mTLS

    client.on_connect = on_connect
    client.on_message = on_message

    # Parâmetros de conexão. Porta 1883 = MQTT sem TLS.
    client.connect(
        host=state['MQTT_BROKER_HOST'],
        port=state['MQTT_BROKER_PORT'],
        keepalive=60,
    )

    # Dispara thread do Paho em background.
    client.loop_start()
    return client

# Instância do Paho, executada apenas 1 vez e que roda em background.
mqtt_client = iniciar_mqtt()



# DASHBOARD (Streamlit) -------------------------------------------------------

# Listeners dos botões do streamlit que publicam no Broker MQTT
def _publicar(topico, ligado):
    mqtt_client.publish(topico, "ON" if ligado else "OFF", retain=True)

def on_change_I_00():
    _publicar(Topics.TOPIC_I_00, st.session_state.I_00)

def on_change_I_01():
    _publicar(Topics.TOPIC_I_01, st.session_state.I_01)

def on_change_Q_00():
    _publicar(Topics.TOPIC_Q_00, st.session_state.Q_00)

def on_change_Q_01():
    _publicar(Topics.TOPIC_Q_01, st.session_state.Q_01)


# Layout da página/interface streamlit
st.set_page_config(page_title="Painel MQTT", layout="wide")
st.title("Prática 2 - MQTT")
st.caption(f"Broker Address: `{state['MQTT_BROKER_HOST']}:{state['MQTT_BROKER_PORT']}`")

st.divider()  # Um simples divisor na interface.

# Dashboard contendo os elementos dinâmicos (atualizada a cada 100ms)
@st.fragment(run_every="0.1s")
def dashboard():

    st.subheader("Entradas")
    st.caption("Publicadas pelo CLP (entrada física) ou pelos toggles (entrada virtual).")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # Mostrador da variável 'counter'
        st.metric(
            label="Counter",
            value=state['counter']
        )

    with col2:
        # Seletor da entrada 'I_00'
        st.toggle(
            label="Forçar I_00",
            key="I_00",
            on_change=on_change_I_00
        )
        # Estado de I_00 lido do broker
        st.metric(
            label="Entrada I_00",
            value=state['I_00']
        )

    with col3:
        # Seletor da entrada 'I_01'
        st.toggle(
            label="Forçar I_01",
            key="I_01",
            on_change=on_change_I_01
        )
        # Estado de I_01 lido do broker
        st.metric(
            label="Entrada I_01",
            value=state['I_01']
        )

    st.divider()

    st.subheader("Saídas")
    st.caption("Comandadas pelo dashboard. O CLP assina estes tópicos e aciona as saídas físicas.")

    col4, col5 = st.columns([1, 1])

    with col4:
        # Comando da saída 'Q_00'
        st.toggle(
            label="Acionar Q_00",
            key="Q_00",
            on_change=on_change_Q_00
        )
        st.metric(
            label="Saída Q_00",
            value=state['Q_00']
        )

    with col5:
        # Comando da saída 'Q_01'
        st.toggle(
            label="Acionar Q_01",
            key="Q_01",
            on_change=on_change_Q_01
        )
        st.metric(
            label="Saída Q_01",
            value=state['Q_01']
        )

dashboard()
