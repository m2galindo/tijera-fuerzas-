"""
Programa: fuerzas en la mesa con mecanismo de tijera (Modelo 1)

1. Pide los datos de entrada (Enter = usar el valor por defecto).
2. Calcula todas las fuerzas en función de la masa m [kg] y del ángulo de la tijera θ [°].
3. Simula el mecanismo: la tijera sube desde la posición horizontal hasta el ángulo θ que
   pusiste. Si el ángulo es muy grande, la caja se desliza o se voltea y se cae de la mesa.
4. Guarda la simulación en simulacion_tijera.gif, una tabla de barrido y las gráficas.

Notación:
  θ  = ángulo de los brazos de la tijera con la horizontal (dato de entrada)
  α  = inclinación de la mesa (sale de la geometría)
Unidades: longitudes en m, fuerzas en N, ángulos en grados.

Nota: el usuario aplica una fuerza (par) en la manivela del tornillo B–D.
Esa fuerza externa es la que produce la tensión T en el tornillo y fija el ángulo θ.
Su valor depende de la rosca y no se calcula aquí.

Uso:
  python tijera_fuerzas.py                      -> pregunta los datos
  python tijera_fuerzas.py --m 40 --theta 80    -> sin preguntar (los demás datos por defecto)
Requiere: pip install matplotlib pillow
"""

import argparse
import math
import sys

g = 9.81  # m/s²

# Datos por defecto (los de las hojas de cálculo del equipo)
DATOS = {
    "m":     (40.0, "kg", "Masa de la caja (máx. 40 kg)"),
    "theta": (50.0, "°",  "Ángulo de la tijera θ"),
    "L":     (0.12, "m",  "Largo de cada eslabón corto de la tijera"),
    "a":     (0.20, "m",  "Distancia del apoyo G al borde de la caja"),
    "b":     (0.35, "m",  "Base de la caja (≤ 0.40 m)"),
    "c":     (0.20, "m",  "Distancia del borde de la caja al poste H"),
    "h":     (0.25, "m",  "Altura de la caja (≤ 0.30 m)"),
    "y_A":   (0.25, "m",  "Altura del perno A (base de la tijera)"),
    "y_H":   (0.45, "m",  "Altura del perno H (poste fijo)"),
    "mu_k":  (0.35, "",   "Coeficiente de fricción cinética caja-mesa"),
}


# ----------------------------- ENTRADA DE DATOS -----------------------------
def pedir_datos():
    p = argparse.ArgumentParser()
    for k in DATOS:
        p.add_argument(f"--{k}", type=float)
    args = vars(p.parse_args())
    preguntar = all(v is None for v in args.values()) and sys.stdin.isatty()

    d = {}
    print("=== Datos de entrada (Enter = valor por defecto) ===")
    for k, (val, uni, desc) in DATOS.items():
        if args[k] is not None:
            d[k] = args[k]
        elif preguntar:
            while True:
                r = input(f"{desc} [{val} {uni}]: ").strip().replace(",", ".")
                if r == "":
                    d[k] = val
                    break
                try:
                    d[k] = float(r)
                    break
                except ValueError:
                    print("  Escribe un número.")
        else:
            d[k] = val
        print(f"  {k:<6} = {d[k]} {uni}")
    d["d"] = d["a"] + d["b"] + d["c"]
    print(f"  d      = a + b + c = {d['d']:.3f} m")
    return d


# ----------------------------- MODELO ESTÁTICO -----------------------------
def alfa(D, theta_deg):
    """Inclinación de la mesa α [rad]; None si el ángulo no es posible."""
    if not 0 < theta_deg < 90:
        return None
    s = (D["y_A"] + 4 * D["L"] * math.sin(math.radians(theta_deg)) - D["y_H"]) / D["d"]
    return math.asin(s) if abs(s) <= 1 else None


def calcular(D, m, theta_deg):
    """Todas las fuerzas para una masa m y un ángulo θ (equilibrio estático)."""
    al = alfa(D, theta_deg)
    if al is None:
        raise ValueError(f"θ = {theta_deg}° no es geométricamente posible")
    th = math.radians(theta_deg)
    W = m * g
    b, c, h, d = D["b"], D["c"], D["h"], D["d"]

    # Caja
    N = W * math.cos(al)
    f = W * math.sin(al)
    desliza = math.tan(abs(al)) > D["mu_k"]
    voltea = math.tan(abs(al)) > b / h

    # Mesa: ΣM_H = 0 y ΣF_y = 0
    G_y = W * ((c + b / 2) * math.cos(al) - (h / 2) * math.sin(al)) / (d * math.cos(al))
    H_y = W - G_y

    # Tijera
    F1 = G_y / (2 * math.sin(th))   # eslabones GE, GF, BA, DA (compresión)
    T = 2 * G_y / math.tan(th)      # tornillo B–D (tensión), producida por la fuerza del usuario
    return {
        "m [kg]": m, "θ [°]": theta_deg, "α [°]": math.degrees(al),
        "N [N]": N, "f [N]": f, "G_y [N]": G_y, "H_y [N]": H_y,
        "F1 [N]": F1, "T [N]": T, "C_x [N]": T, "C_y [N]": 0.0, "A_y [N]": G_y,
        "N1 [N]": G_y, "N2 [N]": H_y, "desliza": desliza, "voltea": voltea,
    }


def imprimir(r):
    print(f"\n--- m = {r['m [kg]']} kg, θ = {r['θ [°]']:.2f}° ---")
    for k, v in r.items():
        if isinstance(v, bool):
            print(f"  {k:<10} {'sí' if v else 'no'}")
        elif k not in ("m [kg]", "θ [°]"):
            print(f"  {k:<10} {v:10.3f}")


def theta_horizontal(D):
    s = (D["y_H"] - D["y_A"]) / (4 * D["L"])
    return math.degrees(math.asin(s)) if 0 < s < 1 else None


def theta_para_alfa(D, alfa_deg):
    s = (D["y_H"] - D["y_A"] + D["d"] * math.sin(math.radians(alfa_deg))) / (4 * D["L"])
    return math.degrees(math.asin(s)) if 0 < s < 1 else None


# ----------------------------- SIMULACIÓN -----------------------------
def geometria(D, theta_deg):
    th = math.radians(theta_deg)
    L, yA = D["L"], D["y_A"]
    lc, ls = L * math.cos(th), L * math.sin(th)
    P = {"A": (0, yA), "B": (-lc, yA + ls), "D": (lc, yA + ls), "C": (0, yA + 2 * ls),
         "E": (-lc, yA + 3 * ls), "F": (lc, yA + 3 * ls), "G": (0, yA + 4 * ls)}
    al = alfa(D, theta_deg)
    u = (math.cos(al), -math.sin(al))     # dirección de la mesa, de G hacia H
    P["H"] = (D["d"] * u[0], P["G"][1] + D["d"] * u[1])
    return P, al, u


def poligono(p, phi, w, hh):
    e = (math.cos(phi), math.sin(phi))
    n = (-math.sin(phi), math.cos(phi))
    q = (p[0] + w * e[0], p[1] + w * e[1])
    return [p, q, (q[0] + hh * n[0], q[1] + hh * n[1]), (p[0] + hh * n[0], p[1] + hh * n[1]), p]


def simular(D):
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation, PillowWriter

    m, th_obj = D["m"], D["theta"]
    th_ini = theta_horizontal(D) or th_obj
    n_sub = 45
    dt = 0.04
    BASE_Y = 0.12

    # Estado de la caja
    caja = {"modo": "mesa", "s": D["a"], "v": 0.0, "w": D["b"], "hh": D["h"],
            "psi": 0.0, "om": 0.0, "p": None, "phi": 0.0, "vx": 0.0, "vy": 0.0}

    fig = plt.figure(figsize=(11, 6.5))
    ax = fig.add_axes([0.06, 0.08, 0.58, 0.85])
    tax = fig.add_axes([0.66, 0.08, 0.33, 0.85]); tax.axis("off")
    ax.set_aspect("equal"); ax.set_xlim(-0.3, D["d"] + 0.45); ax.set_ylim(-0.03, 1.1)
    ax.set_xlabel("x [m]"); ax.set_ylabel("y [m]"); ax.grid(alpha=0.3)
    ax.set_title(f"Simulación: m = {m} kg, θ objetivo = {th_obj}°")
    ax.plot([-0.3, D["d"] + 0.45], [0, 0], color="gray", lw=1)
    ax.plot([-0.1, D["d"]], [BASE_Y, BASE_Y], color="#2563eb", lw=6)
    for xw in (-0.05, D["d"] - 0.05):
        ax.add_patch(plt.Circle((xw, 0.05), 0.05, color="#2563eb"))
    ax.plot([0, 0], [BASE_Y, D["y_A"]], color="#2563eb", lw=5)

    barras, = ax.plot([], [], color="black", lw=2.5)
    tornillo, = ax.plot([], [], color="#15803d", lw=3, ls="--")
    mesa, = ax.plot([], [], color="#2563eb", lw=6)
    poste, = ax.plot([], [], color="#2563eb", lw=5)
    caja_ln, = ax.plot([], [], color="#b45309", lw=2.5)
    pernos, = ax.plot([], [], "o", color="black", ms=5)
    ax.annotate("fuerza del\nusuario", xy=(-0.11, 0.0), xytext=(-0.28, 0.0), color="#15803d",
                fontsize=8, arrowprops=dict(arrowstyle="-|>", color="#15803d"))
    flecha = ax.texts[-1]
    aviso = ax.text(D["d"] / 2, 1.02, "", ha="center", fontsize=14, color="#c0392b", weight="bold")
    info = tax.text(0, 1, "", va="top", family="monospace", fontsize=9.5)

    frames = [th_ini + (th_obj - th_ini) * i / n_sub for i in range(n_sub + 1)] + [th_obj] * 70

    def piso(x):
        return BASE_Y if -0.1 <= x <= D["d"] else 0.0

    def actualizar_caja(al, u, G):
        mu = D["mu_k"]
        sg = 1 if al >= 0 else -1
        ta = math.tan(abs(al))
        if caja["modo"] == "mesa":
            if ta > caja["w"] / caja["hh"] and caja["w"] / caja["hh"] <= mu:
                caja["modo"] = "voltea"
            elif ta > mu:
                caja["modo"] = "desliza"
        if caja["modo"] == "voltea":
            caja["om"] += 10 * dt
            caja["psi"] += caja["om"] * dt
            if caja["psi"] >= math.pi / 2:      # quedó acostada: ahora es una caja h × b
                if sg > 0:
                    caja["s"] += caja["w"]
                else:
                    caja["s"] -= caja["hh"]
                caja["w"], caja["hh"], caja["psi"] = caja["hh"], caja["w"], 0.0
                caja["modo"] = "desliza" if ta > mu else "mesa"
        if caja["modo"] == "desliza":
            acc = sg * g * (math.sin(abs(al)) - mu * math.cos(al))
            caja["v"] += acc * dt
            caja["s"] += caja["v"] * dt
            centro = caja["s"] + caja["w"] / 2
            if centro > D["d"] or centro < 0:   # se sale de la mesa
                caja["modo"] = "cae"
                caja["p"] = (G[0] + caja["s"] * u[0], G[1] + caja["s"] * u[1])
                caja["phi"] = -al
                caja["vx"], caja["vy"] = caja["v"] * u[0], caja["v"] * u[1]
                caja["om"] = -4.0 * sg
        if caja["modo"] == "cae":
            caja["vy"] -= g * dt
            caja["p"] = (caja["p"][0] + caja["vx"] * dt, caja["p"][1] + caja["vy"] * dt)
            caja["phi"] += caja["om"] * dt
            pol = poligono(caja["p"], caja["phi"], caja["w"], caja["hh"])
            cx = sum(q[0] for q in pol[:4]) / 4
            ymin = min(q[1] for q in pol[:4])
            if ymin <= piso(cx):                # toca el suelo: queda acostada
                k = round(caja["phi"] / (math.pi / 2))
                caja["phi"] = k * math.pi / 2
                if k % 2:
                    caja["w"], caja["hh"] = caja["hh"], caja["w"]
                    caja["phi"] = 0.0
                else:
                    caja["phi"] = 0.0
                x0 = cx - caja["w"] / 2
                if piso(cx) == 0.0:             # cae al suelo, fuera del carrito
                    x0 = max(x0, D["d"] + 0.01) if cx > 0 else min(x0, -0.11 - caja["w"])
                caja["p"] = (x0, piso(cx))
                caja["modo"] = "suelo"

    def poligono_caja(al, u, G):
        if caja["modo"] in ("cae", "suelo"):
            return poligono(caja["p"], caja["phi"], caja["w"], caja["hh"])
        p = (G[0] + caja["s"] * u[0], G[1] + caja["s"] * u[1])
        if caja["modo"] == "voltea":
            sg = 1 if al >= 0 else -1
            piv_s = caja["s"] + (caja["w"] if sg > 0 else 0)
            piv = (G[0] + piv_s * u[0], G[1] + piv_s * u[1])
            pol = poligono(p, -al, caja["w"], caja["hh"])
            ang = -sg * caja["psi"]
            ca, sa = math.cos(ang), math.sin(ang)
            return [(piv[0] + ca * (x - piv[0]) - sa * (y - piv[1]),
                     piv[1] + sa * (x - piv[0]) + ca * (y - piv[1])) for x, y in pol]
        return poligono(p, -al, caja["w"], caja["hh"])

    def dibujar(theta):
        P, al, u = geometria(D, theta)
        actualizar_caja(al, u, P["G"])
        orden = ["G", "E", "D", "A", "B", "F", "G"]
        barras.set_data([P[k][0] for k in orden], [P[k][1] for k in orden])
        tornillo.set_data([P["B"][0], P["D"][0]], [P["B"][1], P["D"][1]])
        mesa.set_data([P["G"][0], P["H"][0]], [P["G"][1], P["H"][1]])
        poste.set_data([P["H"][0], P["H"][0]], [BASE_Y, P["H"][1]])
        pernos.set_data([P[k][0] for k in P], [P[k][1] for k in P])
        flecha.xy = (P["B"][0] - 0.01, P["B"][1])
        flecha.set_position((P["B"][0] - 0.2, P["B"][1] + 0.02))
        pol = poligono_caja(al, u, P["G"])
        caja_ln.set_data([q[0] for q in pol], [q[1] for q in pol])

        estados = {"mesa": "en reposo", "desliza": "SE DESLIZA", "voltea": "SE VOLTEA",
                   "cae": "SE ESTÁ CAYENDO", "suelo": "SE CAYÓ DE LA MESA"}
        caja_ln.set_color("#b45309" if caja["modo"] == "mesa" else "#c0392b")
        aviso.set_text("¡LA CAJA SE CAYÓ!" if caja["modo"] in ("cae", "suelo") else
                       ("¡La caja se desliza!" if caja["modo"] == "desliza" else
                        ("¡La caja se voltea!" if caja["modo"] == "voltea" else "")))

        r = calcular(D, m, theta)
        txt = (f"DATOS DE ENTRADA\n"
               f" m={D['m']} kg  θ obj={th_obj}°\n"
               f" L={D['L']} m  a={D['a']} m\n b={D['b']} m  c={D['c']} m\n"
               f" h={D['h']} m  d={D['d']:.2f} m\n"
               f" y_A={D['y_A']} m  y_H={D['y_H']} m\n μk={D['mu_k']}\n\n"
               f"ESTADO ACTUAL\n θ = {theta:6.2f} °\n α = {r['α [°]']:6.2f} °\n"
               f" Caja: {estados[caja['modo']]}\n"
               f" (desliza si α > {math.degrees(math.atan(D['mu_k'])):.2f}°,\n"
               f"  voltea si α > {math.degrees(math.atan(D['b'] / D['h'])):.2f}°)\n\n")
        if caja["modo"] == "mesa":
            txt += (f"FUERZAS (equilibrio)\n"
                    f" N   = {r['N [N]']:7.1f} N\n f   = {r['f [N]']:7.1f} N\n"
                    f" G_y = {r['G_y [N]']:7.1f} N\n H_y = {r['H_y [N]']:7.1f} N\n"
                    f" F1  = {r['F1 [N]']:7.1f} N (comp.)\n T   = {r['T [N]']:7.1f} N (tens.)\n"
                    f" C_x = {r['C_x [N]']:7.1f} N\n A_y = {r['A_y [N]']:7.1f} N")
        else:
            txt += "FUERZAS\n Ya no hay equilibrio\n estático: la caja\n se mueve."
        info.set_text(txt)
        return barras, tornillo, mesa, poste, caja_ln, pernos, info, aviso

    anim = FuncAnimation(fig, dibujar, frames=frames, interval=40, repeat=False)
    anim.save("simulacion_tijera.gif", writer=PillowWriter(fps=25))
    print("Simulación guardada en simulacion_tijera.gif")
    plt.close(fig)


# ----------------------------- PROGRAMA PRINCIPAL -----------------------------
if __name__ == "__main__":
    D = pedir_datos()

    if alfa(D, D["theta"]) is None:
        print(f"\nERROR: con θ = {D['theta']}° la tijera no puede armar la mesa con estas medidas.")
        print("Prueba otro ángulo (0° < θ < 90°) o revisa L, y_A, y_H y d.")
        sys.exit(1)

    # 1) Resultados
    th0 = theta_horizontal(D)
    if th0:
        print(f"\nMesa horizontal (α = 0°) con θ = {th0:.2f}°")
        imprimir(calcular(D, D["m"], th0))
    r = calcular(D, D["m"], D["theta"])
    print("\nÁngulo que pusiste:")
    imprimir(r)

    a_d = math.degrees(math.atan(D["mu_k"]))
    a_v = math.degrees(math.atan(D["b"] / D["h"]))
    th_d, th_v = theta_para_alfa(D, a_d), theta_para_alfa(D, a_v)
    print(f"\nLa caja desliza con α > {a_d:.2f}° (θ > {th_d:.2f}°)" if th_d else
          f"\nLa caja desliza con α > {a_d:.2f}° (la tijera no llega a ese ángulo)")
    print(f"La caja se voltea con α > {a_v:.2f}° (θ > {th_v:.2f}°)" if th_v else
          f"La caja se voltea con α > {a_v:.2f}° (la tijera no llega a ese ángulo)")
    if r["voltea"] and a_v < a_d:
        print(">> Con tu ángulo la caja SE VOLTEA y se cae.")
    elif r["desliza"]:
        print(">> Con tu ángulo la caja SE DESLIZA y se cae de la mesa.")
    else:
        print(">> Con tu ángulo la caja se queda en su lugar.")

    # 2) Barrido de θ y m
    import csv
    filas = []
    for m in (10, 20, 30, 40):
        for th in range(5, 90, 5):
            try:
                filas.append(calcular(D, m, th))
            except ValueError:
                pass
    with open("barrido_tijera.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=filas[0].keys())
        w.writeheader()
        w.writerows(filas)
    print("\nTabla de barrido guardada en barrido_tijera.csv")

    # 3) Gráficas y simulación
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        ths = [t / 2 for t in range(2, 179) if alfa(D, t / 2) is not None]
        fig, ax = plt.subplots(1, 2, figsize=(11, 4.2))
        for m in (10, 20, 30, 40):
            rs = [calcular(D, m, t) for t in ths]
            ax[0].plot(ths, [x["T [N]"] for x in rs], label=f"m = {m} kg")
            ax[1].plot(ths, [x["F1 [N]"] for x in rs], label=f"m = {m} kg")
        ax[0].set(title="Fuerza en el tornillo T vs θ", xlabel="θ [°]", ylabel="T [N]")
        ax[1].set(title="Fuerza en los eslabones F1 vs θ", xlabel="θ [°]", ylabel="F1 [N]")
        for x in ax:
            x.grid(alpha=0.3)
            x.legend()
        fig.tight_layout()
        fig.savefig("graficas_tijera.png", dpi=200)
        plt.close(fig)
        print("Gráficas guardadas en graficas_tijera.png")
        simular(D)
    except ImportError:
        print("Instala matplotlib y pillow para las gráficas y la simulación: pip install matplotlib pillow")