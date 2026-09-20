import time
import paho.mqtt.client as mqtt

# ------------------------------------------------------------------------------
# Configurações do Broker e Certificados
# ------------------------------------------------------------------------------
# BROKER_IP = "10.0.0.90"  # Substitua pelo IP do seu servidor Mosquitto
BROKER_IP = "mosquitto"  # Substitua pelo IP do seu servidor Mosquitto
PORT = 8883

CA_CERT = "ca.crt"
CLIENT_CERT = "paho_client.crt"
CLIENT_KEY = "paho_client.key"

TOPIC_SUB = "esp32/temp"  # Tópico onde o ESP32 publica as leituras
TOPIC_PUB = "test/debug"  # Tópico onde o ESP32 escuta comandos


# ------------------------------------------------------------------------------
# Callbacks (Paho MQTT v2)
# ------------------------------------------------------------------------------
def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("✅ Conectado ao broker Mosquitto via mTLS!")
        client.subscribe(TOPIC_SUB)
        print(f"📡 Monitorando o tópico: {TOPIC_SUB}\n")
    else:
        print(f"❌ Falha ao conectar. Código de erro: {reason_code}")


def on_message(client, userdata, msg):
    print(f"--> [RX do ESP32] Tópico: {msg.topic} | Msg: {msg.payload.decode()}")


# ------------------------------------------------------------------------------
# Inicialização e Configuração mTLS
# ------------------------------------------------------------------------------
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
    client_id="pc-paho-monitor",
)

# Configura o mTLS passando a CA, o certificado e a chave privada do cliente
client.tls_set(ca_certs=CA_CERT, certfile=CLIENT_CERT, keyfile=CLIENT_KEY)

# Desativa validação estrita de hostname (necessário para conectar via IP local sem SAN)
client.tls_insecure_set(True)

client.on_connect = on_connect
client.on_message = on_message

# ------------------------------------------------------------------------------
# Loop Principal
# ------------------------------------------------------------------------------
print(f"Conectando ao broker MQTTS em {BROKER_IP}:{PORT}...")
client.connect(BROKER_IP, PORT, keepalive=60)

# Roda o processamento de rede em segundo plano
client.loop_start()

try:
    while True:
        # Envia comandos digitados no terminal para o ESP32
        cmd = input("Digite um comando (LIGAR / DESLIGAR / sair): ").strip()
        if cmd.lower() == "sair":
            break
        if cmd:
            client.publish(TOPIC_PUB, cmd)
            print(f"<-- [TX para ESP32] Mensagem '{cmd}' enviada em '{TOPIC_PUB}'")
except KeyboardInterrupt:
    pass
finally:
    print("\nEncerrando monitor...")
    client.loop_stop()
    client.disconnect()