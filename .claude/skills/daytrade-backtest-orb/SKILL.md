---
name: daytrade-backtest-orb
description: Faz backtest do setup ORB (Opening Range Breakout) em dados históricos intradiários de WIN ou WDO (CSV OHLC de 1 ou 5 minutos), testando janela do range, stop, alvo e horário de saída, e compara variações de parâmetros. Use quando o usuário pedir backtest, "esse setup funciona?", "testa o ORB no histórico", "qual melhor janela/alvo" ou enviar um CSV de candles.
---

# Backtest do ORB

Script: `.claude/skills/daytrade-backtest-orb/backtest_orb.py` (só biblioteca padrão).

## Dados

CSV com cabeçalho contendo `datetime,open,high,low,close` (volume opcional). Também aceita colunas separadas `data` e `hora`. Datas `AAAA-MM-DD HH:MM` ou `DD/MM/AAAA HH:MM`. Separador `,` ou `;`, e decimal com vírgula também é aceito. Os candles devem ser de **um único contrato contínuo** (ex.: WIN@N no Profit, histórico do MT5 ou do TradingView).

Se o usuário não tiver dados, explique onde exportar (Profit, MetaTrader 5, TradingView) e não invente resultados.

## Uso

```
python3 .claude/skills/daytrade-backtest-orb/backtest_orb.py dados.csv --ativo WIN \
    [--inicio 09:00] [--janela 30] [--stop meio|oposto] [--alvo 1.0] \
    [--saida 12:00] [--custo 0.5] [--contratos 1] [--grade] [--trades saida.csv]
```

- `--janela`: minutos do range de abertura (padrão 30, ou seja, 9h00–9h30)
- `--stop meio`: ponto médio do range; `oposto`: extremo oposto
- `--alvo`: múltiplo do range (1.0 = 1× range)
- `--saida`: horário limite; zera a posição no fechamento do candle desse horário
- `--grade`: roda combinações de janela (15/30), stop (meio/oposto) e alvo (1/1,5/2) e mostra um ranking

## Premissas (sempre informe ao usuário)

- No máximo 1 trade por dia: o primeiro rompimento (candle que **fecha** fora do range), com entrada no fechamento desse candle.
- Se stop e alvo forem atingidos no mesmo candle, conta como **stop** (conservador).
- Não modela slippage além do custo informado. Resultado em R$ para o número de contratos dado.

## Cuidados na interpretação

- Menos de 100 dias de dados: amostra fraca.
- Com `--grade`, avise sobre **overfitting**: o melhor parâmetro do passado tende a piorar no futuro. Sugira validar separando o período (ex.: otimizar em 2024 e testar em 2025 com `--de/--ate`).
- Compare a expectativa líquida (com custos) e o drawdown máximo, não só o lucro total.

Backtest não garante resultado futuro.
