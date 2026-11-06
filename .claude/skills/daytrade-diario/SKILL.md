---
name: daytrade-diario
description: Registra operações de daytrade (WIN e WDO) no diário de trades do repositório, em diario/trades.csv, inclusive importando o relatório OperationReport.csv do Profit, e lista ou corrige registros. Use quando o usuário enviar o CSV ou print do relatório da corretora, o usuário disser "registra esse trade", "anota no diário", "entrei/saí em ...", "fiz X pontos", colar operações da corretora, ou pedir para ver ou editar trades anteriores.
---

# Diário de trades

Arquivo: `diario/trades.csv`, na raiz do repositório. Se não existir, crie com o cabeçalho abaixo.

```
data,hora_entrada,hora_saida,ativo,lado,contratos,entrada,stop,alvo,saida,setup,seguiu_plano,emocao,notas
```

| Coluna | Formato | Exemplo |
|---|---|---|
| data | AAAA-MM-DD | 2026-11-03 |
| hora_entrada, hora_saida | HH:MM ou HH:MM:SS | 09:34 |
| ativo | WIN ou WDO | WIN |
| lado | C (compra) ou V (venda) | C |
| contratos | inteiro | 2 |
| entrada, stop, alvo, saida | número com ponto decimal | 173550 ou 5162.5 |
| setup | texto curto, sem vírgula | ORB, OB, FVG, VWAP, outro |
| seguiu_plano | S ou N | S |
| emocao | uma palavra | calmo, ansioso, revanche, euforico |
| notas | texto sem vírgula (use ; se precisar) | saiu antes do alvo por medo |

## Importar o relatório do Profit (preferido)

Se o usuário enviar o `OperationReport.csv` exportado do Profit (relatório de operações), não transcreva à mão:

```
python3 -I .claude/skills/daytrade-diario/importar_profit.py <caminho do OperationReport.csv> diario/trades.csv
```

O script lê a data do cabeçalho, converte lado e preços, ajusta arredondamentos para o resultado bater com a corretora e substitui as operações daquele dia mantendo as anotações manuais (stop, alvo, setup, seguiu_plano, emocao, notas). Depois confira o total bruto com o "Res. Total Intervalo" da última linha do relatório.

## Planilha Excel

Depois de qualquer importação ou alteração no diário, regenere a planilha e envie ao usuário:

```
python3 .claude/skills/daytrade-diario/gerar_planilha.py diario/trades.csv diario/diario_trades.xlsx --custo WIN=1,WDO=0
```

Abas: Operações (pontos, R$ bruto, custo, líquido, acumulado), Resumo por dia e totais. Ajuste `--custo` quando o usuário informar o custo por contrato da corretora.

## Como registrar à mão

1. Extraia os campos da mensagem do usuário. Converta preços no formato brasileiro (`5.162,5`) para `5162.5`.
2. Se faltarem **entrada, saída, ativo, lado ou contratos**, pergunte. Os outros campos podem ficar vazios, mas incentive preencher stop, setup e seguiu_plano, porque sem eles as estatísticas ficam pobres.
3. Mostre o resultado calculado antes de gravar:
   - pontos = (saida − entrada) para compra; (entrada − saida) para venda
   - R$ bruto = pontos × valor_do_ponto × contratos (WIN 0,20; WDO 10,00)
   - Múltiplo R = pontos / |entrada − stop| (se houver stop)
4. Acrescente a linha ao CSV, sem reescrever as linhas existentes.
5. Para vários trades colados de uma vez (ex.: extrato da corretora), monte todas as linhas e mostre uma tabela de confirmação antes de gravar.

## Consultas e correções

- "Trades de hoje / da semana": leia o CSV e mostre uma tabela com o resultado de cada trade e o total.
- Para estatísticas completas, use a skill `daytrade-estatisticas`.
- Correção: mostre a linha atual e a nova, e só então altere.

## Versionamento

Depois de gravar, pergunte se o usuário quer commitar o diário (`git add diario/trades.csv && git commit`). Não faça push sem ele pedir.
