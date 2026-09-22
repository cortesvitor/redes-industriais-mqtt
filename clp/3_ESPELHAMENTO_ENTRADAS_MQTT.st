(* =========================================================
   ESPELHAMENTO_ENTRADAS_MQTT  -  Program (ST)
   Le as entradas fisicas e monta os payloads de publicacao.
   Payload ON/OFF para casar com o dashboard.
   ========================================================= *)


(* ===== PARTE 1 - CAIXA DE CIMA ===== *)

PROGRAM ESPELHAMENTO_ENTRADAS_MQTT
VAR
END_VAR


(* ===== PARTE 2 - CAIXA DE BAIXO ===== *)

(* I00 e I01 sao as entradas integradas do XP340. Se o compilador
   acusar 'not defined', confira o nome real em
   Configuration (Config) > XP340 > Integrated I/O. *)

IF I00 THEN
    PUBS_PAYLOADS[1] := 'ON';
ELSE
    PUBS_PAYLOADS[1] := 'OFF';
END_IF

IF I01 THEN
    PUBS_PAYLOADS[2] := 'ON';
ELSE
    PUBS_PAYLOADS[2] := 'OFF';
END_IF
