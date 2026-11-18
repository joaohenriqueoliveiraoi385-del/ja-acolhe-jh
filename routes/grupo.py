from flask import Blueprint, render_template, request, redirect, url_for, session
from db import db
from model import Grupo, GrupoMembro, MensagemGrupo, Usu, Not

grupo_bp = Blueprint("grupo", __name__, url_prefix="/grupos")


@grupo_bp.route("/")
def listar():
    if 'usuario_id' not in session:
        return redirect(url_for("home"))
    
    usuario_id = session['usuario_id']
    grupos = Grupo.query.order_by(Grupo.data_criacao.desc()).all()
    
    participacoes = {
        m.grupo_id: m.status 
        for m in GrupoMembro.query.filter_by(usu_id=usuario_id).all()
    }
    
    return render_template("grupos.html", grupos=grupos, participacoes=participacoes, usuario_id=usuario_id)


@grupo_bp.route("/criar", methods=["POST"])
def criar():
    if 'usuario_id' not in session:
        return redirect(url_for("home"))
    
    nome = request.form.get("nome_grupo")
    descricao = request.form.get("descricao_grupo")
    tipo = request.form.get("tipo")
    usuario_id = session['usuario_id']
    
    if nome and descricao and tipo:
        novo_grupo = Grupo(
            nome_grupo=nome,
            descricao_grupo=descricao,
            tipo=tipo,
            criador_id=usuario_id
        )
        db.session.add(novo_grupo)
        db.session.commit()
        
        membro_criador = GrupoMembro(
            grupo_id=novo_grupo.id_grupo,
            usu_id=usuario_id,
            status='aprovado'
        )
        db.session.add(membro_criador)
        db.session.commit()
        
    return redirect(url_for("grupo.listar"))


@grupo_bp.route("/entrar/<int:grupo_id>", methods=["POST"])
def entrar(grupo_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home"))
    
    usuario_id = session['usuario_id']
    grupo = Grupo.query.get_or_404(grupo_id)
    
    membro_existente = GrupoMembro.query.filter_by(grupo_id=grupo_id, usu_id=usuario_id).first()
    
    if not membro_existente:
        status_inicial = 'aprovado' if grupo.tipo == 'aberto' else 'pendente'
        
        novo_membro = GrupoMembro(
            grupo_id=grupo_id,
            usu_id=usuario_id,
            status=status_inicial
        )
        db.session.add(novo_membro)

        if grupo.tipo == 'fechado' and grupo.criador_id != usuario_id:
            nome_solicitante = session.get('usuario_nome', 'Alguém')
            nova_not = Not(
                titulo_not="Solicitação de grupo 🔒",
                mensagem_not=f"{nome_solicitante} pediu para entrar no seu grupo '{grupo.nome_grupo}'.",
                link=url_for("grupo.chat", grupo_id=grupo.id_grupo),
                usu_id=grupo.criador_id
            )
            db.session.add(nova_not)

        db.session.commit()
        
    return redirect(url_for("grupo.listar"))


@grupo_bp.route("/chat/<int:grupo_id>")
def chat(grupo_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home"))
    
    usuario_id = session['usuario_id']
    grupo = Grupo.query.get_or_404(grupo_id)
    
    membro = GrupoMembro.query.filter_by(grupo_id=grupo_id, usu_id=usuario_id, status='aprovado').first()
    if not membro and grupo.criador_id != usuario_id:
        return redirect(url_for("grupo.listar"))
        
    mensagens = MensagemGrupo.query.filter_by(grupo_id=grupo_id).order_by(MensagemGrupo.data_envio.asc()).all()
    membros_pendentes = GrupoMembro.query.filter_by(grupo_id=grupo_id, status='pendente').all() if grupo.criador_id == usuario_id else []
    
    return render_template("detalhe_grupo.html", grupo=grupo, mensagens=mensagens, membros_pendentes=membros_pendentes, usuario_id=usuario_id)


@grupo_bp.route("/chat/<int:grupo_id>/enviar", methods=["POST"])
def enviar_mensagem(grupo_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home"))
        
    texto = request.form.get("texto")
    usuario_id = session['usuario_id']
    
    grupo = Grupo.query.get_or_404(grupo_id)
    membro = GrupoMembro.query.filter_by(grupo_id=grupo_id, usu_id=usuario_id, status='aprovado').first()
    
    if texto and texto.strip() and (membro or grupo.criador_id == usuario_id):
        nova_msg = MensagemGrupo(
            texto=texto.strip(),
            grupo_id=grupo_id,
            usu_id=usuario_id
        )
        db.session.add(nova_msg)
        db.session.commit()
        
    return redirect(url_for("grupo.chat", grupo_id=grupo_id))


@grupo_bp.route("/aprovar/<int:grupo_id>/<int:membro_id>", methods=["POST"])
def aprovar_membro(grupo_id, membro_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home"))
        
    grupo = Grupo.query.get_or_404(grupo_id)
    
    if grupo.criador_id == session['usuario_id']:
        membro = GrupoMembro.query.get_or_404(membro_id)
        if membro.grupo_id == grupo_id:
            membro.status = 'aprovado'

            nova_not = Not(
                titulo_not="Entrada aprovada! 🎉",
                mensagem_not=f"Você foi aceito no grupo '{grupo.nome_grupo}'. Já pode participar do chat!",
                link=url_for("grupo.chat", grupo_id=grupo.id_grupo),
                usu_id=membro.usu_id
            )
            db.session.add(nova_not)
            db.session.commit()
            
    return redirect(url_for("grupo.chat", grupo_id=grupo_id))