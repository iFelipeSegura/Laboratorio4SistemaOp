# Laboratorio3SistemaOp


## Contenido

1. [¿Qué es la sincronización de procesos?](#1-qué-es-la-sincronización-de-procesos)
2. [Semáforos](#2-semáforos)
3. [Mutex (Exclusión Mutua)](#3-mutex-exclusión-mutua)
4. [Monitores](#4-monitores)
5. [Variables Condicionales](#5-variables-condicionales)
6. [Conclusión Comparativa](#6-conclusión-comparativa)

---

### 1. ¿Qué es la sincronización de procesos?
Es el mecanismo encargado de coordinar la ejecución de procesos que se ejecutan de forma simultánea y que comparten un espacio de direcciones o recursos. 

* **Objetivo principal:** Evitar **condiciones de carrera** (race conditions), donde el resultado final depende del orden de ejecución de las instrucciones, garantizando así la integridad y consistencia de los datos.

### 2. ¿Qué es un semáforo?
Un semáforo es una herramienta de sincronización de bajo nivel que consiste en una variable entera protegida a la que solo se puede acceder mediante dos operaciones atómicas:

* **`wait()` (o P):** Si el valor es mayor que cero, lo decrementa. Si es cero, bloquea al proceso.
* **`signal()` (o V):** Incrementa el valor del semáforo y despierta a uno de los procesos bloqueados.
* **Tipos:** * *Binarios:* (0 o 1) Funcionan de forma similar a un mutex.
    * *Contadores:* Permiten el acceso a un número limitado de instancias de un recurso.

### 3. ¿Qué es un mutex?
El término proviene de *Mutual Exclusion*. Es un objeto de sincronización que se utiliza para permitir que solo un hilo o proceso acceda a un recurso compartido (sección crítica) a la vez.

* **Diferencia clave:** A diferencia de los semáforos, el mutex tiene el concepto de **propietario**. Solo el hilo que bloqueó el mutex es el que está facultado para desbloquearlo.

### 4. ¿Qué es un monitor?
Un monitor es un tipo de dato abstracto de **alto nivel** que encapsula variables, estructuras de datos y procedimientos. 

* **Exclusión implícita:** Solo un proceso puede estar activo dentro del monitor en un momento dado. Esto significa que el programador no tiene que escribir código explícito de "bloqueo" y "desbloqueo" para cada función, reduciendo errores.

### 5. ¿Qué es una variable condicional?
Son variables utilizadas dentro de los monitores para suspender la ejecución de un hilo hasta que se cumpla una condición específica. No tienen un valor entero como los semáforos.

* **Operaciones:**
    * `wait()`: El proceso libera el monitor y se bloquea.
    * `signal()`: Despierta a uno de los procesos que estaba esperando por esa condición.

---

### 6. Conclusión Comparativa
Al analizar los diferentes métodos, se pueden extraer las siguientes conclusiones:

| Método | Nivel | Complejidad | Seguridad |
| :--- | :--- | :--- | :--- |
| **Mutex** | Bajo | Sencillo | Alta (propietario único). |
| **Semáforos** | Bajo | Media/Alta | Baja (propenso a errores de lógica). |
| **Monitores** | Alto | Complejo de implementar | Muy Alta (gestión automática). |

**Resumen final:**
El método más robusto y moderno es el uso de **Monitores**, ya que al ser una abstracción de alto nivel, minimiza el riesgo de errores comunes como el *deadlock* (bloqueo mutuo) o el olvido de liberación de recursos. Sin embargo, los **Mutex** y **Semáforos** siguen siendo esenciales en el desarrollo de sistemas de bajo nivel (kernels, drivers) debido a su mínima sobrecarga (overhead) y rapidez.
