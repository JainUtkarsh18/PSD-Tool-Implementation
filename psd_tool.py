pip install psd-tools pillow
from psd_tools import PSDImage
from psd_tools.api.layers import TypeLayer
import os

# Load PSD
psd = PSDImage.open("sample.psd")

print("===== PSD METADATA =====")
print("Size:", psd.size)
print("Color Mode:", psd.color_mode)
print("Depth:", psd.depth)
print("Number of layers:", len(psd))

# Output directories
os.makedirs("exported_layers", exist_ok=True)
os.makedirs("text_layers", exist_ok=True)

def traverse_layers(layers, level=0):
    """Recursively traverse PSD layers"""
    for layer in layers:
        indent = "  " * level
        print(f"{indent}- {layer.name} | Visible: {layer.visible}")

        # If layer is a group
        if layer.is_group():
            traverse_layers(layer, level + 1)
        else:
            # Export raster layer
            if layer.visible and layer.has_pixels():
                image = layer.composite()
                output_path = f"exported_layers/{layer.name}.png"
                image.save(output_path)
                print(f"{indent}  ✔ Exported: {output_path}")

            # Handle text layers
            if isinstance(layer, TypeLayer):
                text = layer.text
                text_path = f"text_layers/{layer.name}.txt"
                with open(text_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"{indent}  ✍ Text extracted: {text_path}")

print("\n===== LAYER STRUCTURE =====")
traverse_layers(psd)

# Export full PSD composite
psd.composite().save("full_composite.png")
print("\n✔ Full PSD composite saved as full_composite.png")
