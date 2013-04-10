e2-italiafilms
==============

<b>ItaliaFilms</b>, i migliori film dai siti italian di streaming online. Il plugin consente di vedere film in streaming 
sul nostro ricevitore enigma2 direttamente dai seguenti siti di streaming online: 

Cineblog01.org<br/>
BongStreaming.org<br/>
FilmPerTutti.tv<br/>
Film-Stream.tv<br/>
Terrafilms.tv<br/>

Sono supportati i seguenti servizi di hosting:
VK<br/>
NowVideo<br/>
Putlocker<br/>

Installazione:
Il plugin utilizza python-lxml per il parsing delle pagine HTML, è necessario quindi installare il pacchetto
tramite telnet o SSH:

opkg install python-lxml
 
Copiare quindi i file sorgenti dentro una cartella chiamata ItaliaFilms e copiare la cartella dentro:

/usr/lib/enigma2/python/Plugins/Extensions/

del vostro ricevitore, quindi riavviare enigma2 per rendere effettive le modifiche.

Questa è una versione beta e non tutti i film sono riproducibili. Se avete problemi con VK, una volta avviato il
film basta mettere in pausa la riproduzione finchè non compare il numero che indica la durata del film, a quel 
punto è possibile riavviare la rispoduzione.

thanks to subixonfire

Questo software è rilasciato sotto licenza Open Source GNU GPLv2 http://www.gnu.org/licenses/gpl-2.0.html
