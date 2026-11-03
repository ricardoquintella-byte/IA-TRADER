#!/usr/bin/env python3
"""Importa o relatório de operações do Profit (OperationReport.csv) para diario/trades.csv.

Uso: python3 importar_profit.py OperationReport.csv [diario/trades.csv]

- Lê a data do cabeçalho ("Data: DD/MM/AAAA") e as linhas de operação (separador ;).
- Lado V = vendeu primeiro: entrada = preço de venda, saída = preço de compra.
- Se o preço arredondado do relatório não bater com os pontos informados, ajusta a
  entrada para o resultado conferir com a corretora.
- Operações já existentes no diário (mesma data, hora de entrada HH:MM, ativo, lado e
  contratos) são atualizadas mantendo stop, alvo, setup, seguiu_plano, emocao e notas.
"""
import csv
import os
import sys

CAMPOS = ["data", "hora_entrada", "hora_saida", "ativo", "lado", "contratos", "entrada",
          "stop", "alvo", "saida", "setup", "seguiu_plano", "emocao", "notas"]
MANUAIS = ["stop", "alvo", "setup", "seguiu_plano", "emocao", "notas"]


def num_br(v):
    v = (v or "").strip()
    if not v or v == "-":
        return None
    return float(v.replace(".", "").replace(",", "."))


def fmt(n):
    return str(int(n)) if float(n).is_integer() else f"{n:.2f}".rstrip("0").rstrip(".")


def ativo_base(simbolo):
    s = simbolo.strip().upper()
    for base in ("WIN", "WDO", "IND", "DOL"):
        if s.startswith(base):
            return {"IND": "WIN", "DOL": "WDO"}.get(base, base)
    return s


def ler_profit(caminho):
    with open(caminho, encoding="utf-8-sig", errors="replace") as f:
        linhas = f.read().splitlines()
    data = None
    for l in linhas[:10]:
        if l.lower().startswith("data:"):
            d, m, a = l.split(":", 1)[1].strip().split("/")
            data = f"{a}-{m}-{d}"
    ini = next(i for i, l in enumerate(linhas) if l.startswith("Ativo;"))
    if not data:
        sys.exit("Data não encontrada no cabeçalho do relatório.")
    trades = []
    for r in csv.DictReader(linhas[ini:], delimiter=";"):
        if not (r.get("Ativo") or "").strip():
            continue
        lado = r["Lado"].strip().upper()[:1]
        pc, pv = num_br(r["Preço Compra"]), num_br(r["Preço Venda"])
        qtd = int(num_br(r["Qtd Compra"]) or num_br(r["Qtd Venda"]))
        entrada, saida = (pv, pc) if lado == "V" else (pc, pv)
        pts = num_br(r.get("Res. Operação (%)")) or 0.0
        calc = (saida - entrada) * (1 if lado == "C" else -1)
        if abs(calc - pts) > 0 and abs(calc - pts) < 1:  # arredondamento do preço médio
            entrada = saida - pts if lado == "C" else saida + pts
        trades.append({
            "data": data, "hora_entrada": r["Abertura"].strip(), "hora_saida": r["Fechamento"].strip(),
            "ativo": ativo_base(r["Ativo"]), "lado": lado, "contratos": str(qtd),
            "entrada": fmt(entrada), "stop": "", "alvo": "", "saida": fmt(saida),
            "setup": "", "seguiu_plano": "", "emocao": "", "notas": r["Ativo"].strip(),
        })
    return data, trades


def chave(t):
    return (t["data"], t["hora_entrada"][:5], t["ativo"], t["lado"], t["contratos"])


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    destino = sys.argv[2] if len(sys.argv) > 2 else "diario/trades.csv"
    data, novos = ler_profit(sys.argv[1])
    existentes = []
    if os.path.exists(destino):
        with open(destino, newline="", encoding="utf-8") as f:
            existentes = list(csv.DictReader(f))
    do_dia = [t for t in existentes if t["data"] == data]
    outros = [t for t in existentes if t["data"] != data]
    usados, atualizados = set(), 0
    for n in novos:
        for i, e in enumerate(do_dia):
            if i not in usados and chave(e) == chave(n):
                usados.add(i)
                for c in MANUAIS:
                    if (e.get(c) or "").strip():
                        n[c] = e[c]
                atualizados += 1
                break
    sobras = [e for i, e in enumerate(do_dia) if i not in usados]
    final = sorted(outros + novos, key=lambda t: (t["data"], t["hora_entrada"]))
    os.makedirs(os.path.dirname(destino) or ".", exist_ok=True)
    with open(destino, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, extrasaction="ignore")
        w.writeheader()
        w.writerows(final)
    print(f"{data}: {len(novos)} operações importadas ({atualizados} já existiam e mantiveram as anotações).")
    if sobras:
        print(f"AVISO: {len(sobras)} registro(s) desse dia no diário não estão no relatório e foram removidos:")
        for s in sobras:
            print("  ", ",".join(s.get(c, "") for c in CAMPOS))


if __name__ == "__main__":
    main()
