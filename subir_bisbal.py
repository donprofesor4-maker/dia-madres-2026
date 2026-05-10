#!/usr/bin/env python3
"""Subir fotos de Bisbal a Cloudinary y actualizar fotos_baile.json (sin MJ)."""

import os, json, sys
from pathlib import Path

import cloudinary
import cloudinary.uploader

# ── Config ──────────────────────────────────────────────
BISBAL_DIR = Path("/Volumes/Untitled/DCIM/251D7100/Nueva carpeta con elementos 2")
CLOUD_NAME = "dpiwcrjvv"
API_KEY = "652514619318429"
API_SECRET = sys.argv[1] if len(sys.argv) > 1 else None
OUTPUT_JSON = Path("/Users/navirami/dia-madres-2026/fotos_baile.json")

if not API_SECRET:
    print("Uso: python3 subir_bisbal.py <api_secret>")
    sys.exit(1)

cloudinary.config(cloud_name=CLOUD_NAME, api_key=API_KEY, api_secret=API_SECRET, secure=True)

EXT = {".jpg", ".jpeg", ".png"}

# ── Recolectar Bisbal ───────────────────────────────────
files = sorted(p for p in BISBAL_DIR.iterdir() if p.is_file() and p.suffix.lower() in EXT)
print(f"Bisbal: {len(files)} fotos encontradas\n")

# ── Subir ───────────────────────────────────────────────
nuevos = []
for i, fp in enumerate(files, 1):
    nombre = fp.name
    print(f"[bisbal] {i}/{len(files)} Subiendo {nombre}...", end=" ", flush=True)
    try:
        resp = cloudinary.uploader.upload(
            str(fp),
            folder="baile-4to-2025/bisbal",
            tags=["bisbal", "dia-madres-2026"],
            use_filename=True,
            unique_filename=False,
            resource_type="image",
        )
        url = resp.get("secure_url", resp.get("url", ""))
        nuevos.append({"url": url, "nombre": nombre, "tag": "bisbal"})
        print("OK")
    except Exception as e:
        print(f"ERROR: {e}")

# ── Cargar JSON existente y filtrar MJ ──────────────────
print("\nCargando fotos_baile.json...")
with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
    existentes = json.load(f)

antes = len(existentes)
shakira = [f for f in existentes if f["tag"] == "shakira"]
mj = [f for f in existentes if f["tag"] == "mj"]
print(f"  Shakira: {len(shakira)} | MJ: {len(mj)} (se elimina)")

# ── Unir Shakira + Bisbal ───────────────────────────────
final = shakira + nuevos
with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print(f"\nListo. JSON: {len(final)} fotos ({len(shakira)} Shakira + {len(nuevos)} Bisbal)")
print(f"  MJ removido: {len(mj)} fotos (quedan en Cloudinary para 2° primaria)")
print(f"  Guardado: {OUTPUT_JSON}")
