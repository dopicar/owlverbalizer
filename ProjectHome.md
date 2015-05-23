**This project has moved to https://github.com/Kaljurand/owl-verbalizer**


---


OWL verbalizer is a tool that converts an OWL ontology into an Attempto Controlled English (ACE) text.

It can handle complex OWL formulas such as

```
man
    and (not (own some car))
    and (own some bike)
  SubClassOf inverse (likes) some ({Mary})
```

by turning them into natural English sentences such as:

```
Every man
    that owns a bike
    and
    that does not own a car
  is liked by Mary .
```

This conversion is designed to be reversible, i.e. one can convert the ACE representation back into OWL so that no loss in meaning occurs. For more of the theory and design choices behind the verbalization read section **5.6 Verbalizing OWL in ACE** of

> Kaarel Kaljurand. Attempto Controlled English as a Semantic Web Language.
> PhD thesis, Faculty of Mathematics and Computer Science, University of Tartu, 2007.
> http://attempto.ifi.uzh.ch/site/pubs/papers/phd_kaljurand.pdf

For a demo visit the [OWL verbalizer demo page](http://attempto.ifi.uzh.ch/site/docs/owl_to_ace.html).

OWL verbalizer is implemented in SWI-Prolog. It offers a command-line front-end and can also be run as an HTTP server. The input is expected to be in OWL 2 XML. The following example demonstrates launching the server and using it to verbalize an OWL/XML ontology from a remote repository.

```
$ ./owl_to_ace.exe -httpserver -port 5123 &

$ curl 'http://owl.cs.manchester.ac.uk/repository/download?
        ontology=http://www.co-ode.org/ontologies/pizza/pizza.owl&format=OWL/XML'
| curl -F "xml=<-" http://localhost:5123
```

The resulting ACE text will appear in STDOUT.


---


