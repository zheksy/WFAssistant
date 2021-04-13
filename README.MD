# upute za pokretanje

## preduvjeti

python
pip
google chrome

potrebno je instalirati sve python module koje program zahtjeva uz pomoć PIPa.
google chrome mora imati dva plugina: wayfarer+, preko kojeg se simulira rad na tipkovnici
                                      SingleFile, koji sprema stranice kako bi se parsirale.

wayfarer+ mora biti podešen BEZ translation buttona jer su u konfliktu sa radom programa. također, button cooldown je preporučeno maksimalno 20 sekundi.
SingleFile mora biti podešen na "autosave all tabs" za vrijeme rada programa.

program je najbolje pokretati u izoliranom okruženju (npr. virutalna mašina) ali se može pokretati i na glavnom operacijskom sustavu.

## konfiguracija

potrebno je namjestiti putanju do defaultnog download foldera u fajlu *downloads_dir.txt*. u ovaj folder SingleFile sprema stranice koje služe za prepoznavanje reviewa.

u datoteci *accs_and_offsets.txt* navedeni su svi google računi koji su loginani u browseru, zajedno sa njihovim redoslijedom na listi. kako bi program radio, svi računi u *accs_and_offsets.txt* moraju već biti prisutni u browseru prilikom pokretanja.

ovo se namjesti tako da se odjavi sa gugl servisa, a računi sa logina se prepišu zajedno sa njihovim položajem na listi, ili po potrebi prijave novi računi. imena ne moraju biti točno prepisana, ali položaj mora.

## pokretanje programa

program se pokreće iz konzole sa komandom ```python3 ./AutoReview.py```. konzola se upali tako da se u traku direktorija napiše ```powershell```

program se prvo odlogira iz trenutnog wayfarer računa, nakon čega se logira u prvi zapisan u datoteci *accs_and_offsets.txt*. nakon toga počima proces reviewanja na osnovu podataka skupljenih manualnim reviewanjem. Aktualni račun radi review dok ne zatekne 5 submissiona kojih nema u bazi podataka, nakon čega se prebacuje na idući račun. 

u slučaju da se program NE pokreće u virtualnoj mašini, s obzirom na pristup simuliranja rada, za vrijeme pokretanja programa ne preporuča se ikakav drugi rad na računalu jer će poremetiti rad programa.

