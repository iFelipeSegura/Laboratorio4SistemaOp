import threading
import random
import math
import time
from collections import Counter

ARCHIVO = "resultados.txt"

sem_escritura = threading.Semaphore(1)
sem_lectura   = threading.Semaphore(0)
terminado     = False
mutex_fin     = threading.Semaphore(1)


def inicializar_archivo():
    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write("=== Archivo Compartido ===\n")
        f.write("\n--- NÚMEROS GENERADOS ---\n")
        f.write("\n--- RESULTADOS ---\n")


def leer_pendientes() -> list[int]:
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        contenido = f.read()

    generados = []
    if "--- NÚMEROS GENERADOS ---" in contenido:
        seccion = contenido.split("--- NÚMEROS GENERADOS ---")[1]
        seccion = seccion.split("--- RESULTADOS ---")[0]
        for linea in seccion.strip().splitlines():
            linea = linea.strip()
            if linea.startswith("numero:"):
                generados.append(int(linea.replace("numero:", "").strip()))

    procesados = []
    if "--- RESULTADOS ---" in contenido:
        seccion = contenido.split("--- RESULTADOS ---")[1]
        for linea in seccion.strip().splitlines():
            linea = linea.strip()
            if linea.startswith("El factorial de:"):
                num = int(linea.split(":")[1].split("es")[0].strip())
                procesados.append(num)

    cnt_gen  = Counter(generados)
    cnt_proc = Counter(procesados)
    pendientes = []
    for num, total in cnt_gen.items():
        faltan = total - cnt_proc[num]
        pendientes.extend([num] * faltan)

    return pendientes


def escribir_numero(numero: int):
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        contenido = f.read()

    contenido = contenido.replace(
        "--- RESULTADOS ---",
        f"numero: {numero}\n--- RESULTADOS ---"
    )

    with open(ARCHIVO, "w", encoding="utf-8") as f:
        f.write(contenido)


def escribir_resultado(numero: int, factorial: int):
    with open(ARCHIVO, "a", encoding="utf-8") as f:
        f.write(f"El factorial de: {numero} es {factorial}\n")


def hilo_generador(cantidad: int, semilla: int | None = None):
    global terminado
    rng = random.Random(semilla)

    for _ in range(cantidad):
        numero = rng.randint(1, 10)

        sem_escritura.acquire()
        escribir_numero(numero)
        print(f"[Generador] Escribió en archivo → numero: {numero}")
        sem_lectura.release()

        time.sleep(rng.uniform(0.2, 0.5))

    mutex_fin.acquire()
    terminado = True
    mutex_fin.release()
    print("[Generador] Fin. No se generarán más números.")
    sem_lectura.release()


def hilo_calculador():
    while True:
        sem_lectura.acquire()

        mutex_fin.acquire()
        fin = terminado
        mutex_fin.release()

        pendientes = leer_pendientes()

        if fin and not pendientes:
            print("[Calculador] Sin pendientes. Terminando.")
            break

        if not pendientes:
            sem_lectura.release()
            continue

        numero = pendientes[0]
        resultado = math.factorial(numero)
        print(f"[Calculador] Leyó del archivo → {numero}! = {resultado}")

        escribir_resultado(numero, resultado)
        print(f"[Calculador] Escribió en archivo → El factorial de: {numero} es {resultado}")

        sem_escritura.release()

        time.sleep(0.1)


def main():
    inicializar_archivo()

    t_gen = threading.Thread(target=hilo_generador, args=(6, 42), name="Generador")
    t_cal = threading.Thread(target=hilo_calculador, name="Calculador")

    print("=" * 55)
    print("  Generador escribe en archivo — Calculador lee del mismo")
    print("=" * 55 + "\n")

    t_gen.start()
    t_cal.start()

    t_gen.join()
    t_cal.join()

    print("\n" + "=" * 55)
    print(f"  Completado. Ver '{ARCHIVO}'")
    print("=" * 55)

    print(f"\n── Contenido final de {ARCHIVO} ──")
    with open(ARCHIVO, "r", encoding="utf-8") as f:
        print(f.read())


if __name__ == "__main__":
    main()
