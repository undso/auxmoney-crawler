# auxmoney-crawler
### Tool zum Auslesen der aktuellen Kontostände bei Auxmoney

Der Crawler prüft einmal im Monat die eingegangenen Rückflüsse, den Kontostand und den aktuellen Rendite Index.
Diese Daten werden dann via Telgram bereitgestellt.

Aufruf: 

`docker container run -d --restart=always --env-file=env_file --name auxmoney-crawler undso/auxmoney-crawler`

Konfiguration:

| Parameter | Beschreibung |
|:------------------|:------------------|
| USERNAME | Der Auxmoney Benutzername |
| PASSWORD | Das Auxmoney Password |
| TELEGRAMBOTKEY | Key des Telegram Bots |
| CHATID | ChatId des Chates in welchen die Daten kommuniziert werden sollen. |
| PICTUREPATH | Pfad unter welchem Screenshots der einzelnen Seitenaufrufe abgelegt werden. |


