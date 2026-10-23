# Low-battery pictures

Python scripts that draw the 16 pictures of the "Low battery screen" gallery (480x640, 1 bit).

```
pip install pillow
python3 generate.py preview OUT_DIR      # PNG previews
python3 generate.py emit                 # rewrites src/images/LowBatteryArt.{h,cpp}
```

`artlib.py` is a small toolkit (shapes, hand-drawn lines, hatching, tone dithering), `designs_*.py` hold the
pictures. All pictures are original; the text uses Noto Sans Bold (SIL Open Font License) from this repository.
