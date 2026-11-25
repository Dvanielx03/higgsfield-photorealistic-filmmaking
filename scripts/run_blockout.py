#!/usr/bin/env python3
"""Un solo comando: plan.json → blockout de Blender → esqueletos de prompt para las rutas K y S.

Uso:
  python scripts/run_blockout.py <plan.json> <carpeta_salida> [--blender <ruta>] [--refs refs.json] [--no-video]

Pasos:
  1. Busca Blender (variable BLENDER, PATH, o la instalación más reciente en las rutas habituales).
  2. Ejecuta scripts/blockout/build_blockout.py sin interfaz → .blend, blockout.mp4, keyframes/, plates/, timeline.json.
  3. Genera fichas/kling.md y fichas/seedance.md con scripts/prompt_skeleton.py.
No genera nada en Higgsfield ni gasta créditos: deja todo listo para la ficha, la cotización y el sí del usuario.
"""
import argparse
import glob
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def find_blender(explicit):
    cands = [explicit, os.environ.get("BLENDER"), shutil.which("blender")]
    cands += sorted(glob.glob(r"C:\Program Files\Blender Foundation\Blender *\blender.exe"), reverse=True)
    cands += ["/Applications/Blender.app/Contents/MacOS/Blender", "/usr/bin/blender", "/snap/bin/blender"]
    for c in cands:
        if c and os.path.isfile(c):
            return c
    sys.exit("No encontré Blender. Pasa --blender <ruta> o define la variable BLENDER.")


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("plan")
    p.add_argument("out")
    p.add_argument("--blender", default=None)
    p.add_argument("--refs", default=None)
    p.add_argument("--no-video", action="store_true")
    a = p.parse_args()

    blender = find_blender(a.blender)
    os.makedirs(a.out, exist_ok=True)
    cmd = [blender, "-b", "--factory-startup", "-P", os.path.join(HERE, "blockout", "build_blockout.py"),
           "--", os.path.abspath(a.plan), os.path.abspath(a.out)]
    if a.no_video:
        cmd.append("--no-video")
    print(f"Blender: {blender}")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or "OK blockout" not in r.stdout:
        print(r.stdout[-3000:], r.stderr[-3000:], sep="\n")
        sys.exit("Falló la construcción del blockout.")
    print("Blockout listo.")

    timeline = os.path.join(a.out, "timeline.json")
    fichas = os.path.join(a.out, "fichas")
    os.makedirs(fichas, exist_ok=True)
    for model in ("kling", "kling-shots", "seedance"):
        sk = [sys.executable, os.path.join(HERE, "prompt_skeleton.py"), timeline, "--model", model,
              "--out", os.path.join(fichas, f"{model}.md")]
        if a.refs and model == "seedance":
            sk += ["--refs", a.refs]
        if subprocess.run(sk).returncode != 0:  # un modelo que no aplica (p. ej. 1 keyframe) no tumba el resto
            print(f"Aviso: no se generó la ficha de {model}; revisa los keyframes del plan.")
    print(f"Listo → {os.path.abspath(a.out)}")
    print("Siguiente: keyframes fotorrealistas (ruta K) o referencias (ruta S), rellenar fichas, cotizar y pedir el sí.")


if __name__ == "__main__":
    main()
