---
name: daytrade-smart-money
description: Mapeia zonas de Smart Money (conceitos ICT) em WIN e WDO, como Order Blocks, Fair Value Gaps (FVG), liquidez buy-side e sell-side, quebra de estrutura (BOS/CHoCH) e zonas de premium e discount. Use quando o usuário mencionar Order Block, FVG, imbalance, liquidez, stop hunt, BOS, CHoCH, ICT ou SMC, ou enviar candles/print do gráfico pedindo essas zonas.
---

# Smart Money (ICT) para WIN e WDO

## Dados de entrada

O ideal é OHLC em CSV (data, hora, open, high, low, close, volume) ou um print do gráfico. Peça o timeframe. Faça a leitura **de cima para baixo**: diário/60 min para a estrutura, 5 min para as zonas, 1–2 min para o gatilho.

## Conceitos e como identificar

**Estrutura**
- Alta: topos e fundos ascendentes. Baixa: descendentes.
- **BOS** (break of structure): rompe o último topo (alta) ou fundo (baixa) a favor da tendência.
- **CHoCH** (change of character): primeiro rompimento contra a tendência; é um alerta de possível reversão.

**Order Block (OB)**
- OB de alta: último candle de baixa antes de um movimento impulsivo de alta que faz BOS.
- OB de baixa: último candle de alta antes de um impulso de baixa que faz BOS.
- Zona = do open à mínima (alta) ou do open à máxima (baixa) desse candle.
- Fica mais forte se ainda não foi revisitado (mitigado) e se o impulso deixou FVG.

**Fair Value Gap (FVG)**
- Em três candles consecutivos, FVG de alta quando `low[3] > high[1]`; a zona vai de high[1] a low[3].
- FVG de baixa quando `high[3] < low[1]`.
- **Regra do app**: FVG só vale se estiver alinhado com a estrutura do timeframe maior.

**Liquidez**
- Buy-side: acima de topos iguais e de máximas óbvias (dia anterior, abertura). Sell-side: abaixo de fundos iguais e mínimas óbvias.
- Varredura (sweep): o preço passa do nível, captura stops e volta. Costuma anteceder o movimento real.

**Premium e discount**
- No range do impulso, acima de 50% é premium (preferir vendas) e abaixo de 50% é discount (preferir compras).

## Setup típico

1. Estrutura do timeframe maior define o lado.
2. O preço varre liquidez contra esse lado.
3. CHoCH ou BOS no timeframe menor a favor do lado.
4. Entrada no reteste do OB ou FVG gerado, com volume de absorção.
5. Stop além da extremidade da zona; alvo na liquidez oposta.

## Saída

Liste as zonas ordenadas por proximidade do preço atual:

```
<ATIVO> · TF <x> · estrutura: ALTA / BAIXA / LATERAL (último BOS/CHoCH em ...)

Zona          Tipo           Faixa            Status       Força
OB alta       demanda        172.800–173.050  não mitigado alta
FVG baixa     imbalance      173.550–173.700  parcial      média
Liquidez BS   topos iguais   ~174.300         intacta      —

Cenário provável: ...
Invalidação: ...
```

Ao trabalhar com print, avise que os níveis são aproximados. Não invente zonas sem dados; se não houver informação suficiente, diga o que falta. Análise técnica não é recomendação de investimento.
