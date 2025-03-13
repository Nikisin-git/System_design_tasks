workspace    {
    name "Сервис поиска попутчиков"
    !identifiers hierarchical
   
    model {
        user = Person "Пользователь"
      
        WebInterface = softwareSystem "Интерфейс сайта" {
            
            DB = container "База данных"{
                technology "PostgreSQL"
                
            }

           

           Journey = container "Поездка"{
            -> DB "Создание поездки" "PostgreSQL"
            technology "ReactJS"
           } 
           
           Route = container "Маршрут"{
                -> DB "Создание маршрута" "PostgreSQL"
                technology "Qt Location"
            }

           Traveller = container "Попутчик"{
            -> DB "Создание пользователя" "PostrgreSQL"
            -> Journey "Подключение пользователя""ReactJS"
            technology "ReactJS"
           }

           Search = container "Система поиска"{
            -> DB "Запрос на выборку" technology: "PostreSQL"
            -> user "Предоставить результат" technology "ElasticSearch"
            #-> Journey "Получение информации о поездке"
            #-> Traveller "Поиск пользователя по логину"
            #-> Traveller "Поиск имени и фамилии"
            #-> Route "Получение маршрута пользователя"
            technology "ElasticSearch"
            }
            
            
        }
             
                user -> WebInterface "Взаимодействие с интерфейсом сайта"  "ReactJS"
                user -> WebInterface.Search "Поиск пользователя по логину"  "ElasticSearch"
                user -> WebInterface.Search "Поиск имени и фамилии"  "ElasticSearch"
                user -> WebInterface.Search "Получение маршрутов пользователей"  "ElasticSearch"
                user -> WebInterface.Search "Получение информации о поездке"  "ElasticSearch"  
                
    }       

                
   
    
    
    views {
     themes default
        systemContext WebInterface "context" {
            include *
        }

        container WebInterface "c2" {
            include *
            autoLayout
        }   
       
       dynamic WebInterface "Publish"{
        WebInterface.Traveller -> WebInterface.Journey "Добавить попутчиков" "ReactJS"
        WebInterface.Journey -> WebInterface.DB "Опубликовать поездку" "PostgreSQL"
        WebInterface.DB -> WebInterface.Search "Вывести информацию о поездке" 
       
        }
     
    }
    
}