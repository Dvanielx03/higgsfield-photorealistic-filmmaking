#!/usr/bin/env python3
"""Esqueleto de prompt con marcas de tiempo a partir del timeline.json del blockout.

Uso:
  python scripts/prompt_skeleton.py <timeline.json> --model kling|seedance [--refs refs.json] [--out prompt.md]

refs.json (opcional): referencias de producción y el tramo en que actúa cada una, p. ej.
  [{"tag": "@sala", "defines": "the room", "from": 0, "to": 8},
   {"tag": "@persona_a", "defines": "appearance of Persona A ONLY", "from": 0, "to": 8}]

El esqueleto deja marcadores <…> para que la skill los rellene con la biblia. No inventa
contenido: solo estructura tiempos, cortes, keyframes, referencias y audio por tramo.
  kling-shots → una generación de Kling por plano (secciones con cortes), con los keyframes de cada plano.
  kling    → plano continuo guiado por keyframes (start, intermedios, end) con la sintaxis
             oficial de Kling «X–Y sec | Keyframe N:». Sin video de referencia: Kling 4.0
             no lee bien los blockouts (prueba de Thomas Lundström, oct-2026).
  seedance → secciones con blockout como video de referencia, bloque Video lock y CUT por plano.
"""
import argparse
import json
import math
import sys

AUDIO_EN = {
    "silencio": "silence", "ambiente": "ambience", "efectos": "sound effects",
    "dialogo": "dialogue", "diálogo": "dialogue", "musica": "music", "música": "music",
}


def fmt(t):
    m, s = divmod(float(t), 60)
    return f"{int(m)}:{s:05.2f}"


def audio_for(timeline, a, b):
    parts = []
    for seg in timeline.get("audio", []):
        if seg["start"] < b and seg["end"] > a:
            kind = AUDIO_EN.get(seg["type"].lower(), seg["type"])
            if kind == "music" and "post" in seg.get("desc", "").lower():
                continue  # la música en post no entra en el prompt
            parts.append(f"{kind}: {seg.get('desc', '<…>')}")
    return "; ".join(parts) if parts else "practical sound only"


def wants_model_music(timeline):
    return any(AUDIO_EN.get(s["type"].lower()) == "music" and "post" not in s.get("desc", "").lower()
               for s in timeline.get("audio", []))


def refs_block(refs):
    if not refs:
        return ["References:", "<@tag — what it defines ONLY, for <from>–<to> only. Not its background or layout.>"]
    out = ["References:"]
    for r in refs:
        out.append(f"{r['tag']} — {r.get('defines', '<what it defines>')}, for {fmt(r['from'])}–{fmt(r['to'])} only.")
    return out


def audio_line(timeline):
    if wants_model_music(timeline):
        return "Audio: per segment as written below. Music only where a segment asks for it."
    return "Audio: No music and no score. Sound per segment as written below."


def kling(tl, refs):
    kfs = tl.get("keyframes", [])
    if len(kfs) < 2:
        sys.exit("Kling necesita al menos 2 keyframes (inicio y fin) en el timeline.")
    d = tl["duration"]
    L = [f"Model: kling4_0 · mode: image-to-video · duration: {round(d)} s · aspect {tl.get('aspect', '9:16')}",
         f"Media: start_image = KF01 · image_references (in order) = "
         + ", ".join(f"KF{k['index']:02d}" for k in kfs[1:-1]) + f" · end_image = KF{kfs[-1]['index']:02d}",
         "(Kling 4.0 does not combine Keyframes with Omni Reference: no reference video, no extra reference images.)",
         "",
         f"One single continuous {round(d)}-second take with no cuts, no transitions and no scene changes. "
         + ("Camera: " + "; then ".join(f"{sh['move']}" for sh in tl['shots'] if sh.get('move')) + ". " if any(sh.get('move') for sh in tl['shots']) else "<Camera behaviour: rig, speed, grade>. ") + "<Fixed character description from the bible>.",
         audio_line(tl), ""]
    for a, b in zip(kfs, kfs[1:]):
        L.append(f"{a['t']:.2f}–{b['t']:.2f} sec | Keyframe {a['index']} → Keyframe {b['index']}: "
                 f"<camera move and action that carries frame {a['index']} into frame {b['index']}>. "
                 f"Sound: {audio_for(tl, a['t'], b['t'])}.")
    L += ["", "No subtitles. No background music." if not wants_model_music(tl) else "No subtitles."]
    return L


MIN_KF_GAP = 1.0  # production/blender-kling-seedance.md §6b: entre dos keyframes de Kling, 1–3 s


def thin_keyframes(inside, gap=MIN_KF_GAP):
    """Inicio y fin siempre; un intermedio solo si queda a ≥ gap s de sus vecinos. Los descartados no se suben:
    quedan como acciones dentro del tramo (su keyframe sirve de guía visual para escribir el prompt)."""
    if len(inside) <= 2:
        return inside, []
    chosen, skipped = [inside[0]], []
    for k in inside[1:-1]:
        (chosen if k["t"] - chosen[-1]["t"] >= gap and inside[-1]["t"] - k["t"] >= gap else skipped).append(k)
    return chosen + [inside[-1]], skipped


def kling_per_shot(tl, refs):
    """Ruta K para secciones con cortes: Kling 4.0 hace tomas continuas, así que va una generación por plano.
    Cada plano usa los keyframes que caen dentro de él (inicio = start_image, fin = end_image), aclarados a 1–3 s."""
    kfs = tl.get("keyframes", [])
    L = [f"# Ruta K · una generación de Kling 4.0 por plano · aspect {tl.get('aspect', '9:16')}",
         "(Kling 4.0 no lee blockouts ni combina Keyframes con Omni Reference: la cámara y la identidad viven en los keyframes.)",
         "(Duración mínima de Kling: 3 s. Un plano más corto se genera a 3 s y se recorta en montaje cortando en movimiento.)", ""]
    for sh in tl["shots"]:
        # fin exclusivo: el fotograma en t = fin ya es el primero del plano siguiente (otra cámara)
        inside = [k for k in kfs if sh["start"] - 1e-6 <= k["t"] < sh["end"] - 1e-6]
        dur = sh["end"] - sh["start"]
        gen = max(3, math.ceil(dur))
        L.append(f"## {sh['id']} · {fmt(sh['start'])}–{fmt(sh['end'])} del clip · usa {dur:.2f} s · generar {gen} s")
        if len(inside) < 2:
            L.append(f"FALTAN KEYFRAMES: este plano necesita al menos inicio y fin (usa auto_keyframes en el plan).")
            L.append("")
            continue
        inside, beats = thin_keyframes(inside)
        L.append(f"Media: start_image = KF{inside[0]['index']:02d}"
                 + (" · image_references (in order) = " + ", ".join(f"KF{k['index']:02d}" for k in inside[1:-1]) if len(inside) > 2 else "")
                 + f" · end_image = KF{inside[-1]['index']:02d}")
        size = sh.get("size") or "<shot size>"
        move = sh.get("move") or "<movement>"
        if sh.get("handheld"):
            move += ", subtle handheld"
        L.append(f"One single continuous {gen}-second take, no cuts. {size}, {sh.get('lens_mm', 35)} mm. Camera: {move}. "
                 "<Fixed character description from the bible>.")
        for a, b in zip(inside, inside[1:]):
            ta, tb = a["t"] - sh["start"], b["t"] - sh["start"]
            mid = "".join(f" At {k['t'] - sh['start']:.2f} sec: <action shown in KF{k['index']:02d}>." for k in beats
                          if a["t"] < k["t"] < b["t"])
            L.append(f"{ta:.2f}–{tb:.2f} sec | Keyframe {a['index']} → Keyframe {b['index']}: "
                     f"<action that carries frame {a['index']} into frame {b['index']}>.{mid} Sound: {audio_for(tl, a['t'], b['t'])}.")
        L += ["No subtitles. No background music." if not wants_model_music(tl) else "No subtitles.", ""]
    return L


def seedance(tl, refs):
    d = tl["duration"]
    key = tl.get("blockout_key", [])
    L = [f"Model: seedance_2_5 · mode: omni_reference · duration: {round(d)} s · aspect {tl.get('aspect', '9:16')} · draft: true",
         "Media order: image_references (plate → set → characters → props) → video_references (blockout) → audio_references",
         "",
         "Style: Photorealistic live-action, shot like a feature film. NOT 3D-render, no game engine.",
         "<Lighting from the bible> <Color from the bible> <Camera: physical cine lenses, 180° shutter, 24fps>",
         audio_line(tl), ""]
    L += refs_block(refs)
    L += ["",
          f"@Video 1 · {round(d)}s — camera movement, cuts and timing ONLY, 1:1 frame-aligned. It is a coarse grey previz: "
          "not colour, not materials, not the environment.",
          "Video lock: @Video 1 is the SOLE authority for camera movement, cuts and timing. The previz is re-dressed, never re-imagined. Decode it like this:"]
    for k in key:
        L.append(f"- The {k['blockout']} in @Video 1 is <@{k['tag']}> ({k['label']}). "
                 "It carries no body motion: give natural human movement that keeps its position, path, speed and facing."
                 if k["kind"] == "persona" else
                 f"- The {k['blockout']} in @Video 1 is <@{k['tag']}> ({k['label']}).")
    L.append("- The grey volumes are placeholders for the set in the references. Replace them entirely.")
    n = len(tl["shots"])
    L += ["", f"There are exactly {n} shots (CUT 1 to CUT {n}), in this order, each cutting where @Video 1 cuts. "
              "Never add or drop a shot.", ""]
    for i, sh in enumerate(tl["shots"], 1):
        size = sh.get("size") or "<shot size>"
        move = sh.get("move") or "<movement>"
        if sh.get("handheld"):
            move += ", subtle handheld"
        L.append(f"CUT {i} ({fmt(sh['start'])}–{fmt(sh['end'])}) — {size}, {sh.get('lens_mm', 35)} mm, {move}: "
                 f"<how many people in frame>. <one concrete action>. <face>. "
                 f"Sound: {audio_for(tl, sh['start'], sh['end'])}.")
    L += ["", "Hold: <characters, props, sky and light that stay the same throughout>."]
    return L


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("timeline")
    p.add_argument("--model", choices=["kling", "kling-shots", "seedance"], required=True)
    p.add_argument("--refs", default=None)
    p.add_argument("--out", default=None)
    a = p.parse_args()
    with open(a.timeline, encoding="utf-8") as f:
        tl = json.load(f)
    refs = json.load(open(a.refs, encoding="utf-8")) if a.refs else []
    lines = {"kling": kling, "kling-shots": kling_per_shot, "seedance": seedance}[a.model](tl, refs)
    text = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"OK → {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
