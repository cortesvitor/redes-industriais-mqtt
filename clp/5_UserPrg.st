(* =========================================================
   UserPrg  -  ja existe em Application > UserPOUs
   Colar estas 3 chamadas na caixa de BAIXO.
   Sem isso o codigo compila mas nunca executa.

   A ordem importa: monta os payloads das entradas, roda o
   MQTT (publica e recebe), e so entao aplica as saidas.
   Invertendo, cada valor chega um ciclo atrasado.
   ========================================================= *)

ESPELHAMENTO_ENTRADAS_MQTT();
MQTT();
ESPELHAMENTO_SAIDAS_MQTT();
