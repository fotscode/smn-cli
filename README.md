# smn-cli

Interfaz tipo CLI para obtener datos sobre el clima de Argentina, los datos son proveidos por el [servicio meteorológico nacional](https://www.smn.gob.ar/).

## Uso

Se debe tener `python` instalado y ademas `curl`, `grep`, `awk` y `head`, es decir comandos tipo Unix.

`python smn-cli.py` para realizar la consulta de forma interactiva.

`python smn-cli.py -d CANTIDAD` permite mostrar CANTIDAD de días, por defecto se muestra un solo día.

`python smn-cli.py -l 'LOCALIDAD'` para buscar según el nombre de localidad.

`python smn-cli.py -n NUMERO` para buscar según el numero de localidad (identificador según smn).
