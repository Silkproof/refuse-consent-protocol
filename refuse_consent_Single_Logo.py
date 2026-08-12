import math
import os
import webbrowser

def generate_single_glitch_hexagon():
    # --- Geometrie Parameter ---
    R = 180  
    sqrt3 = math.sqrt(3)
    
    vertices = [
        (-R, 0), (-R/2, -sqrt3/2 * R), (R/2, -sqrt3/2 * R), 
        (R, 0), (R/2, sqrt3/2 * R), (-R/2, sqrt3/2 * R)
    ]
    
    profile = [
        (0.0, 0.0), (0.2, 0.0), (0.2, 0.15), (0.35, 0.15), 
        (0.35, -0.05), (0.45, -0.05), (0.45, 0.0), (0.7, 0.0), 
        (0.7, 0.12), (0.85, 0.12), (0.85, 0.0), (1.0, 0.0)
    ]

    def get_edge_points(v_start, v_end, is_inverse):
        dx, dy = v_end[0] - v_start[0], v_end[1] - v_start[1]
        nx, ny = -dy, dx
        pts = []
        for t, offset in profile:
            _t, _offset = (1.0 - t, -offset) if is_inverse else (t, offset)
            pts.append((v_start[0] + dx * _t + nx * _offset, v_start[1] + dy * _t + ny * _offset))
        if is_inverse: pts.reverse()
        return pts

    # --- SVG Pfad generieren ---
    path_data = []
    for i in range(6):
        pts = get_edge_points(vertices[i], vertices[(i+1)%6], i >= 3)
        if i == 0: path_data.append(f"M {pts[0][0]:.3f} {pts[0][1]:.3f}")
        for p in pts[1:]: path_data.append(f"L {p[0]:.3f} {p[1]:.3f}")
    path_data.append("Z")

    scale = 3.6
    hole_vertices = [(0, -18*scale), (15*scale, -5*scale), (10*scale, 15*scale), (-12*scale, 12*scale), (-18*scale, -2*scale)]
    path_data.append(f"M {hole_vertices[0][0]:.3f} {hole_vertices[0][1]:.3f}")
    for p in hole_vertices[1:]: path_data.append(f"L {p[0]:.3f} {p[1]:.3f}")
    path_data.append("Z")
    
    svg_path = " ".join(path_data)

    # --- SVG Datei zusammenbauen (mit offiziellem XML Header) ---
    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 500 500" style="background-color: white;">')
    svg.append(f'<path d="{svg_path}" fill="black" fill-rule="evenodd" transform="translate(250, 250)" />')
    svg.append('</svg>')

    # --- Datei speichern (Zwingend als UTF-8) ---
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "refuse_consent_logo.svg")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))
        
    print(f"ERFOLG! Einzel-Logo wurde hier gespeichert:\n{file_path}\n")
    return file_path

if __name__ == "__main__":
    try:
        print("Generiere Einzel-Glitch-Hexagon...")
        saved_file_path = generate_single_glitch_hexagon()
        
        print("Versuche Browser zu öffnen...")
        webbrowser.open(f"file://{saved_file_path}")
        
    except Exception as e:
        print(f"\nFEHLER: {e}")
        
    input("\nDrücke Enter, um das Fenster zu schliessen...")