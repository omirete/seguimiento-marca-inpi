# Seguimiento automático del [trámite de marca en INPI](https://portaltramites.inpi.gob.ar/marcasconsultas/busqueda)

Bot desarrollado en Python. Revisa el estado de tu acta y, si hay cambios, te envía un mensaje por Telegram.

Para usarlo, debes clonar este repositorio y agregar dos archivos en la raíz del proyecto:

* marca.json
* .env

En `marca.json` tienes que indicar el número de acta de tu trámite. Por ejemplo:

```
{
  "acta": 123456
}
```

Luego, en `.env` tienes que definir las dos variables de entorno necesarias para que funcione tu bot de Telegram (los detalles de cómo obtener estos valores están más abajo):

```
API_TOKEN=12345678901:AAAAAAAAAAAAAAAAAAAAAAAAAAA
MY_USER_ID=12345678
```
¿Cómo obtener estos valores?
* Para conseguir una API_TOKEN, debes [crear un bot de Telegram](https://core.telegram.org/bots#3-how-do-i-create-a-bot).
* Luego, para encontrar tu id de usuario en Telegram (MY_USER_ID), puedes utilizar [este bot de Telegram](https://t.me/getidsbot). Si no funciona, la web de [home-assistant.io](https://www.home-assistant.io/) tiene [instrucciones siempre actualizadas para hacerlo](https://www.home-assistant.io/integrations/telegram/).

No duden en abrir issues por cualquier problema que aparezca.

Personalmente tengo el script configurado como un cronjob en una Raspberry Pi Zero 2. Lo hago correr 4 veces al día, pero pueden configurar la frecuencia que deseen. No recomiendo una frecuencia mayor a 1 vez por hora porque el servidor del INPI podría bloquearles la IP.
