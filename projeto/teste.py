def testar_abrir_lista():
    #falta as especificações
    listas_exemplo = [
        {
            "titulo": "Lista de Álgebra Linear",
            "exercicios": ["Ex. 1: Matrizes", "Ex. 2: Determinantes"]
        },
        {
            "titulo": "Lista de Cálculo I",
            "exercicios": ["Ex. 1: Derivadas", "Ex. 2: Limites"]
        },
        {
            "titulo": "Lista de Física",
            "exercicios": ["Ex. 1: Leis de Newton", "Ex. 2: Energia Cinética"]
        }
    ]

    with open('listas.json', 'w', encoding='utf-8') as arquivo:
        json.dump(listas_exemplo, arquivo, indent=4, ensure_ascii=False)

    resultado = abrir_lista()

    print("\nResultado da execução:")
    print(f"Sucesso: {resultado['sucesso']}")
    print(f"Mensagem: {resultado['mensagem']}")

    os.remove('listas.json')  


   