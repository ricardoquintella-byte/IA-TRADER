---
name: daytrade-confluencia-mtc
description: Avalia a confluência MTC do dia, ou seja, se WIN e WDO estão ALINHADOS ou DIVERGENTES e se macro, fluxo e gráfico concordam em múltiplos timeframes. Gera um placar de confluência e decide se vale operar WIN, WDO, ambos ou nenhum. Use quando o usuário perguntar sobre confluência, MTC, "WIN e WDO estão alinhados?", "qual ativo operar hoje" ou "tem confluência pra entrar?".
---

# Confluência MTC: WIN × WDO, macro, fluxo e gráfico

Regra do app IA TRADER: **só operar com confluência de 3 ou mais fatores (macro + fluxo + gráfico)**.

## 1. Relação WIN × WDO

A relação normal é inversa: dólar sobe e o índice cai, e vice-versa.
- **ALINHADOS**: os sinais respeitam a relação inversa (WDO compra e WIN venda, ou WDO venda e WIN compra). O cenário é coerente.
- **DIVERGENTES**: os dois sobem ou os dois caem juntos. Costuma ser fluxo atípico ou evento específico; reduza a mão ou fique de fora.
- **NEUTRO**: um dos dois está sem direção.

## 2. Placar de confluência

Atribua +1 (a favor), 0 (neutro) ou −1 (contra) para o lado pretendido:

| Fator | O que olhar |
|---|---|
| Macro | viés do briefing (DXY, S&P, juros, commodities, agenda) |
| Timeframe maior | estrutura no diário/60 min |
| Timeframe operacional | estrutura no 5 min, BOS/CHoCH |
| VWAP | preço acima (compra) ou abaixo (venda), e inclinação |
| Fluxo | agressão no tape, saldo de players, volume no rompimento |
| Zona | reação em OB, FVG ou liquidez (skill `daytrade-smart-money`) |
| WIN×WDO | ALINHADOS +1, DIVERGENTES −1 |

Decisão:
- **≥ +4**: confluência forte, mão normal
- **+3**: confluência mínima, mão normal ou reduzida
- **+1 a +2**: insuficiente, não operar
- **≤ 0**: contra o lado pretendido; avalie o lado oposto ou fique fora

## 3. Saída

```
CONFLUÊNCIA MTC · <hora>
WIN×WDO: ALINHADOS / DIVERGENTES / NEUTRO

                 WIN (compra/venda)   WDO (compra/venda)
Macro            +1                   +1
TF maior         ...
TF operacional   ...
VWAP             ...
Fluxo            ...
Zona             ...
WIN×WDO          ...
TOTAL            +x                   +y

OPERAR WIN: SIM/NÃO — motivo
OPERAR WDO: SIM/NÃO — motivo
RISCO DO DIA: ...
```

Peça os dados que faltarem e marque o fator como 0 se o usuário não souber. Não é recomendação de investimento.
