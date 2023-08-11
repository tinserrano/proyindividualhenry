from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import pandas as pd


data = pd.read_csv("datasets/dataset.csv")

app = FastAPI()



@app.get('/peliculas_idioma/{idioma}')
def peliculas_idioma(idioma:str):
    count = data['language_name'].str.contains(idioma).sum()
    return {'idioma':idioma, 'cantidad':count}


@app.get('/peliculas_duracion/{pelicula}')
def peliculas_duracion(pelicula:str):
    '''Ingresas la pelicula, retornando la duracion y el año'''
    indice = data[data.title.str.contains(pelicula)].index.values
    respuesta = data.loc[indice, "runtime"].values.tolist()
    anio = data.loc[indice, "year"].values.tolist()
     
    return {'pelicula':pelicula, 'duracion':respuesta, 'anio':anio}


@app.get('/franquicia/{franquicia}')
def franquicia(franquicia:str):
    '''Se ingresa la franquicia, retornando la cantidad de peliculas, ganancia total y promedio'''
    data2 = data
    data2["collection_name"].fillna("", inplace=True)
    indice = data2[data2.collection_name.str.contains(franquicia)].index.values
    respuesta = len(data2.loc[indice, "year"])
    ganancia = data2.loc[indice, "return"].sum()
    promedio = data2.loc[indice, "return"].mean()
    return {'franquicia':franquicia, 'cantidad':respuesta, 'ganancia_total':ganancia, 'ganancia_promedio':promedio}

@app.get('/peliculas_pais/{pais}')
def peliculas_pais(pais:str):
    '''Ingresas el pais, retornando la cantidad de peliculas producidas en el mismo'''
    data3 = data
    data3["production_country_name"].fillna("", inplace=True)
    indice = data3[data3.production_country_name.str.contains(pais)].index.values
    respuesta = len(data3.loc[indice])
    return {'pais':pais, 'cantidad':respuesta}

@app.get('/productoras_exitosas/{productora}')
def productoras_exitosas(productora:str):
#     '''Ingresas la productora, entregandote el revunue total y la cantidad de peliculas que realizo '''
    data4 = data
    data4["production_companies_names"].fillna("", inplace=True)
    indice = data4[data4.production_companies_names.str.contains(productora)].index.values
    revenue = data4.loc[indice, "revenue"].sum()
    cantidad = len(indice)
    return {'productora':productora, 'revenue_total': revenue,'cantidad':cantidad}


@app.get('/get_director/{nombre_director}')
def get_director(nombre_director:str):
#     ''' Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. 
#     Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma. En formato lista'''
    data5 = data
    data5["crew_name"].fillna("", inplace=True)
    indice = data5[data5.crew_name.str.contains(nombre_director)].index.values
    retorno_total = data5.loc[indice, "revenue"].sum()
    peliculas = data5.loc[indice, "title"].values.tolist()
    anio = data5.loc[indice, "year"].astype(int).tolist()
    retornoPelicula = data5.loc[indice, "revenue"].astype(int).tolist()
    budget = data5.loc[indice, "budget"].astype(int).tolist()
    revenue_pelicula = (data5.loc[indice, "revenue"] - data5.loc[indice, "budget"]).astype(int).tolist()
    
    return {'director':nombre_director, 'retorno_total_director':retorno_total, 
            'peliculas':peliculas, 'anio':anio, 'retorno_pelicula':retornoPelicula, 'budget_pelicula':budget,'revenue_pelicula':revenue_pelicula}

# # ML
@app.get('/recomendacion/{titulo}')
def recomendacion(titulo:str):
    '''Ingresas un nombre de pelicula y te recomienda las similares en una lista'''
    data6 = data
    indice = data6[data6.title.str.contains(titulo)].index.values
    respuesta = data6.loc[indice, "recomendaciones"].values.tolist()
    return {'lista recomendada': respuesta} 