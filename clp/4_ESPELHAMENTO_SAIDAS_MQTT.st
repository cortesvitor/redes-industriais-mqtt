(* =========================================================
   ESPELHAMENTO_SAIDAS_MQTT  -  Program (ST)
   Converte os payloads recebidos e aciona as saidas fisicas.
   ========================================================= *)


(* ===== PARTE 1 - CAIXA DE CIMA ===== *)

PROGRAM ESPELHAMENTO_SAIDAS_MQTT
VAR
END_VAR


(* ===== PARTE 2 - CAIXA DE BAIXO ===== *)

Q00 := (SUBS_PAYLOADS[1] = 'ON');
Q01 := (SUBS_PAYLOADS[2] = 'ON');
