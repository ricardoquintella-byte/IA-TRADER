---
name: daytrade-briefing
description: Monta o briefing pré-mercado para WIN e WDO (antes das 9h): agenda econômica, cenário externo (DXY, S&P futuro, Treasuries, petróleo, minério), níveis-chave do dia anterior e viés provável. Use quando o usuário pedir "briefing", "pré-mercado", "como abre hoje", "o que olhar hoje" ou "preparação do dia".
---

# Briefing pré-mercado: WIN e WDO

Objetivo: em uma tela, o trader sabe o contexto do dia, os níveis importantes e o que pode invalidar o viés. Você **não** dá ordem de compra ou venda; dá cenário.

## 1. Coleta (use busca na web se disponível; senão, peça os dados)

Cenário externo, com variação desde o fechamento anterior:
- DXY (índice do dólar) e USD/BRL à vista
- Futuros de S&P 500 e Nasdaq
- Treasury de 10 anos (yield)
- Petróleo (Brent) e minério de ferro (pesam em PETR e VALE, logo no índice)
- EWZ no pré-market, se disponível

Agenda do dia (horário de Brasília) com impacto alto/médio:
- Brasil: IPCA, Copom, ata, dados de atividade, leilões do Tesouro, falas do BC
- EUA: payroll, CPI, PCE, FOMC, auxílio-desemprego, falas do Fed
- Marque o que cai **dentro do pregão** (9h–18h); são horários para reduzir mão ou ficar fora

Níveis técnicos (peça ao usuário se não tiver acesso a dados):
- Máxima, mínima e fechamento do dia anterior (WIN e WDO)
- Ajuste do dia anterior (WDO principalmente)
- Gaps em aberto e zonas de Smart Money relevantes (ver skill `daytrade-smart-money`)

## 2. Leitura

- Correlação típica: dólar forte (DXY ↑, WDO ↑) costuma pesar no WIN, e vice-versa. Se WIN e WDO apontarem na mesma direção, sinalize **divergência** (ver `daytrade-confluencia-mtc`).
- Petróleo e minério em alta tendem a ajudar o WIN.
- Yield americano subindo forte tende a fortalecer o dólar.

## 3. Formato de saída

```
BRIEFING · <data>

EXTERIOR   DXY x% | S&P fut x% | US10Y x% | Brent x% | Minério x%
AGENDA     09:00 ... (impacto) | 10:30 ... | ...
           ⚠ janelas para evitar: ...

WIN        viés: COMPRA / VENDA / NEUTRO  — motivo em uma linha
           níveis: resistências ... | suportes ... | máx/mín ontem ...
WDO        viés: ... — motivo
           níveis: ...

CONFLUÊNCIA WIN×WDO: ALINHADOS / DIVERGENTES
INVALIDA O VIÉS SE: ...
RISCO DO DIA: BAIXO / MÉDIO / ALTO (agenda e volatilidade)
```

Se faltarem dados, diga o que faltou em vez de inventar números. Sempre informe a hora e a fonte dos dados coletados. Briefing é contexto, não recomendação de investimento.
