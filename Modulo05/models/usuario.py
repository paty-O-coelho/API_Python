from sql_alchemy import banco

class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key = True) #criando as tabelas do meu banco, definindo a estrutura e os tipos
    login = banco.Column(banco.String(40))
    senha = banco.Column(banco.String(40))


    def __init__(self, login, senha): #criando o construtor para hotel
        self.login = login
        self.senha = senha

    def json(self): #função para converter o objeto em JSON
        return {
            'user_id': self.user_id,
            'login': self.login

        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first() #seleciona todo os dados do cria_banco [select *from hoteis where hotel_id = hotel_id]
        if user:                                     #first== limit 1
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None


    def save_user(self):
        banco.session.add(self) #ele vai saber quais argumentos a gente passou pra ele e vai salvar
        banco.session.commit() #vai fazer o commit, que sifnifica fim do processo


    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
