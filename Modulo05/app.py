from flask import Flask, jsonify
from flask_restful import Api
from resources.hotel import Hoteis, Hotel  #a partir da pasta resources, pegeue o arquivo hotel, e pegue a classe Hotel
from resources.usuario import User, UserRegister, UserLogin, UserLogout
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST


app = Flask (__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db' #se quiser mudar para qualquer banco, vou mudar so aqui
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #rastrea as modificaçoes
app.config['JWT_SECRET_KEY']= 'DontTellAnyone' #chave secreta
app.config['JWT_BLACKLIST_ENABLED']=True  # deianxo a black lista ativada
api = Api (app)
jwt = JWTManager(app)


@app.before_first_request #nem aqui
def cria_banco():
    banco.create_all()

@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    return token['jti'] in BLACKLIST

@jwt.revoked_token_loader
def token_de_acesso_invalido():
    return jsonify({'message':'You have been logged out.'}), 401




api.add_resource(Hoteis, '/hoteis') #endpoint para retornar todos os hoteis
api.add_resource(Hotel, '/hoteis/<string:hotel_id>') #endpoint que retorna o hotel pelo o id
api.add_resource(User,'/usuarios/<int:user_id>')
api.add_resource(UserRegister,'/cadastro')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')


if __name__ == '__main__' : #padroa flask para chamar um arquivo
    from sql_alchemy import banco
    banco.init_app(app)

    app.run(debug = True)

#http://127.0.0.1:5000/hoteis --> local onde minha aplicação esta sendo rodada
