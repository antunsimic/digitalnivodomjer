# digitalni vodomjer

Potrebno je izraditi web aplikaciju sa sljedećim funkcionalnostima: 

Učitavanje txt datoteke stanja vodomjera koju generira uređaj za daljinsko očitavanje brojila. Primjer: rfu.txt. U jednoj rfu.txt datoteci je očitano stanje vodomjera u X zgrada 

Za svaku od X zgrada iz stanja vodomjera iz rfu.txt potrebno je napraviti izvještaj za svaku zgradu u PDF formatu. Primjer: izvjestaj_zgrada.pdf 

Slanje formiranih izvještaja na adrese e-pošte stambenih zgrada  

Za svaku od X zgrada iz stanja vodomjera iz rfu.txt potrebno je  napraviti izvještaj za Vodovod u XLS  formatu. Primjer: izvjestaj_voda.xls 

Slanje svih formiranih XLS-a u jednoj poruci na adresu e-pošte distributera vode za potrebe izrade računa za potrošnju vode (npr. Vodovod d.o.o., za zgrade u Slavonskom Brodu) 

Učitavanje bankovnih izvoda s uplatama korisnika vodomjera za uslugu očitavanja vodomjera. Primjer: IZV_HR2924070001100072069_01092023-30092023.otp datoteka. 

Po mogućnosti u DBMS, kao što je MySQL  ili Microsoft Access.

- strojno učenje za predviđanje potrošnje: aplikacija predviđa buduću potrošnju vode na temelju povijesnih podataka.
- vizualizaciju potrošnje kroz grafove, mogućnost filtriranja i sortiranja stanova po potrošnji
