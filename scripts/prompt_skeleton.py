#!/usr/bin/env python3
"""Esqueleto de prompt con marcas de tiempo a partir del timeline.json del blockout.

Uso:
  python scripts/prompt_skeleton.py <timeline.json> --model kling|seedance [--refs refs.json] [--out prompt.md]

refs.json (opcional): referencias de producción y el tramo en que actúa cada una, p. ej.
  [{"tag": "@sala", "defines": "the room", "from": 0, "to": 8},
   {"tag": "@persona_a", "defines": "appearance of Persona A ONLY", "from": 0, "to": 8}]

El esqueleto deja marcadores <…> para que la skill los rellene con la biblia. No inventa
contenido: solo estructura tiempos, cortes, keyframes, referencias y audio por tramo.
  kling    → plano continuo guiado por keyframes (start, intermedios, end) con la sintaxis
             oficial de Kling «X–Y sec | Keyframe N:». Sin video de referencia: Kling 4.0
             no lee bien los blockouts (prueba de Thomas Lundström, oct-2026).
  seedance → secciones con blockout como video de referencia, bloque Video lock y CUT por plano.
"""
import argparse
import json
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
    p.add_argument("--model", choices=["kling", "seedance"], required=True)
    p.add_argument("--refs", default=None)
    p.add_argument("--out", default=None)
    a = p.parse_args()
    with open(a.timeline, encoding="utf-8") as f:
        tl = json.load(f)
    refs = json.load(open(a.refs, encoding="utf-8")) if a.refs else []
    lines = kling(tl, refs) if a.model == "kling" else seedance(tl, refs)
    text = "\n".join(lines) + "\n"
    if a.out:
        with open(a.out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"OK → {a.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
