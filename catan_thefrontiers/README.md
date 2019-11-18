# FrontEnd para el juego Colonos de Catán - Grupo Frontiers

## Herramientas utilizadas

* React (16.10.2)
* Redux (4.0.4)

## Librarias adicionales

* axios (0.19.0) (llamadas a la API)
* react-router-dom (5.1.2) (direccionamiento de URLs)
* redux-persist (6.0.0) (para guardar el estado de la aplicación en el navegador)
* redux-thunk (2.3.0) (middleware para acciones asíncronas y llamadas a la API en Redux)
* bootstrap (4.3.1) (estilo y diseño)
* tachyons (4.11.1) (estilo y diseño)
* react-dice-complete (1.2.0) (dados)
* react-loading (2.0.3) (animación de carga)

## Testing

* Jest (24.9.0) (testing básico)
* Enzyme (3.10.0) (testing de React)
* axios-mock-adapter (1.17.0) (mock para axios)


## Instalación

Para usar npm:

```
$ sudo apt install npm
```

Alternativamente (y en Windows), descargar e instalar Node.js manualmente desde la [página oficial](https://nodejs.org/es/download/)

Descargar el repositorio con:

```
$ git clone https://gitlab.com/jagermeister95/catan_thefrontiers.git
```

Instalar dependencias:

```
$ cd catan_thefrontiers/
$ npm install
```

Correr servidor en localhost (puerto por defecto: 3000):

```
$ npm start
```

Notas:

* El estado de la app es persistente, incluso luego de reiniciar el navegador. Para forzar un estado completamente nuevo, eliminar las cookies de localhost o abrir una ventana de incógnito.
* Para pruebas básicas (sin API) el mock NO es dinámico; esto es, devuelve siempre los mismos resultados para los mismos pedidos.
