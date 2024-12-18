def permutar(bits, permutacao):
    """Aplica uma permutação nos bits fornecidos com base no array de permutação."""
    return [bits[i] for i in permutacao]

def deslocamento_esquerda(bits, deslocamentos):
    """Realiza um deslocamento circular à esquerda em uma lista de bits."""
    return bits[deslocamentos:] + bits[:deslocamentos]

def gerar_subchaves(chave):
    """Gera as subchaves K1 e K2 a partir da chave de 10 bits fornecida."""
    P10 = [2, 5, 7, 6, 3, 9, 0, 8, 1, 4]  # Permutação P10, foi feita um mapeamento do índice para deixar de forma mais clara e para melhor manutenção.
    P8 = [5, 8, 6, 3, 7, 9, 4, 2]  # Permutação P8, foi feita um mapeamento do índice para deixar de forma mais clara e para melhor manutenção.

    # Aplicar a permutação P10
    chave = permutar(chave, P10)

    # Dividir em duas metades e realizar deslocamentos à esquerda
    esquerda, direita = chave[:5], chave[5:]
    esquerda, direita = deslocamento_esquerda(esquerda, 1), deslocamento_esquerda(direita, 1)
    K1 = permutar(esquerda + direita, P8)  # Primeira subchave

    # Realizar deslocamento à esquerda novamente
    esquerda, direita = deslocamento_esquerda(esquerda, 2), deslocamento_esquerda(direita, 2)
    K2 = permutar(esquerda + direita, P8)  # Segunda subchave

    return K1, K2

def aplicar_sbox(bits_entrada, sbox):
    """Aplica a transformação da S-Box a uma entrada de 4 bits."""
    linha = (bits_entrada[0] << 1) | bits_entrada[3]
    coluna = (bits_entrada[1] << 1) | bits_entrada[2]
    return [int(x) for x in f"{sbox[linha][coluna]:02b}"]

def funcao_feistel(direita, subchave):
    """Função Feistel que combina expansão/permutação, S-Boxes e permutação P4."""
    EP = [3, 0, 1, 2, 1, 2, 3, 0]  # Expansão/permutação
    P4 = [1, 3, 2, 0]  # Permutação P4

    # Aplicar expansão/permutação
    expandido = permutar(direita, EP)

    # Realizar XOR com a subchave
    resultado_xor = [bit ^ subchave[i] for i, bit in enumerate(expandido)]

    # Aplicar S-Boxes
    S0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]

    S1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]

    esquerda_sbox = aplicar_sbox(resultado_xor[:4], S0)
    direita_sbox = aplicar_sbox(resultado_xor[4:], S1)

    # Aplicar a permutação P4
    return permutar(esquerda_sbox + direita_sbox, P4)

def sdes_encriptar_decriptar(dados, chave, modo='E'):
    """Realiza a encriptação ou decriptação de um bloco de 8 bits usando S-DES."""
    PERMUT_INI = [1, 5, 2, 0, 3, 7, 4, 6]  # Permutação inicial
    PERMUT_INI_INV = [3, 0, 2, 4, 6, 1, 7, 5]  # Permutação inversa
    
    # Gerar as subchaves
    K1, K2 = gerar_subchaves(chave)

    # Selecionar a ordem das subchaves com base no modo
    if modo == 'D':
        K1, K2 = K2, K1

    # Aplicar a permutação inicial
    dados = permutar(dados, PERMUT_INI)

    # Dividir em duas metades
    esquerda, direita = dados[:4], dados[4:]

    # Rodada 1
    resultado = funcao_feistel(direita, K1)
    esquerda = [esquerda[i] ^ resultado[i] for i in range(4)]

    # Trocar as metades
    esquerda, direita = direita, esquerda

    # Rodada 2
    resultado = funcao_feistel(direita, K2)
    esquerda = [esquerda[i] ^ resultado[i] for i in range(4)]

    # Combinar as metades e aplicar a permutação inversa
    combinado = esquerda + direita
    return permutar(combinado, PERMUT_INI_INV)

def main():
    # Chave de 10 bits e bloco de dados de 8 bits
    chave = [1, 0, 1, 0, 0, 0, 0, 0, 1, 0]  # Chave de 10 bits
    dados = [1, 0, 0, 1, 0, 1, 1, 1]  # Bloco de dados de 8 bits

    # Encriptação
    texto_cifrado = sdes_encriptar_decriptar(dados, chave, modo='E')
    print("Encriptação:", ''.join(map(str, texto_cifrado)))

    # Decriptação
    texto_decifrado = sdes_encriptar_decriptar(texto_cifrado, chave, modo='D')
    print("Decriptação:", ''.join(map(str, texto_decifrado)))

if __name__ == "__main__":
    main()
