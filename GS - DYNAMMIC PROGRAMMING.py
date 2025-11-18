from typing import List, Tuple

Projeto = Tuple[str, int, int]  #nome, valor, horas

#1 — Estratégia Gulosa

def estrategia_gulosa(lista_projetos: List[Projeto], capacidade: int) -> Tuple[int, List[int]]:
    projetos_ordenados = []
    for indice, projeto in enumerate(lista_projetos):
        nome, valor, horas = projeto
        razao = valor / horas if horas > 0 else float('inf')
        projetos_ordenados.append((indice, nome, valor, horas, razao))

    projetos_ordenados.sort(key=lambda x: x[4], reverse=True)

    escolhidos = []
    capacidade_restante = capacidade
    valor_total = 0

    for indice, nome, valor, horas, _ in projetos_ordenados:
        if horas <= capacidade_restante:
            escolhidos.append(indice)
            capacidade_restante -= horas
            valor_total += valor

    return valor_total, escolhidos

#2 — Solução Recursiva Pura

def solucao_recursiva(lista_projetos: List[Projeto], capacidade: int) -> Tuple[int, List[int]]:
    n = len(lista_projetos)

    def rec(i: int, cap: int) -> Tuple[int, List[int]]:
        if i < 0 or cap <= 0:
            return 0, []

        nome, valor, horas = lista_projetos[i]

        valor_sem, lista_sem = rec(i - 1, cap)

        if horas > cap:
            return valor_sem, lista_sem

        valor_com, lista_com = rec(i - 1, cap - horas)
        valor_com += valor

        if valor_com > valor_sem:
            return valor_com, lista_com + [i]
        else:
            return valor_sem, lista_sem

    valor_final, lista_final = rec(n - 1, capacidade)
    lista_final.sort()
    return valor_final, lista_final

#3 — Memoização (Top-Down)

def solucao_memoizada(lista_projetos: List[Projeto], capacidade: int) -> Tuple[int, List[int]]:
    from functools import lru_cache

    n = len(lista_projetos)

    @lru_cache(maxsize=None)
    def rec(i: int, cap: int) -> Tuple[int, Tuple[int, ...]]:
        if i < 0 or cap <= 0:
            return 0, ()

        nome, valor, horas = lista_projetos[i]

        valor_sem, lista_sem = rec(i - 1, cap)

        if horas > cap:
            return valor_sem, lista_sem

        valor_com, lista_com = rec(i - 1, cap - horas)
        valor_com += valor

        if valor_com > valor_sem:
            return valor_com, lista_com + (i,)
        else:
            return valor_sem, lista_sem

    valor_final, tupla_final = rec(n - 1, capacidade)
    lista_final = list(tupla_final)
    lista_final.sort()
    return valor_final, lista_final

#4 — Programação Dinâmica Iterativa (Bottom-Up)
def solucao_iterativa(lista_projetos: List[Projeto], capacidade: int) -> Tuple[int, List[int]]:
    n = len(lista_projetos)
    tabela = [[0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        nome, valor, horas = lista_projetos[i - 1]
        for cap in range(capacidade + 1):
            valor_sem = tabela[i - 1][cap]
            valor_com = -1
            if horas <= cap:
                valor_com = valor + tabela[i - 1][cap - horas]
            tabela[i][cap] = max(valor_sem, valor_com)

    escolhidos = []
    cap = capacidade

    for i in range(n, 0, -1):
        if tabela[i][cap] != tabela[i - 1][cap]:
            escolhidos.append(i - 1)
            _, valor, horas = lista_projetos[i - 1]
            cap -= horas

    escolhidos.sort()
    return tabela[n][capacidade], escolhidos

#EXECUÇÃO
if __name__ == "__main__":
    projetos_exemplo = [
        ("Projeto A", 12, 4),
        ("Projeto B", 10, 3),
        ("Projeto C", 7, 2),
        ("Projeto D", 4, 3),
    ]

    capacidade_exemplo = 10

    print("GREEDY:")
    print(estrategia_gulosa(projetos_exemplo, capacidade_exemplo))

    print("\nRECURSIVO PURO:")
    print(solucao_recursiva(projetos_exemplo, capacidade_exemplo))

    print("\nMEMOIZAÇÃO:")
    print(solucao_memoizada(projetos_exemplo, capacidade_exemplo))

    print("\nBOTTOM-UP:")
    print(solucao_iterativa(projetos_exemplo, capacidade_exemplo))