# Receptník

[![Licence](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

- Projekt do **EBC-PYT**.
- Webový portál, kde mohou uživatelé hledat recepty, hodnotit je či přidávat své vlastní.
- Aby mohli s recepty uživatelé pracovat, budou si muset na webu vytvořit účet, přes který budou tyto operace provádět.
- Kromě webového rozhraní pro uživatele aplikace obsahuje také receptové API, pro programátorské kolegy.
- V API si uživatelé mohou vytvořit svůj přístupový klíč a používat tak naši aplikaci pro své vlastní vývojářské účely.
- API slouží výhradně pro získávání receptů ve formě JSON/XML - nelze přes něj recepty mazat, vytvářet upravovat či
  hodnotit.
- Aplikace produkčně běží zde: http://www.receptnik.tk

## Autoři

- **Lucie Pacáková**
- **Lucie Suchánková**
- **Petr Chatrný**

## Použité technologie

|                |                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
|----------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Frontend       | ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white) |
| Backend        | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)                                                                                                                                                                                                                                              |
| Development DB | ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)                                                                                                                                                                                                                                                                                                                                               |
| Production DB  | ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)                                                                                                                                                                                                                                                                                                                                       |
| Server         | ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white)                                                                                                                                                                                                                                                                                                                                           |
| Hosting        | ![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white)                                                                                                                                                                                                                                                                                                                                               |

## Sestavení aplikace

```bash
# získání zdrojového kódu
mkdir receptnik
cd receptnik
git clone https://vase_uzivatelske_jmeno@bitbucket.org/Lucie02/python-receptnik.git
cd python-receptnik

# nastavení virtuálního prostředí pythonu
python3 -m venv venv
. venv/bin/activate

# nainstalování závislostí
pip3 install -r requirements.txt

# nastavení enviromentálních proměnných
export FLASK_APP=src/app.py:app
export FLASK_ENV=development
export FLASK_DEBUG=1

# spuštění aplikace
flask run
```

## Sestavení aplikace - Docker

```bash
mkdir receptnik
cd receptnik
git clone https://vase_uzivatelske_jmeno@bitbucket.org/Lucie02/python-receptnik.git
cd python-receptnik

docker image build -t receptnik .
docker run -p 5000:5000 -d receptnik
```

## Případy užití

![](docs/usecase-diagram.png)

## ERD databáze receptníku

![img.png](docs/db-diagram.png)

## Frontend routy

| Popis             | Metoda | Cesta                | Soubor                  | Veřejně dostupné |
|-------------------|--------|----------------------|-------------------------|------------------|
| Domovská stránka  | GET    | /                    | index.html              | ano              |            
| Seznam receptů    | GET    | /recepty             | recipe_list.html        | ne               |
| Recept detailně   | GET    | /recept/<id>         | recipe.html             | ne               |   
| Dokumentace       | GET    | /dokumentace         | documentation.html      | ano              |    
| Uživatelův profil | GET    | /uzivatel            | user.html               | ne               |    
| Přihlášení        | GET    | /prihlaseni          | login.html              | ano              |     
| Registrace        | GET    | /registrace          | register.html           | ano              |       
| Obnova hesla      | GET    | /obnova-hesla        | reset_password.html     | ano              |         
| Nové heslo        | GET    | /nove-heslo/<token>  | new_password.html       | ano              |           
| Vytvoření receptu | GET    | /vytvoreni-receptu   | create_recipe_form.html | ne               |            
| Úprava receptu    | GET    | /uprava-receptu/<id> | edit_recipe_form.html   | ne               |             
| Vytvoření klíče   | GET    | /vytvorit-klic       | key_form.html           | ne               |
| Odhlášeno         | GET    | /odhlaseno           | message.html            | ano              |
| Rozloučení        | GET    | /rozlouceni          | message.html            | ano              |

## API routy

| Popis                     | Metoda | Cesta                           | Soubor       | Dostupné s API klíčem |
|---------------------------|--------|---------------------------------|--------------|-----------------------|
| Přihlášení uživatele      | POST   | api/users/login                 | -            | ne                    |
| Odhlášení uživatele       | POST   | api/users/logout                | -            | ne                    |
| Registrace uživatele      | POST   | api/users/register              | -            | ne                    |
| Potvrzení registrace      | GET    | api/users/confirm-email/<token> | message.html | ne                    |
| Žádost o obnovu hesla     | POST   | api/users/forgot-password       | -            | ne                    | 
| Nastavit nové heslo       | POST   | api/users/<id>/update-password  | -            | ne                    | 
| Upravit uživatele         | PUT    | api/users/<id>                  | -            | ne                    |
| Smazat uživatele          | DELETE | api/users/<id>                  | -            | ne                    |
| Seznam receptů            | GET    | api/recipes                     | -            | ano                   |
| Detailní recept           | GET    | api/recipes/<id>                | -            | ano                   |
| Vytvořit recept           | POST   | api/recipes                     | -            | ne                    |
| Upravit recept            | PUT    | api/recipes/<id>                | -            | ne                    |
| Smazat recept             | DELETE | api/recipes/<id>                | -            | ne                    |
| Ohodnotit recept          | POST   | api/recipes/<id>/rate           | -            | ne                    |
| Seznam ingrediencí        | GET    | api/ingredients                 | -            | ano                   |
| Seznam typů jídel         | GET    | api/food-types                  | -            | ano                   |
| Vytvořit API klíč         | POST   | api/api-keys                    | -            | ne                    |
| Změnit aktivitu API klíče | POST   | api/api-keys/<id>/activation    | -            | ne                    |
| Smazat API klíč           | DELETE | api/api-keys/<id>               | -            | ne                    |
