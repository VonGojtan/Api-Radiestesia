from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session 
from database import engine, SessionLocal, Base
import models
from passlib.context import CryptContext

app = FastAPI()

#Criar as tabelas automaticamente no banco
Base.metadata.create_all(bind=engine)

# Configuração da criptografia de senha
pwd_context = CryptContext(schemes=["bcrypt"],deprecated= "auto")

#Conexão com o Banco 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
# Função de senha
def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

# Rota inicial 
@app.get("/")
def home():
    return{"msg":"API Online"}

# Cadastro de usuário
@app.post("/cadastro")
def cadastrar_usuario(email:str, senha:str, db:Session=Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()
    if usuario:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    novo_usuario = models.Usuario(
        email = email,
        senha = hash_senha(senha)
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return{"msg": "Usuário cadastrado com Sucesso"}

# Login
@app.post("/login")
def login (email: str, senha: str, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.email == email).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if not verificar_senha(senha,usuario.senha):
        raise HTTPException(status_code=401, detail="Senha incorreta")
    return {"msg":"Login realizado com sucesso"}