---
name: daytrade-gestao-risco
description: Calcula tamanho de posição, risco por trade, garantia B3 e stop automático diário para WIN (mini-índice) e WDO (mini-dólar). Use quando o usuário perguntar "quantos contratos", "quanto arrisco", "qual meu stop", "minha garantia", "limite de perda do dia", ou informar capital e quiser saber como operar com segurança.
---

# Gestão de risco: WIN e WDO

Você ajuda o trader a dimensionar posições **antes** de operar. Nunca sugira aumentar a mão para recuperar perda.

## Especificações dos contratos

| Contrato | Valor do ponto | Tick mínimo | Valor do tick |
|---|---|---|---|
| WIN (mini-índice) | R$ 0,20 por ponto | 5 pontos | R$ 1,00 |
| WDO (mini-dólar) | R$ 10,00 por ponto | 0,5 ponto | R$ 5,00 |

Parâmetros usados no app IA TRADER (confirme sempre com a corretora, porque mudam):
- Garantia por contrato: **R$ 155,00**
- Stop automático da corretora: **70% da garantia total**
- Capital recomendado: **≥ 3× a garantia total**

Se o usuário informar valores diferentes da corretora dele, use os dele.

## Entradas necessárias

Pergunte só o que faltar:
1. Capital disponível na conta (R$)
2. Ativo (WIN ou WDO)
3. Risco máximo por trade, em % do capital (padrão sugerido: 1%; nunca acima de 2%)
4. Distância do stop técnico em pontos (vem do setup: ORB, Order Block etc.)

## Cálculos

```
risco_R$          = capital × risco_%
perda_por_contrato = stop_pontos × valor_do_ponto
contratos          = floor(risco_R$ / perda_por_contrato)

garantia_total     = contratos × garantia_por_contrato
stop_auto_dia      = garantia_total × 0,70
capital_minimo     = garantia_total × 3
limite_diario_sug  = min(stop_auto_dia, capital × 3%)
```

Regras de saída:
- Se `contratos == 0`: diga claramente que o stop técnico é grande demais para o capital e o risco escolhidos. Sugira esperar um setup com stop menor; não sugira apertar o stop artificialmente.
- Se `capital < capital_minimo`: alerte que o capital está abaixo do recomendado para essa quantidade.
- Mostre também o risco:retorno (R:R) se o usuário der o alvo: `R:R = alvo_pontos / stop_pontos`. Abaixo de 1,5 sinalize como desfavorável.

## Formato da resposta

Tabela curta com: contratos, risco em R$, risco em % do capital, garantia total, stop automático do dia, limite diário sugerido, R:R. Depois, no máximo três linhas de alerta.

Exemplo: capital R$ 5.000, WIN, risco 1%, stop 150 pts
- risco = R$ 50; perda por contrato = 150 × 0,20 = R$ 30 → **1 contrato** (R$ 30 de risco, 0,6%)
- garantia = R$ 155; stop auto = R$ 108,50; capital mínimo = R$ 465 ✓

## Regras inegociáveis para lembrar

- Atingiu o limite diário: **para o dia**. Sem revanche.
- Stop é definido antes da entrada e não é alargado com o trade aberto.
- Não somar posição perdedora (preço médio) em daytrade alavancado.

Isto é cálculo de risco, não recomendação de investimento.
