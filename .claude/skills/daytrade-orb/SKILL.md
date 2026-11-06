---
name: daytrade-orb
description: Calcula e avalia o setup ORB (Opening Range Breakout) para WIN e WDO, com range de abertura, entradas de compra e venda, stops, alvos e risco de fakeout. Use quando o usuário falar em ORB, range de abertura, rompimento da abertura, "máxima e mínima dos primeiros 15/30 minutos", ou passar a máxima e mínima da abertura.
---

# ORB: Opening Range Breakout

## Definição usada

- **Janela do range**: 9h00–9h30 (padrão do app IA TRADER). Aceite 9h00–9h15 se o usuário preferir.
- **OR High / OR Low**: máxima e mínima da janela. **Range** = High − Low.
- Só se opera depois que a janela fecha e há **candle de confirmação** (fechamento fora do range, não só pavio).

## Entradas necessárias

Ativo, OR High, OR Low. Opcional: volume da janela vs. média, VWAP, viés do briefing.

## Cálculo dos níveis

Arredonde para o tick (WIN: 5 pts; WDO: 0,5 pt).

```
buffer = max(1 tick, 5% do range)

COMPRA  entrada = OR High + buffer
        stop    = ponto médio do range  (agressivo: OR Low − buffer)
        alvo 1  = entrada + 1 × range
        alvo 2  = entrada + 2 × range

VENDA   entrada = OR Low − buffer
        stop    = ponto médio do range  (agressivo: OR High + buffer)
        alvo 1  = entrada − 1 × range
        alvo 2  = entrada − 2 × range
```

Mostre risco e R:R de cada lado em pontos e em R$ por contrato (WIN R$ 0,20/pt; WDO R$ 10/pt). Para quantidade de contratos, use a skill `daytrade-gestao-risco`.

## Filtros de qualidade e risco de fakeout

Classifique o risco de fakeout em BAIXO, MÉDIO ou ALTO:
- Range muito estreito (< 0,4× a amplitude média da abertura dos últimos dias) → rompimento falso mais comum
- Range muito largo (> 1,5× a média) → stop caro; prefira esperar reteste
- Rompimento **contra** o viés do briefing ou contra a confluência WIN×WDO → ALTO
- Rompimento sem aumento de volume → MÉDIO/ALTO
- Notícia de alto impacto nos próximos 30 min → ALTO, aguarde
- Preço rompe e volta para dentro do range em 1–2 candles → invalida; não reentrar no mesmo lado sem nova estrutura

## Saída

```
ORB <ATIVO> · janela 9h00–9h30
OR High ... | OR Low ... | Range ... pts

COMPRA   entrada ... | stop ... | alvo1 ... | alvo2 ... | R:R ...
VENDA    entrada ... | stop ... | alvo1 ... | alvo2 ... | R:R ...

Risco de fakeout: ... (motivos)
Lado preferido pelo contexto: ... ou "nenhum, aguardar"
```

Os níveis são técnicos e servem de plano; não são recomendação de investimento.
