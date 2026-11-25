#!/usr/bin/env python3
"""Music-first: detecta pulsos y golpes de una pista y propone cortes que caen en el ritmo.

Uso:
  python scripts/beats.py <musica.mp3|wav> [--duration 30] [--min-shot 1.5] [--cuts 8] [--json salida.json]

Salida: tempo estimado, golpes (onsets) con su fuerza y una lista de cortes sugeridos
(segundos con 2 decimales) que respetan el plano mínimo de la skill (1,5 s por defecto).
Esos cortes se copian a "shots" del plan del blockout para que la previz ya nazca a ritmo.
Requiere ffmpeg en el PATH y numpy. No sustituye el oído: revisar los cortes escuchando.
"""
import argparse
import json
import subprocess
import sys

import numpy as np

SR = 22050
HOP = 512
N_FFT = 2048


def load_mono(path, duration):
    cmd = ["ffmpeg", "-v", "error", "-i", path]
    if duration:
        cmd += ["-t", str(duration)]
    cmd += ["-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    r = subprocess.run(cmd, capture_output=True)
    if r.returncode != 0:
        sys.exit(r.stderr.decode(errors="replace").strip())
    return np.frombuffer(r.stdout, dtype=np.float32)


def onset_envelope(x):
    n_fft = N_FFT
    win = np.hanning(n_fft).astype(np.float32)
    frames = 1 + max(0, (len(x) - n_fft) // HOP)
    if frames < 3:
        sys.exit("Audio demasiado corto.")
    idx = np.arange(n_fft)[None, :] + HOP * np.arange(frames)[:, None]
    spec = np.abs(np.fft.rfft(x[idx] * win, axis=1))
    logspec = np.log1p(spec)
    flux = np.maximum(0.0, np.diff(logspec, axis=0)).sum(axis=1)
    flux = np.concatenate([[0.0], flux])
    flux -= np.convolve(flux, np.ones(16) / 16, mode="same")  # quita la tendencia lenta
    flux = np.maximum(flux, 0.0)
    return flux / (flux.max() or 1.0)


def tempo(env):
    fps = SR / HOP
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    lo, hi = int(fps * 60 / 200), int(fps * 60 / 60)  # 60–200 BPM
    lag = lo + int(np.argmax(ac[lo:hi]))
    # Interpolación parabólica del pico para no quedar atado a la rejilla de fotogramas.
    if 0 < lag < len(ac) - 1:
        y0, y1, y2 = ac[lag - 1], ac[lag], ac[lag + 1]
        den = y0 - 2 * y1 + y2
        if den != 0:
            lag = lag + 0.5 * (y0 - y2) / den
    return 60.0 * fps / lag


def peaks(env, thresh=0.3, min_gap_s=0.12):
    fps = SR / HOP
    gap = max(1, int(min_gap_s * fps))
    out = []
    for i in range(1, len(env) - 1):
        if env[i] >= thresh and env[i] >= env[i - 1] and env[i] > env[i + 1]:
            if not out or i - out[-1] >= gap:
                out.append(i)
            elif env[i] > env[out[-1]]:
                out[-1] = i
    # El fotograma i empieza en i*HOP; su ventana está centrada n_fft/2 muestras después.
    return [((i * HOP + N_FFT // 2) / SR, float(env[i])) for i in out]


def suggest_cuts(onsets, total, min_shot, n_cuts):
    # Los golpes más fuertes primero; se aceptan si dejan planos >= min_shot por ambos lados.
    chosen = []
    for t, s in sorted(onsets, key=lambda o: -o[1]):
        if t < min_shot or total - t < min_shot:
            continue
        if all(abs(t - c) >= min_shot for c in chosen):
            chosen.append(t)
        if n_cuts and len(chosen) >= n_cuts:
            break
    return sorted(round(c, 2) for c in chosen)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("audio")
    p.add_argument("--duration", type=float, default=None, help="usar solo los primeros N segundos")
    p.add_argument("--min-shot", type=float, default=1.5)
    p.add_argument("--cuts", type=int, default=0, help="máximo de cortes sugeridos (0 = sin límite)")
    p.add_argument("--json", default=None)
    a = p.parse_args()

    x = load_mono(a.audio, a.duration)
    total = len(x) / SR
    env = onset_envelope(x)
    bpm = tempo(env)
    ons = peaks(env)
    cuts = suggest_cuts(ons, total, a.min_shot, a.cuts)
    beat = 60.0 / bpm

    print(f"Duración analizada: {total:.2f} s · tempo estimado ≈ {bpm:.1f} BPM (pulso cada {beat:.3f} s)")
    print(f"Golpes detectados: {len(ons)} · los 10 más fuertes:")
    for t, s in sorted(ons, key=lambda o: -o[1])[:10]:
        print(f"  {t:7.2f} s  fuerza {s:.2f}")
    print(f"Cortes sugeridos (plano mínimo {a.min_shot} s): {', '.join(f'{c:.2f}' for c in cuts) or 'ninguno'}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"audio": a.audio, "duration": round(total, 2), "bpm": round(bpm, 2),
                       "beat_s": round(beat, 3),
                       "onsets": [{"t": round(t, 3), "strength": round(s, 3)} for t, s in ons],
                       "suggested_cuts": cuts, "min_shot": a.min_shot}, f, indent=2)
        print(f"OK → {a.json}")


if __name__ == "__main__":
    main()
