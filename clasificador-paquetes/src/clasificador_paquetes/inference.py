import csv
from pathlib import Path
import joblib
from .contracts import Entrada, Salida
import pandas as pd


def leer_csv(ruta: Path) -> list[Entrada]:
    # TODO
    paquetes = list()
    with open(ruta, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for rows in reader:
            try:
                new_entrada = Entrada(**rows)
                paquetes.append(new_entrada)
            except:
                    raise ValueError
    return paquetes
    raise NotImplementedError


def preprocesar(entrada: Entrada) -> list[float]:
    # TODO
    resultado = list()
    peso_redondeado = round(entrada.peso_kg, 1)
    resultado.append([peso_redondeado,entrada.distancia_km])

    return resultado
    raise NotImplementedError


def cargar_modelo(ruta: Path):
    # TODO
    modelo = joblib.load(ruta)
    return modelo
    raise NotImplementedError


def predecir(entrada: Entrada, modelo) -> Salida:
    # TODO
    valores = preprocesar(entrada)
    id_paquete = entrada.id_paquete
    categoria = modelo.predict(valores)
    if categoria == "urgente":
        confianza = modelo.predict_proba(valores)[0][1]
    else:
        confianza = modelo.predict_proba(valores)[0][0]

    dict_resultado ={'id_paquete': id_paquete, 'categoria': categoria, 'confianza': confianza}
    resultado = Salida(**dict_resultado)

    return resultado
    raise NotImplementedError


def guardar_csv(resultados: list[Salida], ruta: Path) -> None:
    # TODO
    df = pd.DataFrame(columns=['id_paquete','categoria','confianza'])
    for i in resultados:
        df.loc[len(df)] = [i.id_paquete, i.categoria, i.confianza]
    df.to_csv(ruta)

    raise NotImplementedError


def ejecutar(entrada: Path, modelo: Path, salida: Path) -> None:
    # TODO
    lista_entrada = leer_csv(entrada)
    lista_salida = list()
    model = cargar_modelo(modelo)

    for i in lista_entrada:
        resultado_predict = predecir(i, model)
        lista_salida.append(resultado_predict)

    guardar_csv(lista_salida, salida)
    
    
    raise NotImplementedError


if __name__ == "__main__":
    ejecutar(
        Path("data/raw/paquetes.csv"),
        Path("models/modelo.joblib"),
        Path("resultados.csv"),
    )
