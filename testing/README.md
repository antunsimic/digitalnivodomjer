### `vodomjeri.db`
- baza bez podataka za ožujak.


### `files` 
- direktorij s datotekama očitanja vodomjera za ožujak (i bankovnim izvodima plaćanja usluge za evidenciju)

## Postupak

1. Pokrenuti web stranicu (React server localhost:3000 i Python server localhost:5000)
2. na stranici `Uvid u bazu podataka` uploadati vodomjeri.db.
3. sve datoteke iz `files` odjednom označiti i povući do kvadrata za tu namjenu na stranici za upload datoteka očitanja.
4. kliknuti `Unos u bazu`
5. Čekati na povratnu informaciju (par sekundi) da je unos bio uspješan
6. Downloadati vodomjeri.db nakon obavljenih modifikacija
7. Formirati izvještaje na odgovarajućoj stranici klikom na odgovarajući gumb, i opcionalno downloadati te izvještaje
8. Na stranici `Slanje mailova` klikom na gumb poslati izvještaje na adrese e-pošte specificirane u bazi podataka.


