
import os

# Caminho para a pasta com os arquivos
folder_path = "./assets/gif"

# Listar os arquivos no diretório
files = sorted(os.listdir(folder_path))

# Renomear os arquivos
for index, filename in enumerate(files, start=1):
    # Construir o novo nome
    new_name = f"frame_{index}{os.path.splitext(filename)[1]}"
    
    # Caminho completo para o arquivo antigo e o novo nome
    old_file = os.path.join(folder_path, filename)
    new_file = os.path.join(folder_path, new_name)
    
    # Renomear o arquivo
    os.rename(old_file, new_file)

print("Arquivos renomeados com sucesso!")
