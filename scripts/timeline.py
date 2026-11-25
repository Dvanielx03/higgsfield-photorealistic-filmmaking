#!/usr/bin/env python3
"""Marcas de tiempo para referencias y control de calidad (requiere ffmpeg y ffprobe en el PATH).

Uso:
  python timeline.py cuts      <video> [--threshold 0.3]
      Lista los cortes detectados (segundos) y la duración de cada plano.

  python timeline.py breakdown <video> <carpeta_salida> [--threshold 0.3]
      Desglose de una referencia: un fotograma por plano (en su punto medio) y
      <carpeta>/desglose.md con la tabla de timecodes lista para anotar.

  python timeline.py trim      <video_o_audio> <inicio_s> <fin_s> <salida>
      Recorta un tramo exacto (re-codifica para precisión de fotograma) antes de
      subirlo como video_references o audio_references.

  python timeline.py drift     <video> <cortes_planeados> [--tolerance 0.8] [--threshold 0.3]
      Compara los cortes planeados (p. ej. "3,6,10") con los detectados y marca
      los que se desvían más que la tolerancia (por defecto 0,8 s, el margen de la skill).
"""
import argparse
import json
import os
import re
import subprocess
import sys


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def duration(path):
    r = run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", path])
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        sys.exit(f"No pude leer la duración de {path}: {r.stderr.strip()}")


def detect_cuts(path, threshold):
    r = run(["ffmpeg", "-hide_banner", "-i", path, "-vf",
             f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"])
    times = [float(m) for m in re.findall(r"pts_time:([0-9.]+)", r.stderr)]
    # Elimina detecciones pegadas (< 0,25 s) que suelen ser el mismo corte.
    cuts = []
    for t in times:
        if not cuts or t - cuts[-1] >= 0.25:
            cuts.append(round(t, 2))
    return cuts


def tc(t):
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


def shots_from_cuts(cuts, total):
    edges = [0.0] + cuts + [round(total, 2)]
    return [(edges[i], edges[i + 1]) for i in range(len(edges) - 1) if edges[i + 1] - edges[i] > 0.04]


def cmd_cuts(a):
    total = duration(a.video)
    cuts = detect_cuts(a.video, a.threshold)
    print(f"Duración: {total:.2f} s · cortes detectados: {len(cuts)} (umbral {a.threshold})")
    for i, (s, e) in enumerate(shots_from_cuts(cuts, total), 1):
        print(f"P{i:02d}  {tc(s)} → {tc(e)}  ({e - s:.2f} s)")


def cmd_breakdown(a):
    os.makedirs(a.outdir, exist_ok=True)
    total = duration(a.video)
    shots = shots_from_cuts(detect_cuts(a.video, a.threshold), total)
    rows = []
    for i, (s, e) in enumerate(shots, 1):
        mid = (s + e) / 2
        img = os.path.join(a.outdir, f"P{i:02d}_{mid:06.2f}s.jpg")
        run(["ffmpeg", "-v", "error", "-y", "-ss", f"{mid:.3f}", "-i", a.video,
             "-frames:v", "1", "-vf", "scale=-2:360", img])
        rows.append((i, s, e, os.path.basename(img)))
    md = os.path.join(a.outdir, "desglose.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write(f"# Desglose de referencia · {os.path.basename(a.video)}\n\n")
        f.write(f"Duración {total:.2f} s · {len(rows)} planos detectados (umbral {a.threshold}). "
                "Revisar a ojo: los fundidos y los movimientos rápidos pueden dar cortes falsos o perdidos.\n\n")
        f.write("| Plano | Entra | Sale | Dur. | Fotograma | Tamaño / ángulo | Movimiento | Qué pasa | Texto / gráfico | Audio (música · efectos · ambiente · diálogo · silencio) | Técnica en Higgsfield | ¿Lo tomamos? |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|---|---|\n")
        for i, s, e, img in rows:
            f.write(f"| P{i:02d} | {tc(s)} | {tc(e)} | {e - s:.2f} s | ![]({img}) | | | | | | | |\n")
    print(f"OK → {md} ({len(rows)} planos)")


def cmd_trim(a):
    if a.end <= a.start:
        sys.exit("El fin debe ser mayor que el inicio.")
    is_audio = os.path.splitext(a.output)[1].lower() in (".mp3", ".wav", ".m4a", ".aac", ".flac", ".ogg")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a.start}", "-to", f"{a.end}", "-i", a.media]
    cmd += (["-vn"] if is_audio else ["-c:v", "libx264", "-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac"])
    cmd.append(a.output)
    r = run(cmd)
    if r.returncode != 0:
        sys.exit(r.stderr.strip())
    print(f"OK → {a.output} ({duration(a.output):.2f} s; pedido {a.end - a.start:.2f} s)")


def cmd_drift(a):
    planned = [float(x) for x in a.planned.replace(";", ",").split(",") if x.strip()]
    cuts = detect_cuts(a.video, a.threshold)
    if not cuts:
        sys.exit("No se detectaron cortes: bajar --threshold o revisar a ojo.")
    worst = 0.0
    print(f"Tolerancia ±{a.tolerance:.2f} s · cortes detectados: {', '.join(f'{c:.2f}' for c in cuts)}")
    for p in planned:
        near = min(cuts, key=lambda c: abs(c - p))
        d = near - p
        worst = max(worst, abs(d))
        flag = "OK" if abs(d) <= a.tolerance else "FUERA"
        print(f"  planeado {p:6.2f} s → detectado {near:6.2f} s  (desvío {d:+.2f} s)  {flag}")
    extra = len(cuts) - len(planned)
    if extra:
        print(f"  Aviso: {'sobran' if extra > 0 else 'faltan'} {abs(extra)} corte(s) respecto al plan.")
    print(f"Peor desvío: {worst:.2f} s")


def main():
    # La consola de Windows usa cp1252 por defecto; forzar UTF-8 para las flechas y acentos.
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("cuts"); c.add_argument("video"); c.add_argument("--threshold", type=float, default=0.3)
    b = sub.add_parser("breakdown"); b.add_argument("video"); b.add_argument("outdir"); b.add_argument("--threshold", type=float, default=0.3)
    t = sub.add_parser("trim"); t.add_argument("media"); t.add_argument("start", type=float); t.add_argument("end", type=float); t.add_argument("output")
    d = sub.add_parser("drift"); d.add_argument("video"); d.add_argument("planned")
    d.add_argument("--tolerance", type=float, default=0.8); d.add_argument("--threshold", type=float, default=0.3)
    a = p.parse_args()
    {"cuts": cmd_cuts, "breakdown": cmd_breakdown, "trim": cmd_trim, "drift": cmd_drift}[a.cmd](a)


if __name__ == "__main__":
    main()
