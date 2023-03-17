iri = "https://schema.org/"


def create_movie(title, year, poster, plot, graph):
    movie_id = '_'.join(title.lower().split())
    sparql_create = f"INSERT DATA {{ <{iri}{movie_id}> a <{iri}myMovie> }}"
    sparql_title = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}mytitle> \"{title}\" }}"
    sparql_year = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}myyear> \"{year}\" }}"
    sparql_poster = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}myposter> \"{poster}\" }}"
    sparql_plot = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}myplot> \"{plot}\" }}"
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
    sparql_create = f"INSERT DATA {{ <{iri}{actor_id}> a <{iri}myPerson> }}"
    sparql_name = f"INSERT DATA {{ <{iri}{actor_id}> <{iri}myname> \"{name}\" }}"
    graph.update(sparql_create)
    graph.update(sparql_name)


def insert_isActorOf(movie_id, actor_id, graph):
    sparql_1 = f"INSERT DATA {{ <{iri}{actor_id}> <{iri}isActor> <{iri}{movie_id}> }}"
    sparql_2 = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasActor> <{iri}{actor_id}> }}"
    graph.update(sparql_1)
    graph.update(sparql_2)

def insert_isDirectorOf(movie_id, director_id, graph):
    sparql_1 = f"INSERT DATA {{ <{iri}{director_id}> <{iri}isDirector> <{iri}{movie_id}> }}"
    sparql_2 = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasDirector> <{iri}{director_id}> }}"
    graph.update(sparql_1)
    graph.update(sparql_2)

def insert_isWriterOf(movie_id, writer_id, graph):
    sparql_1 = f"INSERT DATA {{ <{iri}{writer_id}> <{iri}isWriter> <{iri}{movie_id}> }}"
    sparql_2 = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasWriter> <{iri}{writer_id}> }}"
    graph.update(sparql_1)
    graph.update(sparql_2)

def insert_hasGenre(movie_id, genre, graph):
    sparql = f"INSERT DATA {{ <{iri}{movie_id}> <{iri}hasGenre> <{iri}{genre}> }}"
    graph.update(sparql)