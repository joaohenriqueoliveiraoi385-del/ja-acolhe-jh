from db import db


class Usu(db.Model):
    __tablename__ = 'usuarios'

    id_usu = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(40), nullable=False)
    gmail = db.Column(db.String(60), nullable=False, unique=True)
    senha = db.Column(db.String(100), nullable=False)

    curtidas = db.relationship('Curt', backref='usuario', lazy=True)
    comentarios = db.relationship('Coment', backref='usuario', lazy=True)
    publicacoes = db.relationship('Publi', backref='usuario', lazy=True)
    diarios = db.relationship('Diar', backref='usuario', lazy=True)
    notificacoes = db.relationship('Not', backref='usuario', lazy=True)


class Publi(db.Model):
    __tablename__ = 'publicacoes'

    id_publi = db.Column(db.Integer, primary_key=True)
    titulo_publi = db.Column(db.String(150), nullable=False)
    texto_publi = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), default='ativo')
    data_publi = db.Column(db.DateTime, default=db.func.now())

    usu_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usu'),
        nullable=False
    )

    curtidas = db.relationship('Curt', backref='publicacao', lazy=True)
    comentarios = db.relationship('Coment', backref='publicacao', lazy=True)


class Curt(db.Model):
    __tablename__ = 'curtidas'

    id_curt = db.Column(db.Integer, primary_key=True)
    data_curtida = db.Column(db.DateTime, default=db.func.now())

    usu_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usu'),
        nullable=False
    )

    id_publicacao = db.Column(
        db.Integer,
        db.ForeignKey('publicacoes.id_publi'),
        nullable=False
    )


class Coment(db.Model):
    __tablename__ = 'comentarios'

    id_coment = db.Column(db.Integer, primary_key=True)
    texto_coment = db.Column(db.String(300), nullable=False)
    data_coment = db.Column(db.DateTime, default=db.func.now())

    usu_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usu'),
        nullable=False
    )

    id_publicacao = db.Column(
        db.Integer,
        db.ForeignKey('publicacoes.id_publi'),
        nullable=False
    )


class Diar(db.Model):
    __tablename__ = 'diarios'

    id_diar = db.Column(db.Integer, primary_key=True)
    humor = db.Column(db.String(40), nullable=False)
    texto_diar = db.Column(db.String(700), nullable=False)
    data_registro = db.Column(db.DateTime, default=db.func.now())

    usu_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usu'),
        nullable=False
    )


class Int(db.Model):
    __tablename__ = 'interesses'

    id_int = db.Column(db.Integer, primary_key=True)
    nome_interesse = db.Column(db.String(100), nullable=False)
    descricao_int = db.Column(db.String(255), nullable=True)


class Not(db.Model):
    __tablename__ = 'notificacoes'

    id_not = db.Column(db.Integer, primary_key=True)
    titulo_not = db.Column(db.String(200), nullable=False)
    mensagem_not = db.Column(db.String(300), nullable=False)
    lida = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(200), nullable=True)
    data_not = db.Column(db.DateTime, default=db.func.now())

    usu_id = db.Column(
        db.Integer,
        db.ForeignKey('usuarios.id_usu'),
        nullable=False
    )


class Rec(db.Model):
    __tablename__ = 'recursos'

    id_rec = db.Column(db.Integer, primary_key=True)
    titulo_rec = db.Column(db.String(250), nullable=False)
    descricao_rec = db.Column(db.String(500), nullable=False)
    tipo = db.Column(db.String(75), nullable=False)


class Grupo(db.Model):
    __tablename__ = 'grupos'

    id_grupo = db.Column(db.Integer, primary_key=True)
    nome_grupo = db.Column(db.String(100), nullable=False)
    descricao_grupo = db.Column(db.String(300), nullable=False)
    tipo = db.Column(db.String(20), default='aberto')
    criador_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usu'), nullable=False)
    data_criacao = db.Column(db.DateTime, default=db.func.now())

    criador = db.relationship('Usu', backref='grupos_criados')
    membros = db.relationship('GrupoMembro', backref='grupo', cascade="all, delete-orphan", lazy=True)
    mensagens = db.relationship('MensagemGrupo', backref='grupo', cascade="all, delete-orphan", lazy=True)


class GrupoMembro(db.Model):
    __tablename__ = 'grupo_membros'

    id_membro = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    usu_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usu'), nullable=False)
    status = db.Column(db.String(20), default='aprovado')

    usuario = db.relationship('Usu', backref='participacoes_grupos')


class MensagemGrupo(db.Model):
    __tablename__ = 'grupo_mensagens'

    id_msg = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(500), nullable=False)
    data_envio = db.Column(db.DateTime, default=db.func.now())
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id_grupo'), nullable=False)
    usu_id = db.Column(db.Integer, db.ForeignKey('usuarios.id_usu'), nullable=False)

    usuario = db.relationship('Usu', backref='mensagens_grupo')