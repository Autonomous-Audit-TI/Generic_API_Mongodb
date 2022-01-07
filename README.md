# Criadores do projeto em 02/01/2022
# Alexandre Novaes Iosimura - alexandre.iosimura@gmail.com 
# Jean Guilherme Galinhamo - Gui.jean5323@gmail.com
# git clone https://github.com/Autonomous-Audit-TI/Generic_API_Mongodb
#  -------------------------------------------------------------------------------------
# Flask-Mongodb & Python 3 - API - MONGODB - Self Managed by Front-end calls
# ######################################################################################
# **Abstracted API for dynamic CRUD with Flask & Mongodb** #

## Requirments
```
	- pip3 install pipenv
	- Please see requirements.txt for extra info or envir. intall

```

## Usage (Generic)
```
	- git clone https://github.com/Autonomous-Audit-TI/Generic_API_Mongodb
	- pipenv install -r requirment.txt
	- pipenv shell
	- python app.py

```

# app_mongodb Send it first and GET your key ( E.g. http://127.0.0.1:5000/mongo_login) 
# Wait for this return:

{
    "key": "Qw14lrkm7ooupXwwRNQKz0bcrAW2EB95lTWbkmjiIRk"
}

# app_mongodb Using the Key to call one insert POST [E.g. http://127.0.0.1:5000/mongo_insert_one ]
[
    {
        "key": "Qw14lrkm7ooupXwwRNQKz0bcrAW2EB95lTWbkmjiIRk",
        "table_name": "tbl_demonstracao"
    },
       {
        "Nome_Completo": "Alexandre Novaes Iosimura",
        "Telefone": "+1 (000) 000 00000",
        "Endereco": "East York - Toronto - ON",
        "Proprietario":"Maria das coves",
        "Carro":"Chevrolet Cruize",
        "Modelo":"Rebaixado e sem manutenção",
        "Ano":2019,
        "Data de fabricação": "2014-03-01T08:00:00Z"
    }
]
>>>>>>> 172a036 (Second commit)

# app_mongodb Using the Key to call one delet one POST [E.g. http://127.0.0.1:5000/mongo_delete_one ]

[
    {
        "key": "ECbO0ozhPdueFVCKnsGRzOsiUhRVseDikQY2vdFqFwc",
        "table_name": "tbl_clientes",
        "col_name": "nome"
    },
    {
        "word": "Jean Guilherme Galinhamo"
    }
]


# app_mongodb Using the Key  to call  mongo_find_all  POST [E.g. http://127.0.0.1:5000/mongo_find_all]

[
    {
        "key": "ECbO0ozhPdueFVCKnsGRzOsiUhRVseDikQY2vdFqFwc",
        "table_name": "tbl_clientes"
    }
]


# app_mongodb Using the Key to call mongo_list_database_names POST [E.g. http://127.0.0.1:5000/mongo_list_database_names]

[
    {
        "key": "ECbO0ozhPdueFVCKnsGRzOsiUhRVseDikQY2vdFqFwc"
    }
]

# app_mongodb Using the Key to call mongo_search POST [E.g. http://127.0.0.1:5000/mongo_search]
# Thanks to Ahmed (Saad - Pakistan) to start this new class and put me on the game to complete the regex args 

[
    {
        "key": "rFWwOWACa3T82DqLTb-VLmZGm4on37OV085_Dw6yE0Y",
        "table_name": "tbl_clientes",
        "col_name": "Nome_Completo"
    },
    {
        "word": "Alexandre"
    }
]

<img src='https://github.com/Autonomous-Audit-TI/Generic_API_Mongodb/blob/main/logo.png'>
