from flask_restful import Resource, reqparse  #libs importadas a partir do flask_restful
from models.hotel import HotelModel # a partir da pasta, o arquivo e a classe
from flask_jwt_extended import jwt_required

#array de dicionario, usado como banco de dados
hoteis =[
        {
        'hotel_id': 'alpha',
        'nome':'Alpha Hotel',
        'estrelas':4.3,
        'diaria':420.34,
        'cidade':'Rio de Janeiro'
        },
        {
        'hotel_id': 'gaucho',
        'nome':'Hotel do Gaucho',
        'estrelas':3.3,
        'diaria':120.34,
        'cidade':'Porto Alegre'
        },
        {
        'hotel_id': 'gato',
        'nome':'Gato Hotel',
        'estrelas':5.0,
        'diaria':520.34,
        'cidade':'Porto Alegre'
        }
]

#nao sei usar array coporation



class Hoteis(Resource):
    def get(self):
        #return hoteis
        return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}
        #select *from hoteis


class Hotel(Resource):
        #definindo o contrutor da classe
        #esse argumentos iriam se repetir nos metodos post e update, logo viraram atributos da classe
        argumentos = reqparse.RequestParser() #aqui especifico o tipo de informação que devem serem pasadas na crianção do meu novo hotel
        argumentos.add_argument('nome', type=str, required=True, help="the filter name can't left blank ") #aqui eu digo o tipo do campo, digo que ele é obrigatorio,
        argumentos.add_argument('estrelas',type=float, required=True, help="the fild estrelas can't left blank ")#e caso nao passe este campo, eu mando uma mensagem de erro
        argumentos.add_argument('diaria')
        argumentos.add_argument('cidade')

        # def find_hotel(hotel_id): #essa funçao serve para procurar o hotel, caso encontre ela retona ele, se nao ela retona nada
        #     for hotel in hoteis:
        #         if hotel['hotel_id'] == hotel_id: #se o id do hotel passado existir dentro do meu bacno (no caso na minha lista de
        #             return hotel                   #dicionarios), eentao ele retorna o hotel e seus dados
        #     return None #esta classe sera implementada em models de outra forma


        def get(self, hotel_id):
            hotel = HotelModel.find_hotel(hotel_id) #ele usa a funçao para retornar o hotel
            #variavel hotel, é instanciada, chamo a classe HotelModel, e chamo a funçaõ find_hotel, e passo o id do hotel
            if hotel: #caso encontre ele retorna o hotel
                return hotel.json()
            return {'message':'Hotel not found'} # retorna que o Hotel nao foi encontrado

        @jwt_required
        def post(self, hotel_id):
            if HotelModel.find_hotel(hotel_id):
                return {"message":"Hotel iD '{}' alread exists.".format(hotel_id)},400 #bad request



            dados = Hotel.argumentos.parse_args() #referenciando a classe, usando o nome HOTEL
            hotel = HotelModel(hotel_id, **dados) #agora sao objetos, e sao coletados  a partir da pasta models
            try:#tento salvar(usadno a função save_hotel)
                hotel.save_hotel()
            except: #caso nao consiga salvar, eu gero uma mensagem de erro com o codigo 500 (erro interno do servidor)
                {"message":"An internal error ocurred trying to save hotel."},500
            return hotel.json() #caso tudo funcione, eu retorno o objeto hotel convertido para json

            #novo_hotel = { 'hotel_id': hotel_id, **dados}
            #novo_hotel = hotel_objeto.json()#converto o objeto para JSON
            #hoteis.append(novo_hotel) #insere na lista o novo hotel cadastrado
            #return novo_hotel, 200  # codigo que diz que deu certo
        @jwt_required
        def put(self, hotel_id):
            dados =  Hotel.argumentos.parse_args() # ta pegando os dados atraves dos argumemtos passado
            #novo_hotel = { 'hotel_id': hotel_id, **dados} #ta criando um novo hotel, com a chave hotel_id e desembrulhando os dados
            hotel_encontrado = HotelModel.find_hotel(hotel_id) #hotel é instaciado, e usa a função para encontrar o hotel
            if hotel_encontrado:
                hotel_encontrado.update_hotel(**dados) #se eu encontrar o hotel eu faço uma atualizaçao
                hotel_encontrado.save_hotel()
                return hotel_encontrado.json(), 200 # retorno o valor atualizado e um OK
            #hoteis.append(novo_hotel) #caso nao exista (caso o ID do hotell nao exista), eu crio um novo
            hotel = HotelModel(hotel_id, **dados)
            try:
                hotel.save_hotel()
            except:
                {"message":"An internal error ocurred trying to save hotel."},500
            return hotel.json(), 201 #criado

        @jwt_required
        def delete(self, hotel_id):
            """
            global hoteis #variavel global
            hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id] #AQUI NAO ENTENDI
            return {'message':'Hotel deleted'}

            """

            hotel = HotelModel.find_hotel(hotel_id)
            if hotel:
                try:
                    hotel.delete_hotel()
                except:
                    {"message":"An internal error ocurred trying to Delete hotel"}, 500
                return {'message':'Hotel deleted'}
            return {'message':'Hotel not found'},404
