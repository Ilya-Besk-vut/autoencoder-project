# utils.py
import numpy as np
from pathlib import Path
from PIL import Image

def Load_img(folder):
  p = Path(folder)
  files = sorted(f for f in p.iterdir())
  imgs = []
  for f in files:
    try:
          im = Image.open(f)
          im = im.convert('RGB')
          im = im.resize((64,64))
          arr = np.array(im)
          arr = arr.astype(np.float32) / 255.0

          imgs.append(arr)
    except Exception as e:
          print(f"[ERROR] {f}: {e}")

  imgs = np.stack(imgs, axis=0)

  return imgs
