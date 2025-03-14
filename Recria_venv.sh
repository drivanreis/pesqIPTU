# /Recria_venv.sh
#!/bin/bash

# Checar se o VSCode está aberto
if pgrep -x "code" > /dev/null; then
    echo "Feche o VSCode antes de executar este script."
    exit 1
fi

# Sair e desativar ambiente virtual, se estiver ativo
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Desativando o ambiente virtual..."
    deactivate
fi

# Remover o ambiente virtual existente
echo "Removendo o ambiente virtual existente..."
rm -rf .venv
find . -type d \( -name "venv" -o -name ".venv" \) -exec rm -rf {} +

# Remover diretórios "__pycache__"
echo "Removendo diretórios '__pycache__'..."
find . -name "__pycache__" -type d -exec rm -rf {} +

# Criar novo ambiente virtual
echo "Criando novo ambiente virtual..."
python3 -m venv .venv

# Ativar o novo ambiente virtual
echo "Ativando o ambiente virtual..."
source .venv/bin/activate

# Instalar as dependências
echo "Instalando dependências..."
pip install -r requirements.txt

# Abrir o VSCode
echo "Abrindo o VSCode..."
code .

echo "Ambiente virtual recriado com sucesso.
Execute 'python -m main' ou 'python3 main.py'
manualmente no terminal do VSCode."