# Skills de daytrade: WIN e WDO

Skills do Claude Code feitas para o fluxo do app IA TRADER PRO (MTC + ORB + Smart Money).
Elas carregam sozinhas quando o assunto aparece na conversa, ou podem ser chamadas pelo nome com `/nome-da-skill`.

| Momento | Skill | O que faz |
|---|---|---|
| Antes das 9h | `daytrade-briefing` | Cenário externo, agenda, níveis e viés do dia |
| Antes das 9h | `daytrade-controle-emocional` | Checagem de estado e regras de parada |
| Análise | `daytrade-confluencia-mtc` | Placar de confluência e WIN×WDO alinhados/divergentes |
| Análise | `daytrade-orb` | Range de abertura, entradas, stops, alvos, risco de fakeout |
| Análise | `daytrade-smart-money` | Order Blocks, FVG, liquidez, BOS/CHoCH |
| Antes de entrar | `daytrade-gestao-risco` | Contratos, risco em R$, garantia B3, stop automático |
| Antes de entrar | `daytrade-checklist-entrada` | GO / NO-GO em 10 itens |
| Durante o pregão | `daytrade-controle-emocional` | Tilt, revanche, overtrading |
| Depois do trade | `daytrade-diario` | Registra em `diario/trades.csv` |
| Fim do dia | `daytrade-revisao-dia` | Revisão pós-pregão e lição para amanhã |
| Semana/mês | `daytrade-estatisticas` | Acerto, payoff, expectativa, drawdown, por setup/horário |
| Pesquisa | `daytrade-backtest-orb` | Backtest do ORB em CSV de candles |

Os valores de garantia (R$ 155/contrato) e stop automático (70%) vêm do app. Confira sempre com a sua corretora.
Nada aqui é recomendação de investimento.
