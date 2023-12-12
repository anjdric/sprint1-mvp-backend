from sql_alchemy import database


class HotelModel(database.Model):
    __tablename__ = 'hotel'
    hotel_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    nome = database.Column(database.String(50))
    estrelas = database.Column(database.Float(precision=1))
    diaria = database.Column(database.Float(precision=2))
    cidade = database.Column(database.String(50))
    uf = database.Column(database.String(2))
    url_image = database.Column(database.String(4000), nullable=True, default="")
    url_youtube = database.Column(database.String(1000), nullable=True, default="https://www.youtube.com/watch?v=dWRutjjigsQ")
    url_instagran = database.Column(database.String(1000), nullable=True, default="https://www.instagram.com/hoteis")
    url_facebook = database.Column(database.String(1000), nullable=True, default="https://www.facebook.com")
    # Define o cadastro como um hotel validado no sistema
    checked = database.Column(database.Boolean, default=False)
    # Define o cadastro como ativo no sistema
    active = database.Column(database.Boolean, default=False)
    # Define o relacionamento com o usuário vinculado
    user_id = database.Column(database.Integer, database.ForeignKey('usuario.user_id'))

    def __init__(self, hotel_id, nome, estrelas, diaria, cidade, uf,
                 url_image, url_youtube, url_instagran, url_facebook,
                 user_id):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade
        self.uf = uf
        self.url_image = url_image
        self.url_youtube = url_youtube
        self.url_instagran = url_instagran
        self.url_facebook = url_facebook
        self.active = True
        self.checked = False
        self.user_id = user_id

    def json(self):
        return {
            'hotel_id': self.hotel_id,
            'nome': self.nome,
            'estrelas': self.estrelas,
            'diaria': self.diaria,
            'cidade': self.cidade,
            'uf': self.uf,
            'url_image': self.url_image,
            'url_youtube': self.url_youtube,
            'url_instagran': self.url_instagran,
            'url_facebook': self.url_facebook,
            'active': self.active,
            'checked': self.checked,
            'user_id': self.user_id
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        hotel = cls.query.filter_by(hotel_id=hotel_id).first()
        if hotel:
            return hotel
        return None

    def save_hotel(self):
        database.session.add(self)
        database.session.commit()

    def update_hotel(self, nome, estrelas, diaria, cidade):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.cidade = cidade

    def delete_hotel(self):
        database.session.delete(self)
        database.session.commit()
