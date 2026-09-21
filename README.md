# Redes Industriais: Prática 2 - MQTT

Sistema IIoT (Industrial Internet of Things) utilizando **Mosquitto MQTT Broker**, **Paho MQTT Client** e **Streamlit** com criptografia **TLS/mTLS**, rodando em ambiente isolado via **Docker Compose**.


## Principais recursos

- **Comunicação segura:** implementa criptografia mTLS entre Broker e clientes.
- **Pronto para produção:** container Docker isola dependências e gerencia compilação e configuração.
- **Multiplataforma:** sistema roda em qualquer sistema operacional com suporte ao Docker.


## Pré-requisitos

- Docker Engine
- Docker Compose
- OpenSSL (para gerar chaves SSL)


## Instalação

1. **Clone este repositório** em sua máquina local:
```bash
git clone https://github.com/cortesvitor/redes-industriais-mqtt.git
```

2. **Compile o projeto** com o Docker Compose:
```bash
docker compose build
```


## Execução

1. **Suba os containers em background** com o Docker Compose:
```bash
docker compose up -d
```

2. **Monitore a execução dos containers** através dos logs:
```bash
docker compose logs -f
```

3. **Conecte os clientes ao Broker** através do IP local e da porta `8883`.

4. **Acesse a [dashboard](localhost:8501)** para interagir com o sistema.


## Comandos úteis

- **Encerrar a execução** dos containers
```
docker compose down
```

- **Listar containers** em execução
```
docker compose ps
```

- **Acessar terminal** do container
```
docker compose exec -it NOME_DO_CONTAINER sh
```

- **Acessar logs** de container específico
```
docker compose logs -f NOME_DO_CONTAINER
```

- **Acessar estatísticas de uso de recursos** dos containers
```
docker compose stats
```


## Atualizar chaves TLS

Acesse a [documentação](https://mosquitto.org/man/mosquitto-tls-7.html) para encontrar os comandos necessários para gerar novas chaves de autenticação para o TLS. Omitir flag `-aes256` para evitar solicitação de senha toda vez que o sistema for iniciado.


## License

The source code is released under an [MIT License](./LICENSE).
