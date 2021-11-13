
import requests
import json
import sqlite3




def buscar_dados():
    x = '0'
    while (x == '0'):

    #banco
        banco = sqlite3.connect('bancocnpj.db')
        cursor = banco.cursor()
    #menu
        menu = input('buscar por empresa(cnpj) -> 1 \nbuscar por serviço -> 2 \nBuscar todas empresas -> 3\nSair -> 4\n:')
        cnpj = input('digite o cnpj : ')

    #request
        request = requests.get('https://www.receitaws.com.br/v1/cnpj/' + str(cnpj))
        todos = json.loads(request.content)

    #variaveis da api
        nome = todos['nome']
        uf = todos['uf']
        telefone = todos['telefone']
        email = todos['email']
        data_situacao = todos['data_situacao']
        principal = todos['atividade_principal']
        secundaria = todos['atividades_secundarias']
        arraysecundaria = []
        for principal in todos['atividade_principal']:
            atividade_principal =principal['text']

        for secundaria in todos['atividades_secundarias']:
            arraysecundaria.append(secundaria['text'])


        if (menu == '1'):
            print(todos['nome'])
            print(todos['uf'])
            print(todos['telefone'])
            print(todos['email'])
            print(todos['data_situacao'])


            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name ='cnpj_tb'")
            resultado = cursor.fetchone()
            if (1 in resultado):

                cursor.execute("SELECT cnpj FROM cnpj_tb WHERE cnpj={} ".format(cnpj))
                result = cursor.fetchone()
                if result:
                    print('ja existe no banco')
                else:
                    #print('adicionado ao banco')
                    cursor.execute(
                        "INSERT INTO cnpj_tb  VALUES('{}','{}','{}','{}','{}','{}','{}')".format(nome, uf, telefone,email, data_situacao,atividade_principal,cnpj))
                    banco.commit()



                    for item in arraysecundaria:
                        cursor.execute("INSERT INTO atividades_secundarias_tb VALUES('{}','{}')".format(item, cnpj))
                        banco.commit()

            if(0 in resultado):

                cursor.execute("CREATE TABLE cnpj_tb(nome TEXT,uf TEXT,telefone TEXT,email TEXT,data_situacao TEXT,atividade_principal TEXT,cnpj INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT )")
                cursor.execute("INSERT INTO cnpj_tb  VALUES('{}','{}','{}','{}','{}','{}','{}')".format(nome, uf, telefone,email,data_situacao,atividade_principal, cnpj))
                banco.commit()
                cursor.execute("CREATE TABLE atividades_secundarias_tb(atividades_secundarias TEXT, cnpj_key INTEGER, FOREIGN KEY(cnpj_key) REFERENCES cnpj_tb(cnpj))")
                banco.commit()
                for item in arraysecundaria:
                    cursor.execute("INSERT INTO atividades_secundarias_tb VALUES('{}','{}')".format(item,cnpj))
                    banco.commit()


        if(menu == '2'):
            cursor.execute("SELECT nome,atividade_principal FROM cnpj_tb  WHERE cnpj ='{}' ".format(cnpj))
            print(cursor.fetchall())

        if(menu == '3'):
            cursor.execute("SELECT * FROM atividades_secundarias_tb WHERE cnpj_key ='{}' ".format(cnpj))
            print(cursor.fetchall())

        if(menu == '4'):
            x = '1'
            print('até logo')


if __name__ == '__main__':
    buscar_dados()
