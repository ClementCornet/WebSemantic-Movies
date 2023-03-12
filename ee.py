import rdflib
g = rdflib.Graph()
g.parse("movies_project.owl", format="n3")
g.serialize("movies_project.owl", format="xml")