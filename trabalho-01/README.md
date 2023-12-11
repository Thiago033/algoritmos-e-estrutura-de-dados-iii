# Solucionador de TSP

## Visão Geral

Este projeto em Python oferece dois algoritmos para resolver o Problema do Caixeiro Viajante (TSP): um aproximado e um exato.

- `python aproximativo.py`: Executa o algoritmo aproximado.
- `python exato.py`: Executa o algoritmo exato.

## Uso

1. Execute o algoritmo desejado executando um dos seguintes comandos no seu terminal:

    ```bash
    python aproximativo.py
    ```
    ou
    ```bash
    python exato.py
    ```

2. Após executar o comando, o programa solicitará que você escolha uma instância específica do problema TSP. Insira um número entre 1 e 5 para selecionar o problema desejado.

3. Os resultados do algoritmo serão salvos em duas pastas:

    - `approximate_results`: Contém os resultados do algoritmo aproximado.
    - `exact_results`: Contém os resultados do algoritmo exato.

4. Estrutura de Pastas
algoritmos/
│   approximate_results/
│   │   resultado_problema1.txt
│   │   resultado_problema2.txt
│   │   ...
│
│   exact_results/
│   │   resultado_problema1.txt
│   │   resultado_problema2.txt
│   │   ...