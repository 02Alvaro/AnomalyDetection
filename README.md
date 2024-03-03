# Detección de abandono de estudiantes universitarios

Este proyecto utiliza análisis de datos y detección de anomalías para identificar a los estudiantes que están en riesgo de abandonar la universidad. El objetivo es poder predecir con la mayor antelación posible si un estudiante está en riesgo de abandonar, permitiendo a la universidad intervenir y proporcionar apoyo adicional si es necesario.

## Estructura del proyecto

El proyecto se compone de dos servicios principales definidos en un archivo `docker-compose.yml`:

- `anomaly_detection`: este es el servicio principal que realiza el análisis de datos y la detección de anomalías. Este servicio se basa en un Dockerfile en la carpeta `anomalyDetection` y monta esta carpeta en `/app` dentro del contenedor.

- `db`: este servicio ejecuta una base de datos MySQL. Los scripts SQL para inicializar la base de datos se encuentran en la carpeta `/database/sql` y los archivos CSV para poblar la base de datos se encuentran en la carpeta `/database/csv`. Esta base de datos está expuesta en el puerto 3306.

## Ejecutar el proyecto

#### Establecer el fichero .env

Establece las variables de entorno `MYSQL_HOST`,`MYSQL_USER`,`MYSQL_PASSWORD`,`MYSQL_ROOT_PASSWORD` y `MYSQL_DATABASE` con los valores deseados en un fichero .env.

#### Instala las imagenes de docker para TimeEval

Los algoritmos de TimeEval funcionan por imagenes de docker, por tanto hay que instalarlas. Para instalarlas se hace con los siguientes comandos:

```bash
docker pull ghcr.io/timeeval/autoencoder:0.3.0
```

```bash
docker pull ghcr.io/timeeval/dae:0.3.0
```

```bash
docker pull ghcr.io/timeeval/lstm_vae:0.3.0
```

#### Descargar los datos

Por temas de tamaño, los archivos de datos no se incluyen en el repositorio. Para descargarlos, descargue los ficheros del enlace indicado en dependencias. Esto descargará los archivos CSV necesarios para poblar la base de datos.

#### Establecer los algoritmos a ejecutar en el fichero config.yaml

En este fichero se establecen los algoritmos a entrenar y ejecutar. A continuación se muestra un ejemplo:

```yaml
algorithms:
  - name: dae
    reportFile: "allReports.csv"
    train:
      - data_file: "dataset.csv"
        model_output: "dae_model.pkl"
        parameters:
          latent_size: 30
          epochs: 5
    test:
      - data_file: "dataset.csv"
        model_input: "dae_model.pkl"
    train-test:
      - data_file_test: "dataset.csv"
        data_file_train: "dataset.csv"
        model: "dae_model.zip"
        parameters:
          latent_size: 10
          epochs: 5
```

#### Ejecutar el proyecto

Para ejecutar el proyecto, simplemente ejecute el siguiente comando en la raíz del proyecto:

```bash
docker-compose up
```

Por temas de tamaño, los archivos de datos no se incluyen en el repositorio. Para descargarlos, descargue los ficheros del enlace indicado en dependencias. Esto descargará los archivos CSV necesarios para poblar la base de datos.

## Dependencias

Se usan los datos de [Open University Learning Analytics dataset](https://analyse.kmi.open.ac.uk/open_dataset) y los algoritmos de [TimeEval-algorithms ](https://github.com/HPI-Information-Systems/TimeEval-algorithms/tree/main), aunque en primeras iteraciones se han usado los algoritmos de pyod, pero estos no requieren instalación adicional.
