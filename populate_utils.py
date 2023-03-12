# importing the module
import json
 
# Opening JSON file
with open('example_film.json') as json_file:
    data = json.load(json_file)

import rdflib
#g = rdflib.Graph()
#g.parse("test.owl")

iri = "http://semanticweb.org/cleme/projet#"


def create_movie(title, year, poster, plot, graph):
    movie_id = '_'.join(title.lower().split())
    sparql_create = f"INSERT DATA {{ <{iri}{movie_id}> a <{iri}Movie> }}"
    sparql_title = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}title> \"{title}\" }}"
    sparql_year = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}year> \"{year}\" }}"
    sparql_poster = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}poster> \"{poster}\" }}"
    sparql_plot = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}plot> \"{plot}\" }}"
    graph.update(sparql_create)
    graph.update(sparql_title)
    graph.update(sparql_year)
    graph.update(sparql_poster)
    try:
        graph.update(sparql_plot)
    except:
        pass

def create_person(name, graph):
    actor_id = '_'.join(name.lower().split())
    sparql_create = f"INSERT DATA {{ <{iri}{actor_id}> a <{iri}Person> }}"
    sparql_name = f"INSERT DATA {{ <{iri}{actor_id}> <{iri}name> \"{name}\" }}"
    graph.update(sparql_create)
    graph.update(sparql_name)


def insert_isActorOf(movie_id, actor_id, graph):
    sparql_1 = f"INSERT DATA {{ <{iri}{actor_id}> <{iri}isActorOf> <{iri}{movie_id}> }}"
    sparql_2 = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasActor> <{iri}{actor_id}> }}"
    graph.update(sparql_1)
    graph.update(sparql_2)

def insert_isDirectorOf(movie_id, director_id, graph):
    sparql_1 = f"INSERT DATA {{ <{iri}{director_id}> <{iri}isDirectorOf> <{iri}{movie_id}> }}"
    sparql_2 = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasDirector> <{iri}{director_id}> }}"
    graph.update(sparql_1)
    graph.update(sparql_2)

def insert_isWriterOf(movie_id, writer_id, graph):
    sparql_1 = f"INSERT DATA {{ <{iri}{writer_id}> <{iri}isWriterOf> <{iri}{movie_id}> }}"
    sparql_2 = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasWriter> <{iri}{writer_id}> }}"
    graph.update(sparql_1)
    graph.update(sparql_2)

def insert_hasGenre(movie_id, genre, graph):
    sparql = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasGenre> <{iri}{genre}> }}"
    graph.update(sparql)

#a_name = "Victor Sjöström"
#sparql = f"""SELECT ?a ?d 
#WHERE {{ ?a  <{iri}name> ?d }}"""
#res = g.query(sparql)
#for row in res:
#    print(row)
#
#a_name = "Victor Sjöström"
#sparql = f"""SELECT ?a ?d 
#WHERE {{ ?a  <{iri}name> ?d }}"""
#res = g.query(sparql)
#for row in res:
#    print(row)

#create_movie(title="AAAAAAAAAAAAAAAAAAH", year=1111)

#insert_isActorOf("aaaaaaaaaaaaaaaaaah", "victor_sjöström")
#insert_hasGenre("aaaaaaaaaaaaaaaaaah", "Thriller")

#create_person("Ingmar Bergman")
#insert_isDirectorOf("aaaaaaaaaaaaaaaaaah","ingmar_bergman")
#insert_isWriterOf("aaaaaaaaaaaaaaaaaah","ingmar_bergman")

#g.serialize("test.owl", format="xml")