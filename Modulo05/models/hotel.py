from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key = True) #criando as tabelas do meu banco, definindo a estrutura e os tipos
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1)) #quantas casas decimais
    diaria = banco.Column(banco.Float(precision=2))
    cidade = banco.Column(banco.String(40))


    def __init__(self, hotel_id,nome,estrelas,diaria,cidade): #criando o construtor para hotel
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def json(self): #função para converter o objeto em JSON
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas' : self.estrelas,
            'diaria' : self.diaria,
            'cidade' : self.cidade
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first() #seleciona todo os dados do cria_banco [select *from hoteis where hotel_id = hotel_id]
        if hotel:                                     #first== limit 1
            return hotel
        return None


    def save_hotel(self):
        banco.session.add(self) #ele vai saber quais argumentos a gente passou pra ele e vai salvar
        banco.session.commit() #vai fazer o commit, que sifnifica fim do processo

    def update_hotel(self, nome, estrelas,diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()
