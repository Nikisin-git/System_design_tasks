workspace {
    name "Travel companion search service"
    !identifiers hierarchical

    model {
        user = person "Пользователь"

        companion_search = softwareSystem "Сервис поиска попутчиков" {
        
           Route_API_db = container "База данных API маршрутов и поездок" {
                tags "Database"
                technology "MongoDB"    
            }


            auth_API_db = container "База данных аутентификации" {
                tags "Database"
                technology "PostgreSQL Database"

                description "Хранение хэшированных токенов и данных о пользоветялх"
            }

            API_cash = container "Кэш данных пользователей" {
                tags "Database"
                technology "Redis"

                description "Временно хранит информацию о пользователях"
            }

            auth_API = container "API аутентификации" {
                tags ""
                technology "Python FastAPI"

                description "Регистрация и валидация токенов"

                -> auth_API_db "Запрос в базу данных на сохранение данных пользователя" "SQL" 

                database_controller = component "Контроллер обращения к базе"{
                    
                    technology "Python"
                
                    description "Управляет подключением к базе данных и генерацией запросов"
                    -> auth_API_db "Чтение и сохранение токена" "SQL"
                }
                
                auth_controller = component "Контроллер аутентификации" {
                    
                    technology "Python FastAPI"
                
                    description "Регистрация и возвращение токена при аутентификации пользователя"

                    -> database_controller "AUTH_INFO"
                }

            }

            users_API = container "API пользователей" {
                tags ""
                technology "Python FastAPI"
            
                -> auth_API_db "Получение данных из запроса и помещение в базу" "SQL"
                -> auth_API "Валидирует токен" "JSON/HTTPS"

                database_controller = component "Контроллер обращения к базе" {
                    
                    technology "Python"
                
                    description "Управляет подключением к базе данных и генерацией запросов"
                    -> auth_API_db "читает и сохраняет" "SQL/TCP"
                }

                cash_controller = component "Контроллер кэша" {
                    technology "Redis"

                    description "Проверяет данные в кэше и получает их"
                    -> API_cash "Проверяет, получает и обновляет данные"
                }

                auth_controller = component "Контроллер авторизации" {
                    
                    technology "Python"
                
                    description "Входит в сервис авторизации за проверкой токена"
                    -> auth_API "Валидирует токен"
                }
                
                users_controller = component "Контроллер пользователей"{
                    
                    technology "Python FastAPI"
                
                    description "CRUD операции с пользователями"

                    -> database_controller "USER_INFO"
                    -> auth_API "Регистрирует/валидирует токен" "JSON/HTTPS"
                    -> auth_controller "token" 
                    -> cash_controller "Проверяет закешированы ли необходимые данные"
                }
            }

      

            Trip_API = container "API поездок" {
                tags ""
                technology "Python FastAPI"

                
                -> Route_API_db "Помещение данных о поездке, маршруте в базу"
                -> users_API "Запрашивает данные пользователя" "JSON/HTTPS"
               
                database_controller = component "Контроллер обращения к базе" {
                    
                    technology "Python"
                
                    description "Управляет подключением к базе данных и генерацией запросов"
                    -> Route_API_db "читает и сохраняет данные" 
                }

            cash_controller = component "Контроллер кэша" {
                    technology "Redis"

                    description "Проверяет данные в кэше и получает их"
                    -> API_cash "Проверяет, получает и обновляет данные"
                }

                auth_controller = component "Контроллер авторизации" {
                    
                    technology "Python"
                
                    description "Входит в сервис авторизации за проверкой токена"
                    -> auth_API "Валидирует токен" "JSON/HTTPS"
                }
                
                routes_controller = component "Контроллер маршрутов"{
                    
                    technology "Python FastAPI"
                
                    description "CRUD операции с маршрутами"

                    -> database_controller "ROUTE_INFO"
                    -> auth_controller "Регистрирует/валидирует токен" "JSON/HTTPS"

                }

                trips_controller = component "Контроллер поездок"{
                    
                    technology "Python FastAPI"
                
                    description "CRUD операции с поездками"

                    -> database_controller "TRIPS_INFO"
                    -> auth_controller "Регистрирует/валидирует токен" "JSON/HTTPS"
                    -> users_API "Валидация и обработка информации о пользователе" "JSON/HTTPS"
                }
            }

        
        }

        deploymentEnvironment "Docker" {
            deploymentNode "Docker Host" {
                technology "Docker Engine"
                description "Основной хост приложений"

                deploymentNode "Database Auth" {
                    technology "Postgres 14.8-alpine"
                    containerInstance companion_search.auth_API_db {   }
                }




                deploymentNode "Database Trip and Routes" {
                    technology "Mongo"
                    containerInstance companion_search.Route_API_db {  }
                }

                deploymentNode "User cash" {
                    technology "Redis"
                    containerInstance companion_search.API_cash { }   
                }

                deploymentNode "Services" {
                    infrastructureNode "app-network" {
                        technology "Docker Network"
                    }


              

                    companion_search.auth_API -> companion_search.auth_API_db "SQL"
                    companion_search.users_API -> companion_search.auth_API "HTTP"
                    companion_search.Trip_API -> companion_search.auth_API "HTTP"
                    companion_search.Trip_API -> companion_search.users_API "HTTP"
                }
            }
        }
        


        user -> companion_search "Использование сервиса для подбора попутчиков"
        user -> companion_search.Trip_API "Подключение к поездке"
        user -> companion_search.users_API "Регистрация, получение списка пользователей"
        user -> companion_search.auth_API "Получение токена"
        
        user -> companion_search.Trip_API.trips_controller "Инициализирует запросы к API" "JSON/HTTPS"
        user -> companion_search.Trip_API.routes_controller "Инициализирует запросы к API" "JSON/HTTPS"

        user -> companion_search.users_API.users_controller "Инициализирует запросы к API" "JSON/HTTPS"

        user -> companion_search.auth_API.auth_controller "Инициализирует запросы к API" "JSON/HTTPS"

        
    }

    views {

        themes default

        styles {
            element "Database"{
                shape Cylinder
            }
        }

        systemContext companion_search "context_comp" {
            include *
            autoLayout
        }


        container companion_search "c2" {
            include *
            autoLayout
        }

        component companion_search.auth_API "c3_auth" {
            include *

            autoLayout
        }

        component companion_search.users_API "c3_users" {
            include *

            autoLayout
        }


        component companion_search.Trip_API "c3_companion_search" {
            include *

            autoLayout
        }

        deployment * "Docker"{
            include *
            autoLayout
        }

        dynamic companion_search "CreateTrip" "Создание поездки" {
            autoLayout

            user -> companion_search.auth_API "отправляет логин и пароль и получает токен"
            user -> companion_search.Trip_API "Отправляет информацию о поездке"
            companion_search.Trip_API -> companion_search.users_API "валидирует добавляемых пользователей"
            companion_search.users_API -> companion_search.auth_API "валидирует токен"
            companion_search.Trip_API -> companion_search.Route_API_db "Сохраняет данные"
            companion_search.Trip_API -> user "Возвращает данные о созданной поездке"
        }

    } 
}
