from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    Boolean,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import json
import os

# Cria a pasta data se não existir
os.makedirs("data", exist_ok=True)

# Banco de dados SQLite
DATABASE_URL = "sqlite:///data/mapas.db"

# Cria o engine
engine = create_engine(DATABASE_URL, echo=False)

# Cria a base
Base = declarative_base()

# Cria a sessão
SessionLocal = sessionmaker(bind=engine)

# ============================================
# MODELOS (TABELAS)
# ============================================


class Mapa(Base):
    __tablename__ = "mapas"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(500), nullable=False)
    data_mapeamento = Column(DateTime, default=datetime.now)
    total_elementos = Column(Integer, default=0)
    versao = Column(String(50), default="1.0")
    descricao = Column(String(200), nullable=True)

    # Relacionamento com elementos
    elementos = relationship(
        "Elemento", back_populates="mapa", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "url": self.url,
            "data_mapeamento": self.data_mapeamento.strftime("%Y-%m-%d %H:%M:%S"),
            "total_elementos": self.total_elementos,
            "versao": self.versao,
            "descricao": self.descricao,
            "elementos": [elem.to_dict() for elem in self.elementos],
        }


class Elemento(Base):
    __tablename__ = "elementos"

    id = Column(Integer, primary_key=True, index=True)
    mapa_id = Column(Integer, ForeignKey("mapas.id"), nullable=False)

    posicao = Column(Integer)
    profundidade = Column(Integer)
    tag = Column(String(50))
    classe = Column(String(200))
    elemento_id = Column(String(100))
    link = Column(String(500))
    texto = Column(Text)
    pai = Column(String(50))
    seletor_css = Column(String(500))
    xpath = Column(String(500))

    estavel = Column(Boolean, default=True)
    ultima_alteracao = Column(DateTime, nullable=True)

    mapa = relationship("Mapa", back_populates="elementos")

    def to_dict(self):
        return {
            "posicao": self.posicao,
            "profundidade": self.profundidade,
            "tag": self.tag,
            "classe": self.classe,
            "id": self.elemento_id,
            "link": self.link,
            "texto": self.texto,
            "pai": self.pai,
            "seletor_css": self.seletor_css,
            "xpath": self.xpath,
            "estavel": self.estavel,
        }


# ============================================
# FUNÇÕES DE CRIAÇÃO E ACESSO
# ============================================


def criar_tabelas():
    """Cria todas as tabelas no banco de dados"""
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas criadas com sucesso!")


def salvar_mapa(dados, url, descricao=None):
    """Salva um mapa completo no banco de dados"""
    session = SessionLocal()

    try:
        # Cria o mapa
        mapa = Mapa(
            url=url,
            total_elementos=len(dados),
            descricao=descricao
            or f"Mapa gerado em {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        )
        session.add(mapa)
        session.flush()

        # Cria os elementos
        for elem in dados:
            elemento = Elemento(
                mapa_id=mapa.id,
                posicao=elem.get("posicao"),
                profundidade=elem.get("profundidade"),
                tag=elem.get("tag"),
                classe=elem.get("classe"),
                elemento_id=elem.get("id"),
                link=elem.get("link"),
                texto=elem.get("texto"),
                pai=elem.get("pai"),
                seletor_css=elem.get("seletor_css"),
                xpath=elem.get("xpath"),
                estavel=True,
            )
            session.add(elemento)

        session.commit()
        print(
            f"✅ Mapa salvo com sucesso! ID: {mapa.id} - {mapa.total_elementos} elementos"
        )
        return mapa

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao salvar mapa: {e}")
        return None
    finally:
        session.close()


def buscar_ultimo_mapa(url):
    """Busca o último mapa salvo para uma URL"""
    session = SessionLocal()
    try:
        mapa = (
            session.query(Mapa)
            .filter(Mapa.url == url)
            .order_by(Mapa.data_mapeamento.desc())
            .first()
        )
        return mapa
    except Exception as e:
        print(f"❌ Erro ao buscar mapa: {e}")
        return None
    finally:
        session.close()


def listar_mapas(url=None, limite=10):
    """Lista os mapas salvos"""
    session = SessionLocal()
    try:
        query = session.query(Mapa)
        if url:
            query = query.filter(Mapa.url == url)
        mapas = query.order_by(Mapa.data_mapeamento.desc()).limit(limite).all()
        return [m.to_dict() for m in mapas]
    except Exception as e:
        print(f"❌ Erro ao listar mapas: {e}")
        return []
    finally:
        session.close()


def contar_mapas():
    """Conta quantos mapas estão salvos"""
    session = SessionLocal()
    try:
        total = session.query(Mapa).count()
        return total
    except Exception as e:
        print(f"❌ Erro ao contar mapas: {e}")
        return 0
    finally:
        session.close()


def comparar_mapas(mapa_atual, mapa_anterior):
    """Compara dois mapas e retorna as diferenças"""
    if not mapa_anterior:
        return {"status": "primeiro_mapa", "mensagem": "Este é o primeiro mapa salvo."}

    elementos_antigos = {e.posicao: e for e in mapa_anterior.elementos}
    elementos_novos = {e.get("posicao"): e for e in mapa_atual}

    mudancas = {"iguais": [], "mudaram": [], "sumiram": [], "novos": []}

    for pos, elem in elementos_novos.items():
        if pos in elementos_antigos:
            antigo = elementos_antigos[pos]
            mudou = False
            campos_mudaram = []

            if antigo.seletor_css != elem.get("seletor_css"):
                mudou = True
                campos_mudaram.append("seletor_css")
            if antigo.xpath != elem.get("xpath"):
                mudou = True
                campos_mudaram.append("xpath")
            if antigo.texto != elem.get("texto"):
                mudou = True
                campos_mudaram.append("texto")

            if mudou:
                mudancas["mudaram"].append(
                    {
                        "posicao": pos,
                        "tag": elem.get("tag"),
                        "campos": campos_mudaram,
                        "antigo": {
                            "seletor_css": antigo.seletor_css,
                            "xpath": antigo.xpath,
                            "texto": antigo.texto,
                        },
                        "novo": {
                            "seletor_css": elem.get("seletor_css"),
                            "xpath": elem.get("xpath"),
                            "texto": elem.get("texto"),
                        },
                    }
                )
            else:
                mudancas["iguais"].append(pos)
        else:
            mudancas["novos"].append(elem)

    for pos, elem in elementos_antigos.items():
        if pos not in elementos_novos:
            mudancas["sumiram"].append(elem.posicao)

    return mudancas


def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def contar_mapas_por_url(url):

    session = SessionLocal()
    try:
        total = session.query(Mapa).filter(Mapa.url == url).count()
        return total
    except Exception as e:
        print(f"❌ Erro ao contar mapas: {e}")
        return 0
    finally:
        session.close()
