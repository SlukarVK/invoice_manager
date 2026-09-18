Invoice Management API

REST API pro správu faktur vytvořené v Pythonu jako portfolio projekt.

Aplikace umožňuje vytvářet, zobrazovat, upravovat a mazat faktury. Součástí je také výpočet DPH, validace údajů a automatizované testy.

Použité technologie
Python 3.14
FastAPI
SQLAlchemy
Pydantic
SQLite
Uvicorn
pytest
Git / GitHub
Funkce
vytvoření nové faktury
zobrazení seznamu faktur
zobrazení konkrétní faktury
úprava faktury
smazání faktury
výpočet DPH a celkové částky
validace vstupních údajů
kontrola jedinečnosti čísla faktury
automatizované testování pomocí pytest
Databáze

Projekt používá SQLite databázi a SQLAlchemy jako ORM.

Faktura obsahuje například:

číslo faktury
dodavatele
datum vystavení
datum splatnosti
částku bez DPH
sazbu DPH
stav faktury

Aplikace zároveň kontroluje, že datum splatnosti není před datem vystavení.

API dokumentace

Po spuštění aplikace je interaktivní dokumentace dostupná na:

http://127.0.0.1:8000/docs

FastAPI automaticky poskytuje Swagger UI, kde je možné jednotlivé endpointy přímo vyzkoušet.

Příklad výpočtu DPH

Pro částku:

základ: 25 000 Kč
DPH: 21 %

aplikace vypočítá:

DPH: 5 250 Kč
celkem: 30 250 Kč
Testování

Projekt obsahuje automatizované testy pomocí pytest.

Testována je například:

práce s fakturami
vytváření a úprava záznamů
mazání faktur
validace vstupních údajů
výpočet DPH
práce s databází

Aktuálně testovací sada obsahuje 17 testů.

Spuštění testů:

pytest
Spuštění projektu
1. Klonování repozitáře
git clone https://github.com/SlukarVK/invoice_manager.git
cd invoice_manager
2. Vytvoření virtuálního prostředí

Windows:

python -m venv .venv

Aktivace:

.venv\Scripts\activate
3. Instalace závislostí
pip install -r requirements.txt
4. Spuštění aplikace
uvicorn app.main:app --reload

Aplikace bude dostupná na:

http://127.0.0.1:8000

Dokumentace API:

http://127.0.0.1:8000/docs

Projektové zaměření

Projekt vznikl jako praktická ukázka práce s Pythonem a moderním webovým frameworkem.

Při tvorbě jsem si procvičil:

strukturu Python projektu
REST API
práci s databází
ORM pomocí SQLAlchemy
validaci dat pomocí Pydantic
automatizované testování
práci s Git a GitHub
práci s virtuálním prostředím
Autor

Vojtěch Kún

Portfolio projekt vytvořený v rámci rozvoje znalostí Pythonu a backendového vývoje.