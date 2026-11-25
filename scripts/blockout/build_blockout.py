"""Blockout automático en Blender a partir de un plan JSON.

Uso (sin abrir la interfaz de Blender):
  blender -b -P scripts/blockout/build_blockout.py -- <plan.json> <carpeta_salida> [--no-video] [--no-stills]

Genera en <carpeta_salida>:
  blockout.blend        escena editable (para ajustar a mano o con el MCP de Blender)
  blockout.mp4          previz gris a preview_scale (video_references de Seedance 2.5)
  keyframes/KF##_<t>s.png   fotogramas clave a resolución completa (base de los keyframes de Kling 4.0)
  plates/<plano>_plate.png  primer fotograma de cada plano sin personas ni props (base de las referencias de set)
  timeline.json         cortes, lentes, keyframes, clave de colores y audio por tramo

Convenciones del blockout (van al bloque «Blockout key» del prompt):
  persona = cápsula del color del plan + esfera de cabeza color piel + cono que marca hacia dónde mira
  prop    = caja del color del plan · set = volúmenes grises
Requiere Blender 4.2+ (probado en 5.2) y ffmpeg en el PATH para montar el MP4.
"""
import bpy
import json
import math
import os
import shutil
import subprocess
import sys

SKIN = (0.85, 0.66, 0.53, 1.0)
COLOR_NAMES = {
    "red": (0.8, 0.1, 0.1), "orange": (0.9, 0.45, 0.1), "yellow": (1.0, 0.85, 0.0),
    "green": (0.1, 0.65, 0.2), "cyan": (0.1, 0.75, 0.85), "blue": (0.1, 0.25, 0.85),
    "purple": (0.5, 0.2, 0.75), "magenta": (0.9, 0.1, 0.6), "white": (0.95, 0.95, 0.95),
    "grey": (0.5, 0.5, 0.5), "black": (0.05, 0.05, 0.05), "brown": (0.45, 0.28, 0.15),
}


def color_name(rgb):
    return min(COLOR_NAMES, key=lambda n: sum((a - b) ** 2 for a, b in zip(rgb[:3], COLOR_NAMES[n])))


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) < 2:
        sys.exit("Uso: blender -b -P build_blockout.py -- <plan.json> <carpeta_salida> [--no-video] [--no-stills]")
    return argv[0], argv[1], "--no-video" not in argv, "--no-stills" not in argv


def frame(t, fps):
    return int(round(t * fps)) + 1


def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene


def material_free_color(obj, rgb):
    c = tuple(rgb) + ((1.0,) if len(rgb) == 3 else ())
    obj.color = c


def add_box(name, size, loc, rgb, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    material_free_color(o, rgb)
    if parent:
        o.parent = parent
    return o


def add_person(sid, rgb, height):
    root = bpy.data.objects.new(f"{sid}_root", None)
    bpy.context.scene.collection.objects.link(root)
    body_h = height * 0.82
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=body_h, location=(0, 0, body_h / 2))
    body = bpy.context.active_object
    body.name = f"{sid}_body"
    material_free_color(body, rgb)
    body.parent = root
    head_r = height * 0.075
    bpy.ops.mesh.primitive_uv_sphere_add(radius=head_r, location=(0, 0, body_h + head_r))
    head = bpy.context.active_object
    head.name = f"{sid}_head"
    head.color = SKIN
    head.parent = root
    # Cono de dirección: apunta a -Y local (hacia donde mira la persona).
    bpy.ops.mesh.primitive_cone_add(radius1=0.07, depth=0.18, location=(0, -0.24, body_h * 0.85),
                                    rotation=(math.radians(90), 0, 0))
    nose = bpy.context.active_object
    nose.name = f"{sid}_facing"
    material_free_color(nose, (0.05, 0.05, 0.05))
    nose.parent = root
    return root, [body, head, nose]


def key_track(obj, keys, fps, with_yaw=False):
    for k in keys:
        f = frame(k["t"], fps)
        obj.location = k["pos"]
        obj.keyframe_insert("location", frame=f)
        if with_yaw:
            obj.rotation_euler = (0, 0, math.radians(k.get("yaw", 0)))
            obj.keyframe_insert("rotation_euler", frame=f)


def fcurves_of(obj):
    """F-curves de un objeto, compatible con la API clásica y con las acciones por capas (Blender 4.4+/5.x)."""
    ad = obj.animation_data
    if not ad or not ad.action:
        return []
    act = ad.action
    try:
        return list(act.fcurves)
    except Exception:
        pass
    out = []
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for cb in getattr(strip, "channelbags", []):
                out += list(cb.fcurves)
    return out


def add_handheld(cam, target, amplitude, n_keys, fps):
    """Cámara en mano sutil: ruido en la posición de la cámara y, más fuerte, en el punto de mira."""
    for obj, amp, seed in ((target, amplitude, 1.0), (cam, amplitude * 0.4, 7.0)):
        if n_keys < 2:  # con una sola clave no hay F-curve animada: se crea una segunda igual
            obj.keyframe_insert("location", frame=bpy.context.scene.frame_end)
        for fc in fcurves_of(obj):
            if fc.data_path != "location":
                continue
            mod = fc.modifiers.new("NOISE")
            mod.scale = fps * 0.6
            mod.strength = amp
            mod.phase = seed + fc.array_index * 13.0


def setup_render(scene, plan):
    w, h = plan.get("resolution", [1080, 1920])
    scene.render.engine = "BLENDER_WORKBENCH"
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.fps = plan.get("fps", 24)
    scene.frame_start = 1
    scene.frame_end = frame(plan["duration"], scene.render.fps) - 1
    sh = scene.display.shading
    sh.light = "STUDIO"
    sh.color_type = "OBJECT"
    sh.show_shadows = True
    sh.show_cavity = True
    scene.render.image_settings.file_format = "PNG"
    world = bpy.data.worlds.new("previz")
    world.color = (0.12, 0.12, 0.12)
    scene.world = world


def build(plan):
    scene = reset_scene()
    setup_render(scene, plan)
    fps = scene.render.fps

    st = plan.get("set", {})
    set_rgb = st.get("color", [0.55, 0.55, 0.55])
    for b in st.get("boxes", []):
        add_box(f"set_{b['name']}", b["size"], b["location"], b.get("color", set_rgb))

    hideable = []
    key_colors = []
    for s in plan.get("subjects", []):
        root, parts = add_person(s["id"], s["color"], s.get("height", 1.75))
        key_track(root, s["keys"], fps, with_yaw=True)
        hideable += [root] + parts
        key_colors.append({"tag": s["id"], "label": s.get("label", s["id"]), "kind": "persona",
                           "blockout": f"{color_name(s['color'])} capsule with a skin-coloured sphere head "
                                       "and a small black cone showing which way it faces"})
    for p in plan.get("props", []):
        o = add_box(f"prop_{p['id']}", p["size"], p["keys"][0]["pos"], p["color"])
        key_track(o, p["keys"], fps)
        hideable.append(o)
        key_colors.append({"tag": p["id"], "label": p.get("label", p["id"]), "kind": "prop",
                           "blockout": f"small {color_name(p['color'])} box"})

    cams = {}
    for sh in plan["shots"]:
        cdata = bpy.data.cameras.new(f"cam_{sh['id']}")
        cdata.lens = sh.get("lens_mm", 35)
        w, h = plan.get("resolution", [1080, 1920])
        cdata.sensor_fit = "VERTICAL" if h > w else "HORIZONTAL"
        if h > w:
            cdata.sensor_height = 36.0
        else:
            cdata.sensor_width = 36.0
        cam = bpy.data.objects.new(f"cam_{sh['id']}", cdata)
        scene.collection.objects.link(cam)
        target = bpy.data.objects.new(f"target_{sh['id']}", None)
        scene.collection.objects.link(target)
        for k in sh["camera"]:
            f = frame(k["t"], fps)
            cam.location = k["pos"]
            cam.keyframe_insert("location", frame=f)
            target.location = k["look_at"]
            target.keyframe_insert("location", frame=f)
        con = cam.constraints.new("TRACK_TO")
        con.target = target
        con.track_axis = "TRACK_NEGATIVE_Z"
        con.up_axis = "UP_Y"
        hh = float(sh.get("handheld", 0) or 0)
        if hh > 0:
            add_handheld(cam, target, hh, len(sh["camera"]), fps)
        m = scene.timeline_markers.new(sh["id"], frame=frame(sh["start"], fps))
        m.camera = cam
        cams[sh["id"]] = cam
    scene.camera = cams[plan["shots"][0]["id"]]
    return scene, cams, hideable, key_colors


def aspect_of(res):
    w, h = res
    for name, r in (("16:9", 16 / 9), ("9:16", 9 / 16), ("1:1", 1.0), ("4:5", 0.8), ("21:9", 21 / 9), ("4:3", 4 / 3)):
        if abs(w / h - r) < 0.02:
            return name
    return f"{w}:{h}"


def shot_at(plan, t):
    for sh in plan["shots"]:
        if sh["start"] <= t < sh["end"]:
            return sh
    return plan["shots"][-1]


def render_still(scene, path):
    scene.render.filepath = path
    bpy.ops.render.render(write_still=True)


def main():
    plan_path, out, do_video, do_stills = args()
    with open(plan_path, encoding="utf-8") as f:
        plan = json.load(f)
    os.makedirs(out, exist_ok=True)
    scene, cams, hideable, key_colors = build(plan)
    fps = scene.render.fps
    bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(os.path.join(out, "blockout.blend")))

    keyframes_out = []
    if do_stills:
        os.makedirs(os.path.join(out, "keyframes"), exist_ok=True)
        for i, t in enumerate(plan.get("keyframes", []), 1):
            sh = shot_at(plan, t)
            scene.frame_set(frame(t, fps))
            scene.camera = cams[sh["id"]]
            p = os.path.join(out, "keyframes", f"KF{i:02d}_{t:05.2f}s.png")
            render_still(scene, os.path.abspath(p))
            keyframes_out.append({"index": i, "t": t, "shot": sh["id"], "file": os.path.relpath(p, out)})
        os.makedirs(os.path.join(out, "plates"), exist_ok=True)
        for o in hideable:
            o.hide_render = True
        for sh in plan["shots"]:
            scene.frame_set(frame(sh["start"], fps))
            scene.camera = cams[sh["id"]]
            render_still(scene, os.path.abspath(os.path.join(out, "plates", f"{sh['id']}_plate.png")))
        for o in hideable:
            o.hide_render = False

    video_file = None
    if do_video:
        frames_dir = os.path.abspath(os.path.join(out, "_frames"))
        os.makedirs(frames_dir, exist_ok=True)
        scale = plan.get("preview_scale", 0.6667)
        scene.render.resolution_percentage = int(round(scale * 100))
        scene.camera = cams[plan["shots"][0]["id"]]
        scene.render.filepath = os.path.join(frames_dir, "f_")
        bpy.ops.render.render(animation=True)
        scene.render.resolution_percentage = 100
        video_file = "blockout.mp4"
        ff = shutil.which("ffmpeg")
        if ff:
            subprocess.run([ff, "-v", "error", "-y", "-framerate", str(fps), "-start_number", "1",
                            "-i", os.path.join(frames_dir, "f_%04d.png"), "-c:v", "libx264", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",
                            os.path.abspath(os.path.join(out, video_file))], check=True)
            shutil.rmtree(frames_dir, ignore_errors=True)
        else:
            video_file = None
            print("AVISO: ffmpeg no está en el PATH; los fotogramas quedan en _frames/")

    timeline = {
        "name": plan.get("name"),
        "fps": fps,
        "duration": plan["duration"],
        "resolution": plan.get("resolution"),
        "cuts": [sh["start"] for sh in plan["shots"][1:]],
        "aspect": aspect_of(plan.get("resolution", [1080, 1920])),
        "shots": [{"id": sh["id"], "start": sh["start"], "end": sh["end"], "lens_mm": sh.get("lens_mm", 35),
                   "size": sh.get("size"), "move": sh.get("move"), "motivation": sh.get("motivation"),
                   "handheld": sh.get("handheld", 0)}
                  for sh in plan["shots"]],
        "keyframes": keyframes_out,
        "blockout_key": key_colors,
        "audio": plan.get("audio", []),
        "video": video_file,
        "music": plan.get("music"),
    }
    with open(os.path.join(out, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    print(f"OK blockout → {os.path.abspath(out)}")


main()
