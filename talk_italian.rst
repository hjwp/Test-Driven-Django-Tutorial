OBIDIRE ALLA CAPRA! - Un tutorial TDD con Selenium e Django
===========================================================

*Harry Percival*
@hjwp
https://tdd-django-tutorial.com
https://github.com/hjwp/Test-Driven-Django-Tutorial
https://www.pythonanywhere.com


















Introduzione
------------

* l'Italiano
* l'Inglese, gli Americani
* lingagio technico




















Voi
---

* chi conosce Django? Python? TDD? Selenium?

Io
--

* Sestri Levante
* il primio progetto
* Resolver Systems & PythonAnywhere















Oggi
----

* il tutorial officiale di Django
  - a poll / voting app (come si dice?)
* col TDD!
* primo, i "functional test"
  - test funzionali? test di integrazione?
* poi, i "unit test"
  - test unitari? 
* e solo doppo, il codice applicativo
* **le domande, per prigiera** 
   - non fare sempre "si"
   - e anche le correzione del' Italiano












Anteprima
---------

PART 1  - il sito admin
* il primo modello
* lo setup di Django, Selenium, il test runner
* models.py, admin.py

PART 2
* (Blue Peter)
* il Django Test Client
* views.py
* templates

PART 3 (si c'i arriviamo)
* forms
* refactoring









PART 1
------

=====================================   ==================================
Ogettivo                                Come si vede
=====================================   ==================================
Setup di Django                         Usare il *Django test server* e 
                                        navighiamo al manuale a la pagina
                                        "Hello World" 
-------------------------------------   ----------------------------------
Setup del' sito admin                   Iniziamo il primo *functional test*,
                                        che usa il sito admin
-------------------------------------   ----------------------------------
Il primo Model per gli ogetti "Poll"    Continuamo il primo FT, che deve
                                        creare un "Poll" tramite lo sito 
                                        admin. I primi test unitari 
=====================================   ==================================

