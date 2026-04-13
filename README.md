# praca_dyplomowa-
Tutuaj znajdują sie materiały mojej pracy dypolomowej. 
# DJ Audio Recommendation System 

## Opis

Aplikacja w Pythonie do analizy i rekomendacji utworów audio dla DJ-a.

## Funkcjonalności

* ekstrakcja cech audio (librosa)
* baza danych SQLite
* rekomendacje:

  * heurystyczne
  * ML (KNN + feature scaling)

## Jak używać

Dodanie utworu:
python3 cli.py song.mp3

Lista utworów:
python3 cli.py tracks

Rekomendacje ML:
python3 cli.py knn song.mp3

Usuwanie utworu:
python3 cli.py delete song.mp3

## Struktura projektu

* cli.py – CLI
* db.py – baza danych
* features.py – ekstrakcja cech
* recommendations.py – baseline
* ml_recommendations.py – KNN

## Autor

Mikołaj Malinowski 
