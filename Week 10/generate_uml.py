"""Generates the updated UML class diagram (uml_class_diagram.png) for Lab 8.

Draws every class from the system with typed attributes/parameters/return values and
the four relationship notations required by the lab:
- Inheritance/generalisation: solid line, hollow triangle at the parent
- Association: solid line
- Aggregation: solid line, hollow diamond at the whole (Inventory)
- Composition: solid line, filled diamond at the whole (Order)

Box widths are measured from the rendered text, so every compartment fits its content.

Run from this folder:  python generate_uml.py   (requires matplotlib)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

# Coordinate system: 180 wide x 115 tall, y increases upwards
FIG_W, FIG_H, DPI = 18.0, 11.5, 150
CANVAS_W, CANVAS_H = 180, 115

TITLE_H_STEREO = 4.6   # title compartment height when a stereotype is shown
TITLE_H_PLAIN = 3.2
LINE_H = 2.2
PAD = 1.0
MEMBER_FS = 8.5
TITLE_FS = 10

CLASS_STYLE = dict(facecolor="white", edgecolor="black", linewidth=1.3)
TITLE_STYLE = dict(facecolor="#e6e6e6", edgecolor="black", linewidth=1.3)

CLASSES = [
    # x0, y0, min_width, stereotype, name, attrs, methods, name_italic
    (6, 97, 36, "interface", "CanBeShipped", [],
     ["+ calculate_shipping_cost(): float {abstract}"], True),
    (58, 78, 48, "abstract", "Product",
     ["- _product_id: str", "- _name: str", "- _price: float", "- _stock: int", "+ supplier: Supplier"],
     ["+ get_product_id(): str", "+ get_price(): float", "+ update_stock(quantity: int): None",
      "+ display_information(): str", "+ to_dict(): dict", "+ get_fulfilment_info(): str {abstract}"], True),
    (120, 94, 40, "", "Supplier",
     ["+ supplier_id: str", "+ name: str", "+ contact_email: str"],
     ["+ display_information(): str"], False),
    (6, 56, 36, "", "PhysicalProduct", ["- _weight: float"],
     ["+ display_information(): str", "+ calculate_shipping_cost(): float",
      "+ get_fulfilment_info(): str", "+ to_dict(): dict"], False),
    (48, 56, 36, "", "DigitalProduct", ["- _download_size: float"],
     ["+ display_information(): str", "+ get_fulfilment_info(): str", "+ to_dict(): dict"], False),
    (86, 56, 36, "", "SubscriptionProduct", ["- _duration: int"],
     ["+ display_information(): str", "+ get_fulfilment_info(): str", "+ to_dict(): dict"], False),
    (6, 16, 40, "", "Inventory", ["- __products: list[Product]"],
     ["+ add_product(product: Product): None", "+ remove_product(product_id: str): Product | None",
      "+ find_product(product_id: str): Product | None", "+ display_all(): None",
      "+ to_list(): list[dict]"], False),
    (124, 52, 40, "", "OrderLine", ["+ product: Product", "+ quantity: int"],
     ["+ calculate_subtotal(): float"], False),
    (124, 16, 40, "", "Order", ["+ order_id: str", "+ order_lines: list[OrderLine]"],
     ["+ add_order_line(product: Product, quantity: int): None",
      "+ remove_order_line(product_id: str): OrderLine | None", "+ calculate_total(): float"], False),
]


def text_width_units(ax, renderer, inv, s, fontsize, mono=True, bold=False, italic=False):
    t = ax.text(0, 0, s, fontsize=fontsize, family="monospace" if mono else "sans-serif",
                fontweight="bold" if bold else "normal", style="italic" if italic else "normal")
    ext = t.get_window_extent(renderer)
    t.remove()
    (x0, _), (x1, _) = inv.transform((0, 0)), inv.transform((ext.width, 0))
    return x1 - x0


def draw_class(ax, renderer, inv, x0, y0, min_w, stereotype, name, attrs, methods, italic):
    needed = max([text_width_units(ax, renderer, inv, m, MEMBER_FS) for m in attrs + methods]
                 + [text_width_units(ax, renderer, inv, name, TITLE_FS, mono=False, bold=True, italic=italic)]
                 + [text_width_units(ax, renderer, inv, f"\u00ab{stereotype}\u00bb", 8, mono=False, italic=italic) if stereotype else 0])
    w = max(min_w, needed + 2 * PAD)
    title_h = TITLE_H_STEREO if stereotype else TITLE_H_PLAIN
    h = title_h + (len(attrs) + len(methods)) * LINE_H + PAD
    top = y0 + h

    ax.add_patch(Rectangle((x0, y0), w, h, **CLASS_STYLE))
    ax.add_patch(Rectangle((x0, top - title_h), w, title_h, **TITLE_STYLE))
    if stereotype:
        ax.text(x0 + w / 2, top - 1.4, f"\u00ab{stereotype}\u00bb", ha="center", va="center",
                fontsize=8, style="italic")
        ax.text(x0 + w / 2, top - 3.2, name, ha="center", va="center",
                fontsize=TITLE_FS, fontweight="bold", style="italic" if italic else "normal")
    else:
        ax.text(x0 + w / 2, top - title_h / 2, name, ha="center", va="center",
                fontsize=TITLE_FS, fontweight="bold", style="italic" if italic else "normal")

    members = attrs + methods
    split_y = top - title_h - len(attrs) * LINE_H
    ax.plot([x0, x0 + w], [split_y, split_y], color="black", linewidth=1.0)
    for i, member in enumerate(members):
        ax.text(x0 + 1.0, top - title_h - (i + 0.55) * LINE_H, member,
                ha="left", va="center", fontsize=MEMBER_FS, family="monospace")

    return x0, y0, w, h, top, split_y


def hollow_triangle_up(ax, x, y, size=1.6, depth=2.8):
    ax.add_patch(Polygon([(x, y), (x - size, y - depth), (x + size, y - depth)],
                         closed=True, facecolor="white", edgecolor="black", linewidth=1.2))


def diamond(ax, x, y, filled, half=1.1, depth=2.0):
    # tip touches the whole's border at (x, y), body extends outward (+y)
    verts = [(x, y), (x - half, y + depth / 2), (x, y + depth), (x + half, y + depth / 2)]
    ax.add_patch(Polygon(verts, closed=True, facecolor="black" if filled else "white",
                         edgecolor="black", linewidth=1.2))


def main() -> None:
    fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=DPI)
    ax.set_xlim(0, CANVAS_W)
    ax.set_ylim(0, CANVAS_H)
    ax.axis("off")
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    inv = ax.transData.inverted()

    # Order and OrderLine share one aligned column width
    order_specs = [spec for spec in CLASSES if spec[4] in ("Order", "OrderLine")]
    other_specs = [spec for spec in CLASSES if spec[4] not in ("Order", "OrderLine")]
    col_w = max(
        max(text_width_units(ax, renderer, inv, m, MEMBER_FS) for spec in order_specs
            for m in spec[5] + spec[6]) + 2 * PAD,
        40,
    )

    drawn = {}
    for spec in other_specs:
        drawn[spec[4]] = draw_class(ax, renderer, inv, *spec)
    for spec in order_specs:  # same x0, shared column width
        drawn[spec[4]] = draw_class(ax, renderer, inv, spec[0], spec[1], col_w,
                                    spec[3], spec[4], spec[5], spec[6], spec[7])

    solid = dict(color="black", linewidth=1.2)
    dashed = dict(color="black", linewidth=1.2, linestyle=(0, (5, 3)))

    # --- Inheritance: children share one hollow triangle on Product's bottom edge ---
    ax.plot([25, 25], [71.2, 74.5], **solid)      # PhysicalProduct
    ax.plot([67, 67], [71.2, 74.5], **solid)      # DigitalProduct
    ax.plot([104, 104], [69, 74.5], **solid)      # SubscriptionProduct
    ax.plot([25, 104], [74.5, 74.5], **solid)     # shared bus
    ax.plot([64.5, 64.5], [74.5, 75.2], **solid)
    hollow_triangle_up(ax, 64.5, 78)              # hollow triangle at parent (Product)

    # --- Realization (dashed): PhysicalProduct implements CanBeShipped ---
    ax.plot([14, 14], [71.2, 94.2], **dashed)
    hollow_triangle_up(ax, 14, 97)

    # --- Association: Supplier —— Product (no ownership) ---
    ax.plot([106, 120], [98, 100], **solid)
    ax.text(109, 99.6, "0..*", fontsize=8, ha="left", va="bottom")
    ax.text(118, 101.3, "1", fontsize=8, ha="right", va="bottom")
    ax.text(113, 96.2, "supplies", fontsize=8.5, style="italic", ha="center")

    # --- Aggregation: Inventory ◇—— Product (hollow diamond at the whole) ---
    ax.plot([43, 43], [35.4, 84], **solid)
    ax.plot([43, 58], [84, 84], **solid)
    diamond(ax, 43, 33.4, filled=False)
    ax.text(44.6, 34.6, "0..1", fontsize=8, ha="left", va="center")
    ax.text(52, 85.7, "0..*", fontsize=8, ha="center", va="bottom")
    ax.text(50.5, 82.2, "aggregates", fontsize=8.5, style="italic", ha="center")

    # --- Composition: Order ◆—— OrderLine (filled diamond at the whole) ---
    ax.plot([144, 144], [33.2, 52], **solid)
    diamond(ax, 144, 31.2, filled=True)
    ax.text(145.5, 34.2, "1", fontsize=8, ha="left", va="center")
    ax.text(145.5, 50, "0..*", fontsize=8, ha="left", va="center")
    ax.text(147, 42.5, "creates", fontsize=8.5, style="italic", ha="left")

    # --- Association: OrderLine —— Product (line refers to a Product it does not own) ---
    ax.plot([144, 144], [62.8, 84], **solid)
    ax.plot([144, 106], [84, 84], **solid)
    ax.text(108, 85.7, "1", fontsize=8, ha="left", va="bottom")
    ax.text(145.5, 64.6, "0..*", fontsize=8, ha="left", va="center")
    ax.text(125, 85.7, "refers to", fontsize=8.5, style="italic", ha="center")

    # --- Title and notation legend ---
    ax.text(90, 112, "INF1103 Lab 8 (Week 10) \u2014 UML Class Diagram",
            fontsize=13, fontweight="bold", ha="center")
    legend_lines = [
        "Relationship notation:",
        "\u2014\u2014\u25b7  Inheritance (hollow triangle at the parent)",
        "\u2014\u2014\u2014  Association (no ownership)",
        "\u2014\u2014\u25c7  Aggregation (hollow diamond at the whole)",
        "\u2014\u2014\u25c6  Composition (filled diamond at the whole)",
    ]
    lx, ly = 60, 13.6
    ax.add_patch(Rectangle((lx - 1.5, ly - 11.2), 46, 13.2, facecolor="#fafafa",
                           edgecolor="#999999", linewidth=0.8))
    for i, line in enumerate(legend_lines):
        weight = "bold" if i == 0 else "normal"
        ax.text(lx, ly - i * 2.3, line, fontsize=8, va="center", fontweight=weight)

    fig.savefig("uml_class_diagram.png", bbox_inches="tight", facecolor="white")
    print("Saved uml_class_diagram.png")


main()
