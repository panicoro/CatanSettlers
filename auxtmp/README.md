# Los colonos de Catan
El siguiente proyecto implementa el fronted del clásico juego de mesa para un subconjunto de sus reglas.

Para una introducción al juego se recomienda  leer sus reglas [básicas] en principio y luego sus reglas [detalladas].

[básicas]: https://drive.google.com/file/d/1xAtBKKUcGGNYGmStsaMez-lXh7LsySiM/view
[detalladas]: https://drive.google.com/file/d/11sOYT_F_m4w6JRAGLTlwvNwMjfuMlXPN/view

## Getting Started

### Prerequisitos

Se requieren:

 * node ^12.13.0
 * npm ^6.12.0

Para instalarlos (en linux) hacer lo siguiente:
1. En el directorio `$HOME` correr `wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.1/install.sh | bash`. Esto instala `nvm`, el controlador de versiones de NodeJS.
2. Si el comando anterior se ejecutó correctamente, correr `. .bashrc`. Si hubo un error, referirse a la [página] de nvm.
3. El comando `nvm --version` debería ahora devolver la versión, en este caso `0.35.1`.
4. Por último, para instalar `node` y `npm`, correr `nvm install 12.13`. Ahora es posible correr `node -v` y `npm -v`, que deberían devolver las verisiones (en este caso, `v12.13.0` y `6.12.0` respectivamente).

Para instalar en otro sistemas operativos referirse a la [página] antes mencionada.

[página]: https://github.com/nvm-sh/nvm#installation-and-update


### Instalación
Descargar el repositorio e instalar:
```bash
$ git clone https://gitlab.com/chrism4/auxtmp.git
$ cd auxtmp
$ npm install
```

Es importante **no** correr `npm update`, al menos por el momento, pues `react-scripts` no soporta las versiones nuevas de webpack.

## Usage

En el directorio raíz del repositorio ejecutar:
```bash
npm start
```
Después de que la aplicación completa su carga ir al navegador en la siguiente ruta: `http://localhost:3000`.


## Running the tests

### Coding Style

Nosotros seguimos el code style [airbnb javascript].
Para ejecutar la prueba de violación de estilo:

```bash
$ ./node_modules/.bin/eslint yourfile.js
```

[airbnb javascript]: https://github.com/airbnb/javascript

### Unit tests

Esto se ve ejecutando:

```bash
$ npm run coverage
```
