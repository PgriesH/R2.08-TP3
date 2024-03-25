import json
import copy
from datetime import datetime
import re


class Film:

    def __init__(self, titre, datesortie, note, avis):
        self.titre = titre
        self.datesortie = datesortie
        self.note = note
        self.listeavis = [avis]

    def get_titre(self):
        return self._titre

    def set_titre(self, newtitre):
        self._titre = newtitre

    titre = property(fget=get_titre, fset=set_titre)

    def get_releasedate(self):
        return self._datesortie

    def set_releasedate(self, newdatesortie):
        self._datesortie = newdatesortie

    datesortie = property(fget=get_releasedate, fset=set_releasedate)

    def get_note(self):
        return self._note

    def set_note(self, newnote):
        self._note = newnote

    note = property(fget=get_note, fset=set_note)

    def get_avis(self):
        return self._listeavis

    def set_avis(self, newavis):
        self._listeavis = newavis

    listeavis = property(fget=get_avis, fset=set_avis)

    def to_json(self):
        dico = {"titre": self.titre, "date": self.datesortie, "note": self.note, "avis": self.listeavis}
        return json.dumps(dico)

    def __str__(self):
        chaîne = "Le film " + self.titre + " est sorti le " + str(self.datesortie) + ","
        chaîne += " il a la note de " + str(self.note) + " et voici les avis du public l'ayant vu :\n"
        for avis in self._listeavis:
            chaîne += "- " + avis + "\n"
        return chaîne


class Bibliothèque:

    def __init__(self, listefilms):
        self._listefilms = listefilms

    def getlistefilms(self):
        return self._listefilms

    def setlistefilms(self, newlistefilms):
        self._listefilms = newlistefilms

    listefilms = property(fget=getlistefilms, fset=setlistefilms)

    def afficher_films(self):
        for x in self.listefilms:
            print(x.titre, x.datesortie, x.note)

    def mostrate(self):
        notemax = 0.0
        for x in self.listefilms:
            if x.note > notemax:
                notemax = x.note
                meilleur = x
        return meilleur

    def sorted(self):
        sorted = copy.deepcopy(self.listefilms)
        n = len(sorted)
        for i in range(n):
            for j in range(0, n - i - 1):
                if sorted[j].note < sorted[j + 1].note:
                    temp = sorted[j]
                    sorted[j] = sorted[j + 1]
                    sorted[j + 1] = temp
        return sorted

    def top3(self):
        sortedfilmlist = self.sorted()
        return sortedfilmlist[:3]

    def lastmovie(self):
        recent = None
        plusrecent = None
        for film in self.listefilms:
            match = re.findall("[0-9]{4}-[0-9]{2}-[0-9]{2}", film.datesortie)
            if match:
                filmdate = datetime.strptime(match[0], "%Y-%m-%d")
                if recent is None or filmdate > recent:
                    plusrecent = film
                    recent = filmdate
        return plusrecent

    def avrgnote(self):
        qt = 0
        somme = 0
        for x in self.listefilms:
            somme += x.note
            qt += 1
        moy = somme / qt
        return moy

    def fromjson(self, filename):
        with open(filename, "r") as file:
            data = json.load(file)
            for film in data["films"]:
                filmrecup = Film(film["titre"], film["date"], film["note"], film["avis"])
                self.listefilms.append(filmrecup)

    def to_json_file(self, filename):
        with open(filename, "w") as file:
            for film in self.listefilms:
                file.write(film.to_json())


if __name__ == "__main__":
    gladiator = Film("Gladiator", "2000-05-05", 4.5, "Incredible")
    gladiator.listeavis.append("Amazing")
    print(gladiator)
    film2 = Film("TEST", "2000-04-13", 4.0, "ahvuazbuiabazu")
    film3 = Film("test2", "2001-12-03", 5.0, "ezzffeezefefez")
    film4 = Film("ee", "2004-04-21", 3.5, "eeeveeeeeeeeeeeee")
    print("=====================================")
    print()
    biblio = Bibliothèque(listefilms=[gladiator, film2, film3, film4])
    biblio.afficher_films()
    print()
    print(f"Le film le mieux noté est : {biblio.mostrate().titre}")
    top3 = biblio.top3()
    print("TOP 3 :")
    for x in top3:
        print(f"{x.titre}")
    print()
    print()
    print(f"Le plus recent est : {biblio.lastmovie().titre}")
    print(f"La moyenne est de : {biblio.avrgnote()}")
    print("=============================================")
    print()
    biblio.fromjson("movie.json")
    biblio.afficher_films()
    for film in biblio.listefilms:
        print(film.to_json())

    biblio.to_json_file("films.json")
