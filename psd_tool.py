pip install psd-tools

from psd_tools import PSDImage
psd = PSDImage.open("file.psd")

print(psd.size, psd.color_mode)

for layer in psd:
    print(layer.name, layer.visible)

if layer.is_group():
    for sub in layer:
        print(sub.name)

psd.composite().save("full.png")
layer.composite().save("layer.png")

for layer in psd.descendants():
    if layer.is_visible() and not layer.is_group():
        layer.composite().save(f"{layer.name}.png")
