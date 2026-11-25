"""Blockout / animatic automático en Blender a partir de un plan JSON.

Uso (sin abrir la interfaz de Blender):
  blender -b -P scripts/blockout/build_blockout.py -- <plan.json> <carpeta_salida> [--no-video] [--no-stills]

Genera en <carpeta_salida>:
  blockout.blend            escena editable (a mano o con el MCP de Blender)
  blockout.mp4              previz a preview_scale (video_references de Seedance 2.5 / revisión del animatic)
  keyframes/KF##_<t>s.png   fotogramas clave a resolución completa (keyframes de Kling 4.0)
  plates/<plano>_plate.png  primer fotograma de cada plano sin personas ni objetos animados (referencias de set)
  timeline.json             cortes, lentes, movimientos, keyframes, clave de colores y audio por tramo

Formato del plan (todas las claves opcionales salvo duration y shots); ver scripts/blockout/plan.example.json:
  engine          "WORKBENCH" (rápido, colores planos) | "EEVEE" (luces reales: dirección, contraluz, pools)
  world_color     color del fondo/ambiente
  set.boxes[]     {name, shape: box|cylinder|sphere|plane, size, location, rotation(grados), color, emission}
  lights[]        {type: AREA|POINT|SPOT|SUN, location, look_at, energy, color, size, keys:[{t, energy, color}], visible}  (solo EEVEE)
  subjects[]      personas: {id, label, color, height, keys:[{t, pos, yaw, head_yaw, head_pitch(+ = mira abajo), height}],
                             hand_keys:[{t, pos(relativa a la persona)}], visible:[[t0,t1],...]}
  objects[]       objetos animados y gráficos: {id, shape: box|cylinder|sphere|cone|plane|text, text, size, location,
                  rotation, color, emission, pivot(bisagra), parent(id de persona), keys:[{t, pos, rot, scale, color}],
                  visible:[[t0,t1],...]}   (props[] se acepta como alias de objects[] con shape box)
  shots[]         {id, start, end, lens_mm, size, move, motivation, handheld(m), dof:{fstop, focus:[{t, distance}]},
                   camera:[{t, pos, look_at, lens}]}
  keyframes[]     segundos para fotogramas clave; auto_keyframes: true añade inicio, centro y fin de cada plano
  audio[]         {start, end, type: silencio|ambiente|efectos|dialogo|musica, desc}

Convenciones (van al bloque «Blockout key» del prompt): persona = cápsula de color + cabeza esfera color piel +
cono negro en la cabeza que marca hacia dónde mira; los demás objetos según su color.
Requiere Blender 4.2+ (probado en 5.2) y ffmpeg en el PATH.
"""
import bpy
import json
import math
import os
import shutil
import subprocess
import sys

SKIN = (0.85, 0.66, 0.53)
COLOR_NAMES = {
    "red": (0.8, 0.1, 0.1), "orange": (0.9, 0.45, 0.1), "yellow": (1.0, 0.85, 0.0),
    "green": (0.1, 0.65, 0.2), "cyan": (0.1, 0.75, 0.85), "blue": (0.1, 0.25, 0.85),
    "purple": (0.5, 0.2, 0.75), "magenta": (0.9, 0.1, 0.6), "white": (0.95, 0.95, 0.95),
    "grey": (0.5, 0.5, 0.5), "black": (0.05, 0.05, 0.05), "brown": (0.45, 0.28, 0.15),
}
ENGINE = "WORKBENCH"


def color_name(rgb):
    return min(COLOR_NAMES, key=lambda n: sum((a - b) ** 2 for a, b in zip(rgb[:3], COLOR_NAMES[n])))


def args():
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    if len(argv) < 2:
        sys.exit("Uso: blender -b -P build_blockout.py -- <plan.json> <carpeta_salida> [--no-video] [--no-stills]")
    return argv[0], argv[1], "--no-video" not in argv, "--no-stills" not in argv


def frame(t, fps):
    return int(round(t * fps)) + 1


def rgba(rgb):
    return tuple(rgb[:3]) + (1.0,)


# ---------- materiales (EEVEE): el color sale del color de objeto, así se puede animar ----------
_MATS = {}


def material(emission=0.0):
    key = round(float(emission), 3)
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new(f"objcolor_e{key}")
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    info = nt.nodes.new("ShaderNodeObjectInfo")
    if key > 0:
        sh = nt.nodes.new("ShaderNodeEmission")
        sh.inputs["Strength"].default_value = key
        nt.links.new(info.outputs["Color"], sh.inputs["Color"])
        nt.links.new(sh.outputs["Emission"], out.inputs["Surface"])
    else:
        sh = nt.nodes.new("ShaderNodeBsdfPrincipled")
        sh.inputs["Roughness"].default_value = 0.6
        nt.links.new(info.outputs["Color"], sh.inputs["Base Color"])
        nt.links.new(sh.outputs["BSDF"], out.inputs["Surface"])
    _MATS[key] = m
    return m


def paint(obj, rgb, emission=0.0):
    obj.color = rgba(rgb)
    if obj.type in ("MESH", "FONT"):
        obj.data.materials.clear()
        obj.data.materials.append(material(emission))


# ---------- utilidades de animación ----------
def fcurves_of(obj):
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


def set_constant(obj, paths):
    for fc in fcurves_of(obj):
        if fc.data_path in paths:
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"


def visibility(objs, windows, fps, end_frame):
    """Muestra los objetos solo dentro de las ventanas [[t0,t1],...]."""
    if not windows:
        return
    for o in objs:
        o.hide_render = True
        o.hide_viewport = True
        o.keyframe_insert("hide_render", frame=1)
        o.keyframe_insert("hide_viewport", frame=1)
        for t0, t1 in windows:
            for f, hidden in ((frame(t0, fps), False), (frame(t1, fps), True)):
                if f > end_frame + 1:
                    continue
                o.hide_render = hidden
                o.hide_viewport = hidden
                o.keyframe_insert("hide_render", frame=f)
                o.keyframe_insert("hide_viewport", frame=f)
        set_constant(o, ("hide_render", "hide_viewport"))


def add_handheld(cam, target, amplitude, n_keys, fps):
    """Cámara en mano sutil: ruido en la posición de la cámara y, más fuerte, en el punto de mira."""
    for obj, amp, seed in ((target, amplitude, 1.0), (cam, amplitude * 0.4, 7.0)):
        if n_keys < 2:
            obj.keyframe_insert("location", frame=bpy.context.scene.frame_end)
        for fc in fcurves_of(obj):
            if fc.data_path != "location":
                continue
            mod = fc.modifiers.new("NOISE")
            mod.scale = fps * 0.6
            mod.strength = amp
            mod.phase = seed + fc.array_index * 13.0


# ---------- geometría ----------
def add_shape(name, shape, size, loc, rot=None, text=None):
    rot = [math.radians(a) for a in (rot or [0, 0, 0])]
    if shape == "text":
        cu = bpy.data.curves.new(name, "FONT")
        cu.body = text or name
        cu.align_x, cu.align_y = "CENTER", "CENTER"
        cu.size = size[0] if isinstance(size, (list, tuple)) else float(size)
        cu.extrude = 0.01
        o = bpy.data.objects.new(name, cu)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        o.rotation_euler = [math.radians(90) + rot[0], rot[1], rot[2]]  # de pie, mirando a -Y
        return o
    if shape == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(radius=0.5, depth=1, location=loc, rotation=rot)
    elif shape == "sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=loc, rotation=rot)
    elif shape == "cone":
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, depth=1, location=loc, rotation=rot)
    elif shape == "plane":
        bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    return o


def add_person(sid, rgb, height):
    root = bpy.data.objects.new(f"{sid}_root", None)
    bpy.context.scene.collection.objects.link(root)
    body_h = height * 0.82
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=body_h, location=(0, 0, body_h / 2))
    body = bpy.context.active_object
    body.name = f"{sid}_body"
    paint(body, rgb)
    body.parent = root
    head_r = height * 0.075
    head_pivot = bpy.data.objects.new(f"{sid}_headpivot", None)
    bpy.context.scene.collection.objects.link(head_pivot)
    head_pivot.parent = root
    head_pivot.location = (0, 0, body_h + head_r)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=head_r, location=(0, 0, 0))
    head = bpy.context.active_object
    head.name = f"{sid}_head"
    paint(head, SKIN)
    head.parent = head_pivot
    # Cono de mirada en la cara: apunta a -Y local (hacia donde mira la cabeza).
    bpy.ops.mesh.primitive_cone_add(radius1=head_r * 0.45, depth=head_r * 0.9,
                                    location=(0, -head_r * 1.15, 0), rotation=(math.radians(90), 0, 0))
    nose = bpy.context.active_object
    nose.name = f"{sid}_facing"
    paint(nose, (0.05, 0.05, 0.05))
    nose.parent = head_pivot
    return root, head_pivot, [body, head, nose]


def key_subject(root, head_pivot, base_h, keys, fps):
    for k in keys:
        f = frame(k["t"], fps)
        if "pos" in k:
            root.location = k["pos"]
            root.keyframe_insert("location", frame=f)
        if "yaw" in k:
            root.rotation_euler = (0, 0, math.radians(k["yaw"]))
            root.keyframe_insert("rotation_euler", frame=f)
        if "height" in k:
            s = k["height"] / base_h
            root.scale = (1, 1, s)
            root.keyframe_insert("scale", frame=f)
        if "head_yaw" in k or "head_pitch" in k:
            head_pivot.rotation_euler = (math.radians(k.get("head_pitch", 0)), 0, math.radians(k.get("head_yaw", 0)))
            head_pivot.keyframe_insert("rotation_euler", frame=f)


def setup_render(scene, plan):
    global ENGINE
    w, h = plan.get("resolution", [1080, 1920])
    ENGINE = plan.get("engine", "WORKBENCH").upper()
    if ENGINE == "EEVEE":
        for eid in ("BLENDER_EEVEE_NEXT", "BLENDER_EEVEE"):
            try:
                scene.render.engine = eid
                break
            except TypeError:
                continue
        ee = scene.eevee
        for attr, val in (("taa_render_samples", 16), ("use_shadows", True)):
            if hasattr(ee, attr):
                setattr(ee, attr, val)
        scene.view_settings.view_transform = "AgX" if "AgX" in [i.identifier for i in scene.view_settings.bl_rna.properties["view_transform"].enum_items] else scene.view_settings.view_transform
    else:
        scene.render.engine = "BLENDER_WORKBENCH"
        sh = scene.display.shading
        sh.light = "STUDIO"
        sh.color_type = "OBJECT"
        sh.show_shadows = True
        sh.show_cavity = True
    scene.render.resolution_x, scene.render.resolution_y = w, h
    scene.render.fps = plan.get("fps", 24)
    scene.frame_start = 1
    scene.frame_end = frame(plan["duration"], scene.render.fps) - 1
    scene.render.image_settings.file_format = "PNG"
    world = bpy.data.worlds.new("previz")
    wc = plan.get("world_color", [0.12, 0.12, 0.12] if ENGINE == "WORKBENCH" else [0.01, 0.01, 0.012])
    world.color = wc
    try:
        world.use_nodes = True
        bg = world.node_tree.nodes.get("Background")
        if bg:
            bg.inputs["Color"].default_value = rgba(wc)
            bg.inputs["Strength"].default_value = 1.0
    except Exception:
        pass
    scene.world = world


def add_lights(plan, fps):
    for i, L in enumerate(plan.get("lights", [])):
        ld = bpy.data.lights.new(f"light_{i}", L.get("type", "AREA").upper())
        ld.energy = L.get("energy", 300)
        ld.color = L.get("color", [1, 1, 1])
        if ld.type == "AREA":
            ld.size = L.get("size", 1.0)
        if ld.type == "SPOT":
            ld.spot_size = math.radians(L.get("spot_deg", 60))
        lo = bpy.data.objects.new(f"light_{i}", ld)
        bpy.context.scene.collection.objects.link(lo)
        lo.location = L["location"]
        if "look_at" in L:
            tgt = bpy.data.objects.new(f"light_{i}_target", None)
            bpy.context.scene.collection.objects.link(tgt)
            tgt.location = L["look_at"]
            c = lo.constraints.new("TRACK_TO")
            c.target, c.track_axis, c.up_axis = tgt, "TRACK_NEGATIVE_Z", "UP_Y"
        if L.get("visible"):
            visibility([lo], L["visible"], fps, bpy.context.scene.frame_end)
        seen = {}
        for k in L.get("keys", []):
            f = frame(k["t"], fps)
            if f in seen:  # dos claves en el mismo fotograma: la segunda pisa a la primera y un parpadeo se vuelve rampa
                print(f"AVISO luz {i}: t={seen[f]} y t={k['t']} caen en el fotograma {f}; sepáralas al menos {1 / fps:.3f} s")
            seen[f] = k["t"]
            if "energy" in k:
                ld.energy = k["energy"]
                ld.keyframe_insert("energy", frame=f)
            if "color" in k:
                ld.color = k["color"]
                ld.keyframe_insert("color", frame=f)
        for fc in fcurves_of(ld):  # las luces cambian en línea recta: sin rampas ni rebotes de Bézier entre claves
            for kp in fc.keyframe_points:
                kp.interpolation = "LINEAR"


def build_object(o, subjects_by_id, fps, end_frame):
    name = f"obj_{o['id']}"
    shape = o.get("shape", "box")
    size = o.get("size", [0.2, 0.2, 0.2])
    loc = o.get("location") or (o.get("keys") or [{}])[0].get("pos", [0, 0, 0])
    holder = None
    if "pivot" in o:  # bisagra: el giro se aplica a un vacío en el pivote
        holder = bpy.data.objects.new(f"{name}_pivot", None)
        bpy.context.scene.collection.objects.link(holder)
        holder.location = o["pivot"]
        ob = add_shape(name, shape, size, [loc[i] - o["pivot"][i] for i in range(3)], o.get("rotation"), o.get("text"))
        ob.parent = holder
    else:
        ob = add_shape(name, shape, size, loc, o.get("rotation"), o.get("text"))
    paint(ob, o.get("color", [0.7, 0.7, 0.7]), o.get("emission", 0.0))
    anim = holder or ob
    if o.get("parent") and o["parent"] in subjects_by_id:
        anim.parent = subjects_by_id[o["parent"]]
    for k in o.get("keys", []):
        f = frame(k["t"], fps)
        if "pos" in k:
            anim.location = k["pos"]
            anim.keyframe_insert("location", frame=f)
        if "rot" in k:
            base = [math.radians(90), 0, 0] if (shape == "text" and not holder) else [0, 0, 0]
            anim.rotation_euler = [base[i] + math.radians(k["rot"][i]) for i in range(3)]
            anim.keyframe_insert("rotation_euler", frame=f)
        if "scale" in k:
            sc = k["scale"]
            ob.scale = [size[i] * sc for i in range(3)] if shape != "text" else [sc, sc, sc]
            ob.keyframe_insert("scale", frame=f)
        if "color" in k:
            ob.color = rgba(k["color"])
            ob.keyframe_insert("color", frame=f)
    visibility([ob], o.get("visible"), fps, end_frame)
    return ob, holder


def build(plan):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    setup_render(scene, plan)
    fps = scene.render.fps
    end_frame = scene.frame_end

    st = plan.get("set", {})
    set_rgb = st.get("color", [0.55, 0.55, 0.55])
    for b in st.get("boxes", []):
        ob = add_shape(f"set_{b['name']}", b.get("shape", "box"), b["size"], b["location"], b.get("rotation"), b.get("text"))
        paint(ob, b.get("color", set_rgb), b.get("emission", 0.0))
    add_lights(plan, fps)

    hideable, key_colors, subjects_by_id = [], [], {}
    for s in plan.get("subjects", []):
        base_h = s.get("height", 1.75)
        root, head_pivot, parts = add_person(s["id"], s["color"], base_h)
        key_subject(root, head_pivot, base_h, s["keys"], fps)
        subjects_by_id[s["id"]] = root
        if s.get("hand_keys"):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=s["hand_keys"][0]["pos"])
            hand = bpy.context.active_object
            hand.name = f"{s['id']}_hand"
            paint(hand, SKIN)
            hand.parent = root
            for k in s["hand_keys"]:
                hand.location = k["pos"]
                hand.keyframe_insert("location", frame=frame(k["t"], fps))
            parts.append(hand)
        visibility(parts, s.get("visible"), fps, end_frame)
        hideable += parts
        key_colors.append({"tag": s["id"], "label": s.get("label", s["id"]), "kind": "persona",
                           "blockout": f"{color_name(s['color'])} capsule with a skin-coloured sphere head "
                                       "and a small black cone on the face showing where it looks"})

    objects = list(plan.get("objects", [])) + [dict(p, shape=p.get("shape", "box")) for p in plan.get("props", [])]
    for o in objects:
        ob, holder = build_object(o, subjects_by_id, fps, end_frame)
        if o.get("animated", True) and (o.get("keys") or o.get("visible") or o.get("parent")):
            hideable.append(ob)
        if o.get("key_label"):
            key_colors.append({"tag": o["id"], "label": o["key_label"], "kind": "objeto",
                               "blockout": f"{color_name(o.get('color', [0.7, 0.7, 0.7]))} {o.get('shape', 'box')}"})

    cams = {}
    w, h = plan.get("resolution", [1080, 1920])
    for sh in plan["shots"]:
        cdata = bpy.data.cameras.new(f"cam_{sh['id']}")
        cdata.lens = sh.get("lens_mm", 35)
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
            if "lens" in k:
                cdata.lens = k["lens"]
                cdata.keyframe_insert("lens", frame=f)
        con = cam.constraints.new("TRACK_TO")
        con.target = target
        con.track_axis = "TRACK_NEGATIVE_Z"
        con.up_axis = "UP_Y"
        dof = sh.get("dof")
        if dof:  # profundidad de campo (se ve en EEVEE): {fstop, focus:[{t, distance}]}
            cdata.dof.use_dof = True
            cdata.dof.aperture_fstop = dof.get("fstop", 2.8)
            for fk in dof.get("focus", []):
                cdata.dof.focus_distance = fk["distance"]
                cdata.dof.keyframe_insert("focus_distance", frame=frame(fk["t"], fps))
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


def keyframe_times(plan, min_gap=0.3):
    """Explícitos + (con auto_keyframes) inicio y fin de cada plano siempre, y el centro si no hay otro cerca.
    Un explícito a menos de min_gap del inicio o del fin de su plano sobra: Kling no gana nada con dos casi iguales."""
    ts = set(round(t, 2) for t in plan.get("keyframes", []))
    if plan.get("auto_keyframes"):
        for sh in plan["shots"]:
            s, e = round(sh["start"], 2), round(sh["end"] - 0.05, 2)
            inner = [t for t in ts if s < t < e]
            ts -= {t for t in inner if t - s < min_gap or e - t < min_gap}
            ts |= {s, e}
            mid = round((sh["start"] + sh["end"]) / 2, 2)
            if all(abs(mid - t) >= min_gap for t in ts if s <= t <= e):
                ts.add(mid)
    return sorted(t for t in ts if 0 <= t < plan["duration"])


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
        for sub in ("keyframes", "plates"):  # sin restos de una construcción anterior con otros tiempos
            shutil.rmtree(os.path.join(out, sub), ignore_errors=True)
        os.makedirs(os.path.join(out, "keyframes"), exist_ok=True)
        for i, t in enumerate(keyframe_times(plan), 1):
            sh = shot_at(plan, t)
            scene.frame_set(frame(t, fps))
            scene.camera = cams[sh["id"]]
            p = os.path.join(out, "keyframes", f"KF{i:02d}_{t:05.2f}s.png")
            render_still(scene, os.path.abspath(p))
            keyframes_out.append({"index": i, "t": t, "shot": sh["id"], "file": os.path.relpath(p, out)})
        os.makedirs(os.path.join(out, "plates"), exist_ok=True)
        saved = [(o, o.hide_render) for o in hideable]
        for sh in plan["shots"]:
            scene.frame_set(frame(sh["start"], fps))
            for o, _ in saved:
                o.hide_render = True
            scene.camera = cams[sh["id"]]
            render_still(scene, os.path.abspath(os.path.join(out, "plates", f"{sh['id']}_plate.png")))
        for o, v in saved:
            o.hide_render = v
        scene.frame_set(1)

    video_file = None
    if do_video:
        frames_dir = os.path.abspath(os.path.join(out, "_frames"))
        os.makedirs(frames_dir, exist_ok=True)
        scene.render.resolution_percentage = int(round(plan.get("preview_scale", 0.6667) * 100))
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
        "name": plan.get("name"), "fps": fps, "duration": plan["duration"],
        "resolution": plan.get("resolution"), "aspect": aspect_of(plan.get("resolution", [1080, 1920])),
        "engine": ENGINE,
        "cuts": [sh["start"] for sh in plan["shots"][1:]],
        "shots": [{"id": sh["id"], "start": sh["start"], "end": sh["end"], "lens_mm": sh.get("lens_mm", 35),
                   "size": sh.get("size"), "move": sh.get("move"), "motivation": sh.get("motivation"),
                   "handheld": sh.get("handheld", 0)} for sh in plan["shots"]],
        "keyframes": keyframes_out, "blockout_key": key_colors,
        "audio": plan.get("audio", []), "video": video_file, "music": plan.get("music"),
    }
    with open(os.path.join(out, "timeline.json"), "w", encoding="utf-8") as f:
        json.dump(timeline, f, ensure_ascii=False, indent=2)
    print(f"OK blockout → {os.path.abspath(out)}")


main()
