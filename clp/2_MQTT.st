(* =========================================================
   MQTT  -  Program (ST)
   Application > MQTT (pasta) > Add Object > POU
              tipo Program, linguagem Structured Text

   O editor tem DUAS caixas:
   PARTE 1 na de CIMA, PARTE 2 na de BAIXO.
   ========================================================= *)


(* ===== PARTE 1 - CAIXA DE CIMA ===== *)

PROGRAM MQTT
VAR
    MQTT_FB            : MQTT_CLIENT;
    MQTT_FB_Enable     : BOOL := TRUE;
    MQTT_FB_Error      : BOOL;
    MQTT_FB_State      : MQTT_STATES;
    MQTT_FB_Error_Code : MQTT_ERR_CODE;
    i                  : INT;
END_VAR


(* ===== PARTE 2 - CAIXA DE BAIXO ===== *)

(* Conexao com o broker.
   sHostname = IP do PC que roda o docker compose, nao 'mosquitto'.
   O CLP esta fora da rede do Docker e nao resolve esse nome. *)
MQTT_FB.CONNECTION_CONFIG.sHostname     := '192.168.15.10';
MQTT_FB.CONNECTION_CONFIG.uiPort        := 1883;
MQTT_FB.CONNECTION_CONFIG.sClientId     := 'XP340_CLP';
MQTT_FB.CONNECTION_CONFIG.bCleanSession := TRUE;

(* Ponteiros para as variaveis de publicacao e assinatura *)
MQTT_FB.PUBLISH   := Pubs;
MQTT_FB.SUBSCRIBE := Subs;

(* Habilita a funcao MQTT *)
MQTT_FB.ENABLE := MQTT_FB_Enable;

(* Variaveis de erro *)
MQTT_FB_Error      := MQTT_FB.ERROR;
MQTT_FB_State      := MQTT_FB.STATE;
MQTT_FB_Error_Code := MQTT_FB.ERROR_CODE;

(* Status das publicacoes e mensagens recebidas *)
MQTT_FB_Pub_Status        := MQTT_FB.PUBLISH_STATUS;
MQTT_FB_Received_Messages := MQTT_FB.RECEIVED_MESSAGES;

(* Publicacao *)
FOR i := 1 TO TO_INT(gc_uiMaxPubs) DO
    Pubs[i].sPublishTopic        := PUBLISH_TOPICS[i];
    Pubs[i].pbPublishPayload     := ADR(PUBS_PAYLOADS[i]);
    Pubs[i].uiPublishPayloadSize := TO_UINT(LEN(PUBS_PAYLOADS[i]));
    Pubs[i].ePublishMessageQoS   := MQTT_QOS_0;
    Pubs[i].bPublishRetain       := TRUE;

    IF (PUBS_PAYLOADS[i] <> PUBS_PAYLOADS_OLD[i]) THEN
        PUBS_PAYLOADS_OLD[i]   := PUBS_PAYLOADS[i];
        Pubs[i].bEnablePublish := TRUE;
    END_IF

    IF (MQTT_FB_Pub_Status[i]) THEN
        Pubs[i].bEnablePublish := FALSE;
    END_IF
END_FOR

(* Assinatura *)
FOR i := 1 TO TO_INT(gc_uiMaxSubs) DO
    Subs[i].sSubscribeTopic  := SUBSCRIBE_TOPICS[i];
    Subs[i].pbPayloadBuffer  := ADR(SUBS_PAYLOADS[i]);
    Subs[i].uiMaxPayloadSize := SIZEOF(SUBS_PAYLOADS[i]);
    Subs[i].eSubscribeQoS    := MQTT_QOS_0;
END_FOR

(* Reconexao em caso de falha *)
IF MQTT_FB_Error THEN
    MQTT_FB_Enable := PULSE_5S;
ELSE
    MQTT_FB_Enable := TRUE;
END_IF

(* Chamada do bloco *)
MQTT_FB();
