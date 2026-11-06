#!/usr/bin/env python3
"""Estatísticas do diário de trades (diario/trades.csv). Só biblioteca padrão."""
import argparse
import csv
import json
import sys
from collections import defaultdict

VALOR_PONTO = {"WIN": 0.20, "WDO": 10.00}


def num(v):
    v = (v or "").strip()
    if not v:
        return None
    if "," in v:  # formato brasileiro 5.162,5
        v = v.replace(".", "").replace(",", ".")
    return float(v)


def faixa_horaria(h):
    if not h:
        return "sem hora"
    hh, mm = (int(x) for x in h.split(":")[:2])
    t = hh * 60 + mm
    if t < 9 * 60 + 30:
        return "09:00-09:30"
    if t < 11 * 60:
        return "09:30-11:00"
    if t < 13 * 60:
        return "11:00-13:00"
    if t < 15 * 60:
        return "13:00-15:00"
    if t < 17 * 60:
        return "15:00-17:00"
    return "17:00+"


def carregar(caminho, args, custos):
    trades, avisos = [], []
    with open(caminho, newline="", encoding="utf-8") as f:
        for i, r in enumerate(csv.DictReader(f), start=2):
            data = (r.get("data") or "").strip()
            ativo = (r.get("ativo") or "").strip().upper()
            if args.data and data != args.data:
                continue
            if args.de and data < args.de:
                continue
            if args.ate and data > args.ate:
                continue
            if args.ativo and ativo != args.ativo.upper():
                continue
            try:
                lado = (r.get("lado") or "").strip().upper()[:1]
                ent, sai = num(r.get("entrada")), num(r.get("saida"))
                qtd = int(num(r.get("contratos")) or 0)
                stop = num(r.get("stop"))
                if ativo not in VALOR_PONTO or lado not in ("C", "V") or ent is None or sai is None or qtd <= 0:
                    raise ValueError("campos obrigatórios inválidos")
            except Exception as e:  # noqa: BLE001
                avisos.append(f"linha {i} ignorada: {e}")
                continue
            sinal = 1 if lado == "C" else -1
            pts = (sai - ent) * sinal
            bruto = pts * VALOR_PONTO[ativo] * qtd
            liquido = bruto - custos.get(ativo, 0.0) * qtd
            r_mult = None
            if stop is not None and stop != ent:
                r_mult = pts / abs(ent - stop)
            trades.append({
                "data": data, "hora": (r.get("hora_entrada") or "").strip(), "ativo": ativo,
                "setup": (r.get("setup") or "").strip() or "sem setup",
                "plano": ((r.get("seguiu_plano") or "").strip().upper()[:1] or "?"),
                "emocao": (r.get("emocao") or "").strip().lower() or "?",
                "pts": pts, "rs": liquido, "r": r_mult,
            })
    trades.sort(key=lambda t: (t["data"], t["hora"]))
    return trades, avisos


def resumo(trades):
    n = len(trades)
    if n == 0:
        return {"trades": 0}
    ganhos = [t["rs"] for t in trades if t["rs"] > 0]
    perdas = [t["rs"] for t in trades if t["rs"] < 0]
    total = sum(t["rs"] for t in trades)
    med_g = sum(ganhos) / len(ganhos) if ganhos else 0.0
    med_p = sum(perdas) / len(perdas) if perdas else 0.0
    rs_r = [t["r"] for t in trades if t["r"] is not None]
    pico = acum = dd = 0.0
    seq = seq_max = 0
    for t in trades:
        acum += t["rs"]
        pico = max(pico, acum)
        dd = max(dd, pico - acum)
        seq = seq + 1 if t["rs"] < 0 else 0
        seq_max = max(seq_max, seq)
    return {
        "trades": n,
        "ganhadores": len(ganhos),
        "perdedores": len(perdas),
        "taxa_acerto_pct": round(100 * len(ganhos) / n, 1),
        "resultado_rs": round(total, 2),
        "ganho_medio_rs": round(med_g, 2),
        "perda_media_rs": round(med_p, 2),
        "payoff": round(med_g / abs(med_p), 2) if med_p else None,
        "expectativa_rs": round(total / n, 2),
        "expectativa_r": round(sum(rs_r) / len(rs_r), 2) if rs_r else None,
        "fator_lucro": round(sum(ganhos) / abs(sum(perdas)), 2) if perdas else None,
        "drawdown_max_rs": round(dd, 2),
        "max_perdas_seguidas": seq_max,
    }


def agrupar(trades, chave):
    g = defaultdict(list)
    for t in trades:
        g[t[chave] if chave != "faixa" else faixa_horaria(t["hora"])].append(t)
    linhas = []
    for k, ts in sorted(g.items()):
        s = resumo(ts)
        linhas.append({"grupo": k, "trades": s["trades"], "acerto_pct": s["taxa_acerto_pct"],
                       "resultado_rs": s["resultado_rs"], "expectativa_rs": s["expectativa_rs"],
                       "expectativa_r": s["expectativa_r"]})
    return linhas


def imprimir_tabela(titulo, linhas):
    print(f"\n{titulo}")
    print(f"  {'grupo':<14}{'trades':>7}{'acerto%':>9}{'result R$':>12}{'exp R$':>10}{'exp R':>8}")
    for l in linhas:
        er = "-" if l["expectativa_r"] is None else f"{l['expectativa_r']:.2f}"
        print(f"  {l['grupo'][:14]:<14}{l['trades']:>7}{l['acerto_pct']:>9.1f}"
              f"{l['resultado_rs']:>12.2f}{l['expectativa_rs']:>10.2f}{er:>8}")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("csv")
    p.add_argument("--data")
    p.add_argument("--de")
    p.add_argument("--ate")
    p.add_argument("--ativo")
    p.add_argument("--custo", default="", help="ex.: WIN=0.5,WDO=1.2 (R$ por contrato)")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    custos = {}
    for par in filter(None, args.custo.split(",")):
        k, v = par.split("=")
        custos[k.strip().upper()] = float(v)

    try:
        trades, avisos = carregar(args.csv, args, custos)
    except FileNotFoundError:
        sys.exit(f"Arquivo não encontrado: {args.csv}")

    out = {
        "resultado": "liquido" if custos else "bruto (sem custos)",
        "resumo": resumo(trades),
        "por_setup": agrupar(trades, "setup"),
        "por_ativo": agrupar(trades, "ativo"),
        "por_horario": agrupar(trades, "faixa"),
        "por_plano": agrupar(trades, "plano"),
        "por_emocao": agrupar(trades, "emocao"),
        "avisos": avisos,
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return
    s = out["resumo"]
    print(f"Resultado {out['resultado']}")
    if s["trades"] == 0:
        print("Nenhum trade no filtro.")
    else:
        for k, v in s.items():
            print(f"  {k:<22}{'-' if v is None else v}")
        imprimir_tabela("Por setup", out["por_setup"])
        imprimir_tabela("Por ativo", out["por_ativo"])
        imprimir_tabela("Por horário de entrada", out["por_horario"])
        imprimir_tabela("Seguiu o plano (S/N)", out["por_plano"])
        imprimir_tabela("Por emoção", out["por_emocao"])
    for a in avisos:
        print(f"AVISO: {a}")


if __name__ == "__main__":
    main()
