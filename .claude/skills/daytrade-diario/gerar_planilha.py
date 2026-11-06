#!/usr/bin/env python3
"""Gera diario/diario_trades.xlsx a partir de diario/trades.csv.

Uso: python3 gerar_planilha.py [diario/trades.csv] [diario/diario_trades.xlsx] [--custo WIN=1,WDO=0]
Abas: Operações (com pontos, R$ bruto, custo, líquido e acumulado), Resumo por dia, Resumo geral.
"""
import csv
import sys
from collections import OrderedDict
from datetime import date
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

VALOR_PONTO = {"WIN": 0.20, "WDO": 10.00}
args = [a for a in sys.argv[1:] if not a.startswith("--")]
origem = args[0] if args else "diario/trades.csv"
destino = args[1] if len(args) > 1 else "diario/diario_trades.xlsx"
custos = {"WIN": 1.0, "WDO": 0.0}
for i, a in enumerate(sys.argv):
    if a == "--custo" and i + 1 < len(sys.argv):
        for par in sys.argv[i + 1].split(","):
            k, v = par.split("=")
            custos[k.strip().upper()] = float(v)

with open(origem, newline="", encoding="utf-8") as f:
    linhas = sorted(csv.DictReader(f), key=lambda r: (r["data"], r["hora_entrada"]))

VERDE, VERM = Font(color="1E8E3E"), Font(color="C5221F")
CAB = PatternFill("solid", fgColor="1F3A5F")
CABF = Font(bold=True, color="FFFFFF")
BRL = 'R$ #,##0.00;[Red]-R$ #,##0.00'

def cabecalho(ws, nomes, larguras):
    ws.append(nomes)
    for i, (n, w) in enumerate(zip(nomes, larguras), start=1):
        c = ws.cell(row=1, column=i)
        c.fill, c.font = CAB, CABF
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "A2"

wb = Workbook()
ws = wb.active
ws.title = "Operações"
cabecalho(ws, ["Data", "Entrada", "Saída", "Ativo", "Lado", "Contratos", "Preço entrada", "Preço saída",
               "Pontos", "R$ bruto", "Custo", "R$ líquido", "Acumulado líquido", "Stop", "Setup",
               "Seguiu plano", "Emoção", "Notas"],
          [11, 9, 9, 6, 6, 9, 12, 12, 9, 11, 9, 11, 13, 10, 10, 8, 10, 40])
dias = OrderedDict()
acum = 0.0
for r in linhas:
    ativo = r["ativo"].upper()
    lado = r["lado"].upper()
    qtd = int(float(r["contratos"]))
    ent, sai = float(r["entrada"]), float(r["saida"])
    pts = (sai - ent) if lado == "C" else (ent - sai)
    bruto = pts * VALOR_PONTO.get(ativo, 0) * qtd
    custo = custos.get(ativo, 0) * qtd
    liq = bruto - custo
    acum += liq
    y, m, d = map(int, r["data"].split("-"))
    ws.append([date(y, m, d), r["hora_entrada"], r["hora_saida"], ativo, "Compra" if lado == "C" else "Venda",
               qtd, ent, sai, round(pts, 2), round(bruto, 2), round(custo, 2), round(liq, 2), round(acum, 2),
               float(r["stop"]) if r.get("stop") else None, r.get("setup") or None,
               r.get("seguiu_plano") or None, r.get("emocao") or None, r.get("notas") or None])
    row = ws.max_row
    ws.cell(row=row, column=1).number_format = "DD/MM/YYYY"
    for col in (7, 8, 14):
        ws.cell(row=row, column=col).number_format = "#,##0.##" if ativo == "WDO" else "#,##0"
    ws.cell(row=row, column=9).number_format = "#,##0.0"
    for col in (10, 11, 12, 13):
        ws.cell(row=row, column=col).number_format = BRL
    ws.cell(row=row, column=12).font = VERDE if liq > 0 else VERM if liq < 0 else Font()
    dd = dias.setdefault(r["data"], {"n": 0, "g": 0, "p": 0, "bruto": 0.0, "custo": 0.0, "liq": 0.0,
                                     "WIN": 0.0, "WDO": 0.0, "contratos": 0})
    dd["n"] += 1
    dd["g"] += liq > 0
    dd["p"] += liq < 0
    dd["bruto"] += bruto
    dd["custo"] += custo
    dd["liq"] += liq
    dd[ativo] = dd.get(ativo, 0.0) + bruto
    dd["contratos"] += qtd
ws.auto_filter.ref = ws.dimensions

wr = wb.create_sheet("Resumo por dia")
cabecalho(wr, ["Data", "Operações", "Ganhos", "Perdas", "Acerto %", "Contratos", "WIN bruto", "WDO bruto",
               "R$ bruto", "Custos", "R$ líquido", "Acumulado líquido"],
          [11, 10, 8, 8, 9, 10, 12, 12, 12, 10, 12, 14])
acum = 0.0
for d, v in dias.items():
    acum += v["liq"]
    y, m, dd_ = map(int, d.split("-"))
    wr.append([date(y, m, dd_), v["n"], v["g"], v["p"], round(100 * v["g"] / v["n"], 1), v["contratos"],
               round(v["WIN"], 2), round(v["WDO"], 2), round(v["bruto"], 2), round(v["custo"], 2),
               round(v["liq"], 2), round(acum, 2)])
    row = wr.max_row
    wr.cell(row=row, column=1).number_format = "DD/MM/YYYY"
    for col in range(7, 13):
        wr.cell(row=row, column=col).number_format = BRL
    wr.cell(row=row, column=11).font = VERDE if v["liq"] > 0 else VERM if v["liq"] < 0 else Font()
tot = {k: sum(v[k] for v in dias.values()) for k in ("n", "g", "p", "contratos", "WIN", "WDO", "bruto", "custo", "liq")}
wr.append(["TOTAL", tot["n"], tot["g"], tot["p"], round(100 * tot["g"] / max(tot["n"], 1), 1), tot["contratos"],
           round(tot["WIN"], 2), round(tot["WDO"], 2), round(tot["bruto"], 2), round(tot["custo"], 2),
           round(tot["liq"], 2), None])
row = wr.max_row
for c in range(1, 13):
    wr.cell(row=row, column=c).font = Font(bold=True)
for col in range(7, 12):
    wr.cell(row=row, column=col).number_format = BRL
wr.append([])
wr.append([f"Custos por contrato usados: WIN R$ {custos['WIN']:.2f} · WDO R$ {custos['WDO']:.2f}"
           + (" (custo do WDO não informado: líquido do WDO = bruto)" if not custos["WDO"] else "")])
wr.cell(row=wr.max_row, column=1).font = Font(italic=True, color="666666")
wr.append(["Fonte: diario/trades.csv (importado dos relatórios do Profit). Ganho/perda contam pelo líquido."])
wr.cell(row=wr.max_row, column=1).font = Font(italic=True, color="666666")

wb.save(destino)
print(f"{destino}: {len(linhas)} operações, {len(dias)} dias, líquido R$ {tot['liq']:.2f} (bruto R$ {tot['bruto']:.2f})")
