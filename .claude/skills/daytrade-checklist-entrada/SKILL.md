---
name: daytrade-checklist-entrada
description: Roda o checklist pré-entrada (go/no-go) antes de abrir uma operação em WIN ou WDO, cobrindo plano, setup, stop, alvo, R:R, tamanho, horário, notícias e estado emocional. Use quando o usuário disser "vou entrar", "posso entrar?", "valida minha entrada", "checklist" ou descrever um trade que pretende fazer.
---

# Checklist pré-entrada: GO / NO-GO

Seja rápido: o trader pode estar com o preço andando. Faça as perguntas em bloco, numa mensagem só, e responda com um veredito claro.

## Itens

| # | Item | Critério para passar |
|---|---|---|
| 1 | Setup do plano | É um setup definido (ORB, OB/FVG, reteste de VWAP etc.), não um palpite |
| 2 | Confluência | ≥ 3 fatores a favor (skill `daytrade-confluencia-mtc`) |
| 3 | Stop definido | Nível técnico, com valor exato, antes da entrada |
| 4 | Alvo definido | Nível técnico (liquidez, extensão do range) |
| 5 | R:R | ≥ 1,5 |
| 6 | Tamanho | Risco ≤ 1–2% do capital (skill `daytrade-gestao-risco`) |
| 7 | Garantia | Capital e garantia suficientes; longe do stop automático de 70% |
| 8 | Horário | Fora de 17h30+ e fora dos 5 min antes/depois de notícia de alto impacto. Faixas preferidas: 9h–9h30 (ORB com confirmação) e 9h30–11h (manhã prime) |
| 9 | Limite diário | Ainda não bateu a perda máxima do dia nem o número máximo de trades |
| 10 | Emocional | Não está tentando recuperar perda, nem eufórico por ganho anterior |

## Veredito

- **GO**: todos os itens passam.
- **GO REDUZIDO**: só falham itens 2 (com +3 exato) ou 8 (horário de menor liquidez) → metade da mão.
- **NO-GO**: falha qualquer um dos itens 1, 3, 5, 6, 7, 9 ou 10. Diga qual e por quê, em uma linha.

## Saída

```
CHECKLIST · <ativo> <compra/venda> @ <entrada>
✓ 1 Setup ORB rompimento confirmado
✓ 3 Stop 172.950 (−150 pts / R$ 30 por contrato)
✗ 5 R:R 1,1 — alvo perto demais
...
VEREDITO: NO-GO — R:R abaixo de 1,5
```

Se for GO, sugira registrar o trade depois com a skill `daytrade-diario`. O checklist é disciplina operacional, não recomendação de investimento.
