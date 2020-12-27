# foodgram-project

При старте проекта необходимо ввести две команды для создания Тегов и списка Ингредиентов

Создание ингредиентов - python manage.py fillingdb

Создание тегов - python manage.py tags

Проект запускается в трех контейнерах (через файл docker-compose.yaml)
Сам проект требует файл .env по адресу /foodgram/.env

Пример файла .env:\n
POSTGRES_DB=postgres          #это стандартрое имя БД. Вы можете создать свою в psql ручками
POSTGRES_USER=postgres        #это стандартный пользователь (не рекомендуется в использовании)
POSTGRES_PASSWORD=вашь пароль #тут все понятно (придумали, запомнили)
DB_HOST=db                    #это host из docker-compose.yaml обычно стоит localhost
DB_PORT=5432                  #стандартный порт postgres

Если хотите запустить проект локально, без контейнеров, для теста используйте sqlite3, (в данном проекте сохранены
настройки с базой sqlite3, они закомментированы)
если же хочется поиграть с postgres не забудте создать БД, пользователя и дать ему права на 
использование Вашей созданной БД, грамотно заполните .env файл.

вот адрес: http://178.154.230.11/
