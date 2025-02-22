import os
import multiprocessing
from bitcoinlib.keys import Address, Key
from datetime import datetime

# Obtém a data e hora atual
data_atual = datetime.now()

# Exibe no formato desejado
print(f"Start: {data_atual}")

# Defina aqui o prefixo desejado (exemplo: "leo")
PREFIXO_DESEJADO = "1leo"

# Função que gera endereços e verifica se atendem ao critério
def encontrar_endereco():
    while True:
        # Gerando uma chave aleatória
        chave = Key()
        # Usando script_type "p2pk" ao criar o endereço
        endereco = chave.address(script_type="p2pk")

        print(f"Gerado: {endereco}")  # Exibe para acompanhar a geração

        # Verifica se o endereço começa com o prefixo desejado
        if endereco.startswith(PREFIXO_DESEJADO):
            return chave.wif(), endereco  # Retorna chave privada e endereço correspondente

# Função para rodar em múltiplos processos
def worker(queue):
    wif, address = encontrar_endereco()
    queue.put((wif, address))  # Adiciona o resultado à fila de comunicação entre processos

if __name__ == "__main__":
    num_processos = os.cpu_count()  # Usa o número máximo de núcleos disponíveis
    queue = multiprocessing.Queue()

    # Criando múltiplos processos para buscar endereços em paralelo
    processos = [multiprocessing.Process(target=worker, args=(queue,)) for _ in range(num_processos)]

    for p in processos:
        p.start()

    # Obtendo o primeiro resultado encontrado
    wif, address = queue.get()

    # Matando todos os processos após encontrar o primeiro resultado
    for p in processos:
        p.terminate()

    print(f"Endereço encontrado: {address}")
    print(f"Chave privada (WIF): {wif}")
