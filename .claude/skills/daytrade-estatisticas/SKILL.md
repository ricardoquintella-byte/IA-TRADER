---
name: daytrade-estatisticas
description: Calcula as estatísticas de desempenho do diário de trades (diario/trades.csv), como taxa de acerto, payoff, expectativa, fator de lucro, drawdown máximo, sequência de perdas e resultado por setup, ativo, horário, aderência ao plano e emoção. Use quando o usuário perguntar "como estou indo", "qual minha taxa de acerto", "meu payoff", "qual setup funciona melhor", "estatísticas do mês" ou "relatório de desempenho".
---

# Estatísticas de desempenho

Use o script deste diretório (só biblioteca padrão do Python):

```
python3 .claude/skills/daytrade-estatisticas/estatisticas.py diario/trades.csv [opções]

  --data AAAA-MM-DD        um dia
  --de AAAA-MM-DD          início do período
  --ate AAAA-MM-DD         fim do período
  --ativo WIN|WDO          filtra o ativo
  --custo WIN=0.5,WDO=1.2  custo por contrato por trade (corretagem + emolumentos), em R$
  --json                   saída em JSON
```

Pergunte o custo por contrato da corretora do usuário se ele não tiver informado; sem isso o resultado é **bruto**, e isso precisa ficar explícito na resposta.

## Como interpretar (explique ao usuário em linguagem simples)

- **Taxa de acerto** sozinha não diz nada; olhe junto com o **payoff** (ganho médio ÷ perda média).
- **Expectativa por trade** (em R$ e em R) é o número principal: se for positiva com 30+ trades, o método tem vantagem; abaixo de 30 trades, avise que a amostra é pequena.
- **Fator de lucro** = ganhos brutos ÷ perdas brutas. Abaixo de 1 perde dinheiro; acima de 1,5 é saudável.
- **Drawdown máximo** em R$: compare com o capital. Se passar de 20%, alerte.
- **Seguiu plano S × N**: costuma ser o achado mais útil. Destaque a diferença.
- **Por setup e horário**: sugira cortar o que tem expectativa negativa com amostra razoável (≥ 15 trades).

## Saída

Resumo em até 8 linhas com os números principais, depois as tabelas por setup, horário e plano, e por fim **duas ou três conclusões acionáveis**. Ofereça uma página visual (artifact) se o usuário quiser ver gráficos da curva de capital.
