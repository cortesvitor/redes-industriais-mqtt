(* =========================================================
   GVL_MQTT  -  Global Variable List
   Application > MQTT (pasta) > Add Object > GVL
   ========================================================= *)

VAR_GLOBAL
    (* Estruturas de publicacao e assinatura *)
    Pubs : ARRAY[1..gc_uiMaxPubs] OF MQTT_PUBLISH;
    Subs : ARRAY[1..gc_uiMaxSubs] OF MQTT_SUBSCRIBE;

    (* TOPICOS DE PUBLICACAO - entradas que o CLP envia *)
    PUBLISH_TOPICS : ARRAY[1..gc_uiMaxPubs] OF STRING := [
        'XP340/I_00',
        'XP340/I_01'
    ];

    (* TOPICOS DE ASSINATURA - saidas que o CLP recebe *)
    SUBSCRIBE_TOPICS : ARRAY[1..gc_uiMaxSubs] OF STRING := [
        'XP340/Q_00',
        'XP340/Q_01'
    ];

    (* Status das publicacoes e mensagens recebidas *)
    MQTT_FB_Pub_Status        : ARRAY[1..gc_uiMaxPubs] OF BOOL;
    MQTT_FB_Received_Messages : ARRAY[1..gc_uiMaxSubs] OF MQTT_RECEIVED;

    (* Payloads *)
    PUBS_PAYLOADS : ARRAY[1..gc_uiMaxPubs] OF STRING;
    SUBS_PAYLOADS : ARRAY[1..gc_uiMaxSubs] OF STRING;

    (* Auxiliar - so publica quando o valor muda *)
    PUBS_PAYLOADS_OLD : ARRAY[1..gc_uiMaxPubs] OF STRING;
END_VAR
