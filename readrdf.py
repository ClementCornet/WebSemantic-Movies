import rdflib
g = rdflib.Graph()
g.parse("oui.owl")

q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?film WHERE {
        <http://www.semanticweb.org/cleme/ontologies/2023/2/untitled-ontology-17#travolta> <http://www.semanticweb.org/cleme/ontologies/2023/2/untitled-ontology-17#isActorOf> ?film
    }
"""

qres = g.query(q)
for row in qres:
    continue
    print(f"{row.film}")


g.update("""INSERT DATA { <z:> a <c:> }""")


all_q = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>

    SELECT ?a ?b ?c WHERE {
        ?a ?b ?c
    }
"""
print("bah")

all_qres = g.query(all_q)
for row in all_qres:
    print(f"{row.a} \t {row.b} \t {row.c}")


g.serialize("heu.owl", format="xml")