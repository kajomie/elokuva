- Tässä sovelluksessa käyttäjät pystyvät pitämään kirjaa katsomistaan elokuvista kirjoittamalla niille arvosteluja. Käyttäjä näkee elokuvasta tietoja kuten esimerkiksi sen nimen, ohjaajan, valmistumisvuoden, sekä lyhyen juonikuvauksen.
- Käyttäjä voi luoda tunnuksen ja kirjautumaan tunnuksillaan sisään.
- Käyttäjä voi lisätä elokuvia (jos sitä ei jo löydy sovelluksesta), ja muokkaamaan ja poistamaan niitä.
- Käyttäjä voi nähdä ja selata sovellukseen lisättyjä elokuvia.
- Käyttäjä voi etsiä elokuvia sovelluksesta hakusanoilla.
- Käyttäjä voi valita lisäämälleen elokuvalle genreluokitteluja (esim. kauhu, draama, komedia jne.)
- Käyttäjäsivulta voi nähdä kunkin käyttäjän kirjoittamat arvostelut ja tämän lisäämät elokuvat.
- Käyttäjä pystyy kirjoittamaan elokuvalle arvostelun ja antamaan sille oman arvosanan, sekä lukea muiden käyttäjien kirjoittamia arvosteluja ja nähdä elokuvalle annetun keskivertoarvosanan.
Pääasiallisena tietokohteena on itse elokuva, ja toissijaisena tietokohteena on käyttäjän kirjoittama arvostelu.

Kun sovellus on kloonattu, niin se voidaan ottaa käyttöön seuraavasti:<br>
python3 -m venv venv<br>
source venv/bin/activate<br>
pip install flask<br>
sqlite3 database.db < schema.sql<br>
sqlite3 database.db < init.sql<br>
flask run

<br>
<br>
Etusivun kuva on osoitteesta:<br>
https://pixabay.com/photos/theatre-chairs-red-audience-4783908/
<br>
Image by <a href="https://pixabay.com/users/sebastiangoessl-3360479/?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4783908">Sebastian Gößl</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=image&utm_content=4783908">Pixabay</a>.<br>
Image is free for use under the Pixabay Content License.