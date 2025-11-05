Esta Herramienta creada en Python3 para poder realizar el ataque de fuerza bruta al panel de la maquina Griffin.
La herramienta esta adaptada para que el ataque se pueda realizar en cualquier entorno de red.

# [+] Uso:

Los parámetros son:

- `-w` lo usamos para indicar la ruta del diccionario a usar.
- `-u` lo usamos para indicar la url principal de la web.
- `-U` lo usamos para indicar el username.

Ejemplo:

```bash
python3 Bruteforce.py -w <diccionario> -u <http://10.10.10.1> -U <user> -c <cookie>
```

Configuración de `ddddocr` en las ultimas versiones vamos a tener un problema y para solucionarlo vamos a tener que modificar el `__init__.py` de la la librería `dddocr` de la siguiente manera:

Tendremos dentro la línea:

```python
image = image.resize((int(image.size[0] * (64 / image.size[1])), 64), Image.ANTIALIAS).convert('L')
```

donde vamos a remplazar solo el `ANTIALIAS` por `LANCZOS`.

Con esto echo nuestro script funcionara de forma correcta.
