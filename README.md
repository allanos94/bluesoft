# bluesoft

## Desafio

Bluesoft Bank es un banco tradicional que se encarga de guardar el dinero de sus ahorradores, ofrece dos tipos de cuenta; ahorros para personas naturales y corrientes para empresas. Adicionalmente para cada cuenta se pueden hacer consignaciones y retiros.

Adicionalmente tiene que soportar algunos requerimientos para sus ahorradores:

Consultar el saldo de la cuenta
Consultar los movimientos más recientes
Generar extractos mensuales

Reglas de negocio:

Una cuenta no puede tener un saldo negativo.
El saldo de la cuenta siempre debe ser consistente frente a dos operaciones concurrentes (consignación, retiro)

También se deben generar reportes en tiempo real como:

Listado de clientes con el número de transacciones para un mes es particular, organizado descendentemente (primero el cliente con mayor # de transacciones en el mes)
Clientes que retiran dinero fuera de la ciudad de origen de la cuenta con el valor total de los retiros realizados superior a $1.000.000.


## Cómo correr la aplicación:

1. Clonar el repositorio en su máquina local.

```shell
git clone git@github.com:allanos94/bluesoft.git
```

2. Ingresar a la carpeta del proyecto.

```shell
cd bluesoft
```

3. Instalar poetry que es el manejador de dependencias de python.

```shell
pip install poetry
```

4. Ahora solo es instalar todas las dependencias con el siguiente comando de poetry:

```shell	
poetry install
```

5. Luego debe instalar los fixtures necesarios para correr la app:

```shell
./manage.py loaddata fixtures/data.json
```

6. Ya puede correr la aplicación con el debug de vscode o con el siguiente comando:

```shell
./manage.py runserver
```

7. Para poder usar la app, debe crear un superuser o registrar un usuario en la app.

```shell
./manage.py createsuperuser
```

8. Todos los EP están documentados en postman y compartiré ese repo via correo electrónico.