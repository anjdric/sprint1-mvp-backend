from sql_alchemy import database


class UsuarioModel(database.Model):
    __tablename__ = 'usuario'
    user_id = database.Column(database.Integer, primary_key=True, autoincrement=True)
    name = database.Column(database.String(255), nullable=False)
    login = database.Column(database.String(40), nullable=False)
    password = database.Column(database.String(40), nullable=False)
    email = database.Column(database.String(40), nullable=False, unique=True)
    # Define o cadastro como ativo no sistema
    active = database.Column(database.Boolean, default=True)
    # Define o relacionamento com os Hoteis do usuários
    hoteis = database.relationship('HotelModel')

    def __init__(self, name, login, password, email):
        self.name = name
        self.login = login
        self.password = password
        self.email = email
        self.active = True

    def json(self):
        return {
            'user_id': self.user_id,
            'name': self.name,
            'login': self.login,
            'email': self.email,
            'active': self.active
        }

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        database.session.add(self)
        database.session.commit()

    def update_user(self, name, email, login, password):
        self.name = name
        self.email = email
        self.login = login
        self.password = password

    def delete_user(self):
        database.session.delete(self)
        database.session.commit()
