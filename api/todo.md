~~DL2~~

~~1. Add person-location relation (who added the location)~~

~~2. Update diagram~~

~~DL3~~

~~1. Dokumentoi 5 resurssia. Metodeja GET PUT POST DELETE käytettävä kaikkia vähintään kahdesti.~~

~~2. Toteuta resurssit (tiedostot)~~

~~3. Kokoa resurssit toimivaksi app.py~~

~~4. Tee populaatio skriptit (populate.py)~~

~~5. Dokumentoi kaikki~~

~~6. Tee testit~~

~~7. Viimeistele~~

~~7.1 Tarkista layout~~

~~7.2 Tarkista REST conformance~~

~~7.3 Tee palautus ja varaa aika~~


~~Kysy:~~

~~DL1 arvostelu = pisteet saahaan lopuksi~~

~~meeting notes = ei tarvi tehä~~

~~jäsenen poisto ryhmästä = nimi vaan pois~~

~~palautusten korjaus = arvioidaan lopuksi~~


DL3 fixit:
  
Korjaa addressability, 

pylint-korjaukset (docstringit, )

vaihda game validation käyttämään checkeriä regexin sijaan

caching

authentication


Muut fixit:

setup.py requirements.txt:n tilalle

yhdistä converterit ja laita ne utils.py 

id:t urleista pois tai hashaa ne

PUT 200 -> 204

