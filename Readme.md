# Tarea Optativo de Python

* Capturar a que album pertece si es posible


# Usage

Para ver la ayuda solo ejecute:

```bash
$python pyazlyrics.py --help

Usage: pyazlyrics.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get-all     Get the info of all site
  get-artist  Get all song of an artist, link look like this: "https://www.azlyrics.com/v/viceganda.html"
  get-page    Get all song of artists within a page, link look like this: "https://www.azlyrics.com/c.html"
  get-song    Get a song info the link looks like this: "https://www.azlyrics.com/lyrics/viceganda/boompanes.html"
```


## Limitaciones

El error que nos da es porque el sitio identifica que estas haciendo muchos requests.
Para prevenir eso puse un sleep (lo que hace la cosa más lento).
Por ahora pruebenlo como yo lo tenía con solo uno a la vez mientras preparo el código para que no nos detecten.

Cuando no les esté mostrando nada, habran el sitio en la pc y miren a ver que dice.


## Instalación

Si tiene anaconda todo debe estar ahí, pero si algo aqui está el `requirements.txt` para instalar:

```bash
pip install -r requirements.txt
```