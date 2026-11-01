#!/usr/bin/env python3
"""Backtest do ORB (Opening Range Breakout) para WIN/WDO em candles intradiários. Só biblioteca padrão."""
import argparse
import csv
import sys
from collections import OrderedDict
from datetime import datetime

VALOR_PONTO = {"WIN": 0.20, "WDO": 10.00}
FORMATOS = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M",
            "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M")


def num(v):
    v = v.strip()
    if "," in v:
        v = v.replace(".", "").replace(",", ".")
    return float(v)


def parse_dt(s):
    s = s.strip()
    for f in FORMATOS:
        try:
            return datetime.strptime(s[:19] if "T" in s else s, f)
        except ValueError:
            continue
    raise ValueError(f"data/hora não reconhecida: {s!r}")


def carregar(caminho):
    with open(caminho, newline="", encoding="utf-8-sig") as f:
        amostra = f.readline()
        f.seek(0)
        sep = ";" if amostra.count(";") > amostra.count(",") else ","
        leitor = csv.DictReader(f, delimiter=sep)
        cols = {c.strip().lower(): c for c in leitor.fieldnames or []}

        def col(*nomes):
            for n in nomes:
                if n in cols:
                    return cols[n]
            return None

        c_dt = col("datetime", "data_hora", "time", "date_time")
        c_d, c_h = col("data", "date"), col("hora", "time")
        c_o, c_hi = col("open", "abertura"), col("high", "maxima", "máxima")
        c_l, c_c = col("low", "minima", "mínima"), col("close", "fechamento")
        if not all([c_o, c_hi, c_l, c_c]) or not (c_dt or (c_d and c_h)):
            sys.exit(f"Colunas não reconhecidas: {leitor.fieldnames}")
        candles = []
        for r in leitor:
            dt = parse_dt(r[c_dt]) if c_dt else parse_dt(f"{r[c_d]} {r[c_h]}")
            candles.append((dt, num(r[c_o]), num(r[c_hi]), num(r[c_l]), num(r[c_c])))
    candles.sort(key=lambda x: x[0])
    dias = OrderedDict()
    for c in candles:
        dias.setdefault(c[0].date(), []).append(c)
    return dias


def minutos(hhmm):
    h, m = hhmm.split(":")
    return int(h) * 60 + int(m)


def simular(dias, ativo, inicio, janela, stop_modo, alvo_mult, saida, custo, contratos):
    ini = minutos(inicio)
    fim_rng = ini + janela
    lim = minutos(saida)
    vp = VALOR_PONTO[ativo]
    trades, sem_trade = [], 0
    for dia, cs in dias.items():
        rng = [c for c in cs if ini <= c[0].hour * 60 + c[0].minute < fim_rng]
        if not rng:
            continue
        H, L = max(c[2] for c in rng), min(c[3] for c in rng)
        R = H - L
        if R <= 0:
            continue
        pos = None
        for c in cs:
            t = c[0].hour * 60 + c[0].minute
            if t < fim_rng:
                continue
            dt, o, hi, lo, cl = c
            if pos is None:
                if t >= lim:
                    break
                if cl > H:
                    stop = (H + L) / 2 if stop_modo == "meio" else L
                    pos = {"lado": "C", "ent": cl, "stop": stop, "alvo": cl + alvo_mult * R, "hora": dt}
                elif cl < L:
                    stop = (H + L) / 2 if stop_modo == "meio" else H
                    pos = {"lado": "V", "ent": cl, "stop": stop, "alvo": cl - alvo_mult * R, "hora": dt}
                continue
            saiu = None
            if pos["lado"] == "C":
                if lo <= pos["stop"]:
                    saiu = (pos["stop"], "stop")
                elif hi >= pos["alvo"]:
                    saiu = (pos["alvo"], "alvo")
            else:
                if hi >= pos["stop"]:
                    saiu = (pos["stop"], "stop")
                elif lo <= pos["alvo"]:
                    saiu = (pos["alvo"], "alvo")
            if saiu is None and t >= lim:
                saiu = (cl, "horario")
            if saiu:
                pos["saida"], pos["motivo"], pos["hora_saida"] = saiu[0], saiu[1], dt
                break
        if pos is None:
            sem_trade += 1
            continue
        if "saida" not in pos:  # dados acabaram antes do horário limite
            pos["saida"], pos["motivo"], pos["hora_saida"] = cs[-1][4], "fim_dados", cs[-1][0]
        sinal = 1 if pos["lado"] == "C" else -1
        pts = (pos["saida"] - pos["ent"]) * sinal
        pos.update(dia=dia, range=R, pts=pts,
                   rs=pts * vp * contratos - custo * contratos,
                   r=pts / abs(pos["ent"] - pos["stop"]))
        trades.append(pos)
    return trades, sem_trade


def metricas(trades, sem_trade):
    n = len(trades)
    if not n:
        return {"trades": 0, "dias_sem_trade": sem_trade}
    g = [t["rs"] for t in trades if t["rs"] > 0]
    p = [t["rs"] for t in trades if t["rs"] <= 0]
    pico = acum = dd = 0.0
    for t in trades:
        acum += t["rs"]
        pico = max(pico, acum)
        dd = max(dd, pico - acum)
    return {
        "trades": n, "dias_sem_trade": sem_trade,
        "acerto_pct": round(100 * len(g) / n, 1),
        "resultado_rs": round(acum, 2),
        "expectativa_rs": round(acum / n, 2),
        "expectativa_r": round(sum(t["r"] for t in trades) / n, 2),
        "fator_lucro": round(sum(g) / abs(sum(p)), 2) if p and sum(p) else None,
        "drawdown_max_rs": round(dd, 2),
        "saidas": {m: sum(1 for t in trades if t["motivo"] == m)
                   for m in ("alvo", "stop", "horario", "fim_dados")},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("csv")
    ap.add_argument("--ativo", required=True, choices=["WIN", "WDO"], type=str.upper)
    ap.add_argument("--inicio", default="09:00")
    ap.add_argument("--janela", type=int, default=30)
    ap.add_argument("--stop", default="meio", choices=["meio", "oposto"])
    ap.add_argument("--alvo", type=float, default=1.0)
    ap.add_argument("--saida", default="12:00")
    ap.add_argument("--custo", type=float, default=0.0, help="R$ por contrato por trade (ida e volta)")
    ap.add_argument("--contratos", type=int, default=1)
    ap.add_argument("--de")
    ap.add_argument("--ate")
    ap.add_argument("--grade", action="store_true")
    ap.add_argument("--trades", help="grava os trades simulados neste CSV")
    a = ap.parse_args()

    dias = carregar(a.csv)
    if a.de:
        dias = OrderedDict((d, c) for d, c in dias.items() if str(d) >= a.de)
    if a.ate:
        dias = OrderedDict((d, c) for d, c in dias.items() if str(d) <= a.ate)
    if not dias:
        sys.exit("Nenhum dado no período.")
    print(f"{a.ativo} · {len(dias)} dias ({min(dias)} a {max(dias)}) · custo R$ {a.custo}/contrato · "
          f"{a.contratos} contrato(s) · saída até {a.saida}")
    if len(dias) < 100:
        print("AVISO: menos de 100 dias, amostra fraca.")

    if a.grade:
        res = []
        for jan in (15, 30):
            for st in ("meio", "oposto"):
                for alv in (1.0, 1.5, 2.0):
                    tr, st_ = simular(dias, a.ativo, a.inicio, jan, st, alv, a.saida, a.custo, a.contratos)
                    res.append(((jan, st, alv), metricas(tr, st_)))
        res.sort(key=lambda x: x[1].get("expectativa_rs", float("-inf")), reverse=True)
        print(f"\n{'janela':>6} {'stop':>7} {'alvo':>5} {'trades':>7} {'acerto%':>8} "
              f"{'result R$':>11} {'exp R$':>8} {'exp R':>6} {'FL':>5} {'DD R$':>9}")
        for (jan, st, alv), m in res:
            if not m["trades"]:
                continue
            fl = "-" if m["fator_lucro"] is None else f"{m['fator_lucro']:.2f}"
            print(f"{jan:>6} {st:>7} {alv:>5.1f} {m['trades']:>7} {m['acerto_pct']:>8.1f} "
                  f"{m['resultado_rs']:>11.2f} {m['expectativa_rs']:>8.2f} {m['expectativa_r']:>6.2f} "
                  f"{fl:>5} {m['drawdown_max_rs']:>9.2f}")
        print("\nAVISO: o melhor da grade tende a piorar fora da amostra (overfitting). Valide com --de/--ate.")
        return

    trades, sem = simular(dias, a.ativo, a.inicio, a.janela, a.stop, a.alvo, a.saida, a.custo, a.contratos)
    print(f"Parâmetros: janela {a.janela} min a partir de {a.inicio}, stop {a.stop}, alvo {a.alvo}× range\n")
    for k, v in metricas(trades, sem).items():
        print(f"  {k:<16}{'-' if v is None else v}")
    if a.trades:
        with open(a.trades, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["data", "hora_entrada", "hora_saida", "lado", "entrada", "stop", "alvo",
                        "saida", "motivo", "range", "pontos", "resultado_rs", "r"])
            for t in trades:
                w.writerow([t["dia"], t["hora"].strftime("%H:%M"), t["hora_saida"].strftime("%H:%M"),
                            t["lado"], t["ent"], round(t["stop"], 2), round(t["alvo"], 2), t["saida"],
                            t["motivo"], t["range"], round(t["pts"], 2), round(t["rs"], 2), round(t["r"], 2)])
        print(f"\nTrades gravados em {a.trades}")


if __name__ == "__main__":
    main()
