#!/usr/bin/env bash
# Fotogramas para continuidad y control de calidad (requiere ffmpeg y ffprobe).
#   frames.sh last  <video> <salida.png>        último fotograma real
#   frames.sh first <video> <salida.png>        primer fotograma
#   frames.sh at    <video> <segundos> <salida.png>   fotograma en un instante
#   frames.sh sheet <video> [salida.png] [fps]  hoja de contacto (por defecto 2 fps)
#   frames.sh compare <video> <segundos> <referencia.png> <salida.png>   fotograma junto a su referencia
#   frames.sh info  <video>                     duración, resolución, fps y audio (para el control de calidad)
set -euo pipefail
mode="${1:-}"; src="${2:-}"
[[ -z "$mode" || -z "$src" ]] && { sed -n '2,8p' "$0"; exit 1; }
[[ -f "$src" ]] || { echo "No existe: $src" >&2; exit 1; }

case "$mode" in
  last)
    out="${3:?falta salida}"
    # -sseof lee solo el final; reverse garantiza el último fotograma decodificado.
    ffmpeg -v error -y -sseof -1 -i "$src" -vf reverse -frames:v 1 "$out"
    ;;
  first)
    out="${3:?falta salida}"
    ffmpeg -v error -y -i "$src" -frames:v 1 "$out"
    ;;
  at)
    t="${3:?falta segundos}"; out="${4:?falta salida}"
    ffmpeg -v error -y -ss "$t" -i "$src" -frames:v 1 "$out"
    ;;
  sheet)
    out="${3:-${src%.*}_sheet.png}"; fps="${4:-2}"
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$src")
    n=$(python -c "import math;print(max(1,math.ceil(float('$dur')*$fps)))")
    cols=6; rows=$(( (n + cols - 1) / cols ))
    # Marca de tiempo: en Windows drawtext necesita fontfile explícito (sin fontconfig).
    font=""
    for f in /c/Windows/Fonts/arial.ttf /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf /System/Library/Fonts/Supplemental/Arial.ttf; do
      [[ -f "$f" ]] && { font="$f"; break; }
    done
    label=""
    if [[ -n "$font" ]]; then
      ff="$font"; [[ "$ff" == /c/* ]] && ff="C\\:/${ff#/c/}"
      label=",drawtext=fontfile='$ff':text='%{pts\\:hms}':x=6:y=6:fontsize=16:fontcolor=yellow:box=1:boxcolor=black@0.5"
    fi
    if ! ffmpeg -v error -y -i "$src" -vf "fps=$fps,scale=240:-1${label},tile=${cols}x${rows}" -frames:v 1 "$out" 2>/dev/null; then
      # Sin etiquetas: la celda i (desde 0, izquierda→derecha) corresponde a i/fps segundos.
      ffmpeg -v error -y -i "$src" -vf "fps=$fps,scale=240:-1,tile=${cols}x${rows}" -frames:v 1 "$out"
      echo "Hoja sin marcas de tiempo: celda i = i/$fps s" >&2
    fi
    ;;
  compare)
    t="${3:?falta segundos}"; ref="${4:?falta referencia}"; out="${5:?falta salida}"
    [[ -f "$ref" ]] || { echo "No existe: $ref" >&2; exit 1; }
    # Ambas a 720 px de alto, una junto a la otra: referencia | fotograma.
    ffmpeg -v error -y -i "$ref" -ss "$t" -i "$src" \
      -filter_complex "[0:v]scale=-2:720,setsar=1[a];[1:v]scale=-2:720,setsar=1[b];[a][b]hstack=inputs=2" \
      -frames:v 1 "$out"
    ;;
  info)
    ffprobe -v error -show_entries format=duration:stream=codec_type,width,height,r_frame_rate \
      -of default=noprint_wrappers=1 "$src"
    exit 0
    ;;
  *) sed -n '2,8p' "$0"; exit 1 ;;
esac
echo "OK → ${out:-}"
