---
name: daytrade-revisao-dia
description: Faz a revisão pós-pregão de um dia de daytrade a partir do diário de trades (diario/trades.csv), com resultado, aderência ao plano, erros recorrentes, melhor e pior trade e uma lição para amanhã. Use quando o usuário pedir "revisão do dia", "como foi hoje", "fechamento do dia", "post-market" ou "o que errei hoje".
---

# Revisão pós-pregão

## Passos

1. Rode as estatísticas do dia (data padrão: hoje):
   ```
   python3 .claude/skills/daytrade-estatisticas/estatisticas.py diario/trades.csv --data AAAA-MM-DD
   ```
   Se o diário do dia estiver vazio, ofereça registrar os trades primeiro (skill `daytrade-diario`).
2. Leia as linhas do dia no CSV para analisar trade a trade.
3. Se o usuário tiver o briefing do dia, compare o viés previsto com o que o mercado fez.

## O que avaliar

- **Resultado**: R$ bruto, em R, % do capital (pergunte o capital se não souber).
- **Aderência**: quantos trades com `seguiu_plano = S`. Compare o resultado dos que seguiram e dos que não seguiram.
- **Gestão**: algum trade sem stop? Perda maior que 1R (stop alargado)? Saída antes do alvo em trade vencedor?
- **Horário**: onde vieram os ganhos e as perdas (abertura, manhã, tarde).
- **Emoção**: houve trades marcados como revanche, ansioso ou eufórico? Qual foi o resultado deles?
- **Regras de parada**: alguma foi violada (ver `daytrade-controle-emocional`)?

## Saída

```
REVISÃO · <data>
Resultado: R$ ... | ... R | ... trades (... G / ... P)
Aderência ao plano: x/y trades — resultado dentro do plano R$ ... vs fora R$ ...

Melhor trade: ...
Pior trade:   ... — o que aconteceu
Erros do dia: 1) ... 2) ...
Acertos do dia: ...

LIÇÃO PARA AMANHÃ (uma só, acionável): ...
NOTA DE DISCIPLINA: x/10
```

A nota de disciplina avalia o processo, não o lucro. Um dia de prejuízo com plano seguido merece nota alta; lucro com regras quebradas merece nota baixa. Ofereça salvar a revisão em `diario/revisoes/AAAA-MM-DD.md`.
