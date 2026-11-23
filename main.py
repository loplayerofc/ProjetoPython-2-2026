"""
Projeto Integrador Python - Análise e Desenvolvimento de Sistemas (ADS)
Arquivo: main.py

Integrantes:
- Gilmar Vitor Soares de Oliveira - Matrícula: 2025.15.1436
- Josué Teixeira Ferreira Filho - Matrícula: 2026.15.178

Descrição:
Ponto de entrada do sistema contendo o Menu Interativo via terminal (CLI).
Construído com laço contínuo (while True) e tratamento de exceções (try/except)
para que o programa nunca trave quando o usuário digitar letras ou opções inválidas.
"""

import sys
from src.analisador import AnalisadorDeDados


def exibir_menu():
    """Exibe na tela o menu principal de opções numeradas."""
    print("=" * 66)
    print("   SISTEMA DE ANÁLISE DE VENDAS - PROJETO INTEGRADOR ADS")
    print("=" * 66)
    print(" [1]  Verificar limpeza técnica dos dados (Auditoria)")
    print(" [2]  Resumo geral de vendas (Faturamento, Lucro e Médias)")
    print(" [3]  Agrupar vendas por Categoria (.groupby)")
    print(" [4]  Agrupar vendas por Região (.groupby)")
    print(" [5]  Estatísticas descritivas dos dados (.describe)")
    print(" [6]  Top 10 produtos mais vendidos (.sort_values)")
    print(" [7]  Filtrar vendas por uma categoria específica")
    print(" [8]  Gerar Gráfico 1: Linha (Evolução Temporal das Vendas)")
    print(" [9]  Gerar Gráfico 2: Barras (Vendas por Categoria)")
    print(" [10] Gerar Gráfico 3: Histograma (Distribuição dos Valores)")
    print(" [11] Gerar Gráfico 4: Dispersão (Vendas vs. Lucro)")
    print(" [12] Gerar Todos os Gráficos de uma vez")
    print(" [0]  Sair do Sistema")
    print("=" * 66)


def pausar():
    """Pausa a tela para o usuário ler o resultado antes de voltar ao menu."""
    try:
        input("\nPressione [ENTER] para voltar ao menu...")
    except (KeyboardInterrupt, EOFError):
        pass


def main():
    # Inicializa o motor de dados usando a classe AnalisadorDeDados criada no src/
    try:
        analisador = AnalisadorDeDados('data/superstore_sales.csv')
    except Exception as erro:
        print(f"[ERRO CRÍTICO] Falha ao carregar base de dados: {erro}")
        sys.exit(1)

    # Requisito 1: Menu à prova de falhas com while True e try/except
    while True:
        exibir_menu()

        try:
            opcao_texto = input("Escolha uma opção (0 a 12): ").strip()
            opcao = int(opcao_texto)
        except ValueError:
            # Tratamento de erro obrigatório: impede travamento caso o usuário digite texto
            print("\n" + "!" * 60)
            print(" [ERRO DE DIGITAÇÃO] Você digitou uma letra ou caractere!")
            print(" Por favor, digite apenas números inteiros entre 0 e 12.")
            print("!" * 60)
            pausar()
            continue
        except (KeyboardInterrupt, EOFError):
            print("\n\nEncerrando o sistema com segurança. Até logo!")
            break

        # Opção de encerramento
        if opcao == 0:
            print("\n" + "=" * 50)
            print("  Programa finalizado com sucesso!")
            print("  Obrigado por utilizar o sistema de ADS.")
            print("=" * 50 + "\n")
            break

        elif opcao == 1:
            print("\n--- STATUS DA LIMPEZA DOS DADOS ---")
            info = analisador.relatorio_limpeza()
            print(f" Arquivo analisado      : {info['arquivo']}")
            print(f" Total de linhas brutas : {info['brutos']}")
            print(f" Duplicatas descartadas : {info['duplicatas']}")
            print(f" Linhas com nulos limpas: {info['nulos']}")
            print(f" Linhas finais tratadas : {info['limpos']}")
            print(f" Colunas disponíveis    : {info['colunas']}")
            print(f" Período analisado      : {info['data_inicial']} até {info['data_final']}")
            pausar()

        elif opcao == 2:
            print("\n--- RESUMO GERAL DO NEGÓCIO ---")
            kpis = analisador.calcular_resumo_geral()
            print(f" Faturamento Total : R$ {kpis['faturamento']:,.2f}")
            print(f" Lucro Total       : R$ {kpis['lucro']:,.2f}")
            print(f" Margem de Lucro   : {kpis['margem_percentual']:.2f}%")
            print(f" Ticket Médio      : R$ {kpis['ticket_medio']:,.2f}")
            print(f" Total de Peças    : {kpis['quantidade_itens']:,} unidades")
            print(f" Total de Pedidos  : {kpis['total_pedidos']:,}")
            print(f" Clientes Únicos   : {kpis['total_clientes']:,}")
            pausar()

        elif opcao == 3:
            print("\n--- VENDAS E LUCRO POR CATEGORIA (.GROUPBY) ---")
            print(analisador.vendas_por_categoria())
            pausar()

        elif opcao == 4:
            print("\n--- VENDAS E LUCRO POR REGIÃO (.GROUPBY) ---")
            print(analisador.vendas_por_regiao())
            pausar()

        elif opcao == 5:
            print("\n--- RESUMO ESTATÍSTICO DESCRITIVO (.DESCRIBE) ---")
            print(analisador.estatisticas_descritivas())
            pausar()

        elif opcao == 6:
            print("\n--- TOP 10 PRODUTOS COM MAIOR FATURAMENTO ---")
            top10 = analisador.top_produtos(10)
            print(top10[['Product_Name', 'Category', 'Sales', 'Profit']])
            pausar()

        elif opcao == 7:
            print("\n--- FILTRAR POR CATEGORIA ---")
            categorias_disponiveis = analisador.df['Category'].unique()
            print("Categorias disponíveis:", ", ".join(categorias_disponiveis))
            nome_cat = input("Digite o nome da categoria que deseja filtrar: ").strip()
            df_filtro = analisador.filtrar_categoria(nome_cat)
            if len(df_filtro) == 0:
                print(f"[AVISO] Não foi encontrado nenhum pedido para a categoria '{nome_cat}'.")
            else:
                soma_fat = df_filtro['Sales'].sum()
                soma_luc = df_filtro['Profit'].sum()
                print(f"\n[ENCONTRADO] {len(df_filtro)} pedidos encontrados para '{nome_cat}':")
                print(f" -> Faturamento Total: R$ {soma_fat:,.2f}")
                print(f" -> Lucro Total      : R$ {soma_luc:,.2f}")
            pausar()

        elif opcao == 8:
            print("\nGerando Gráfico 1 (Linha - Evolução Temporal)...")
            analisador.grafico_linha_evolucao()
            pausar()

        elif opcao == 9:
            print("\nGerando Gráfico 2 (Barras - Categorias)...")
            analisador.grafico_barras_categoria()
            pausar()

        elif opcao == 10:
            print("\nGerando Gráfico 3 (Histograma - Distribuição)...")
            analisador.grafico_histograma_vendas()
            pausar()

        elif opcao == 11:
            print("\nGerando Gráfico 4 (Dispersão - Vendas x Lucro)...")
            analisador.grafico_dispersao_vendas_lucro()
            pausar()

        elif opcao == 12:
            analisador.gerar_todos_graficos()
            pausar()

        else:
            print(f"\n[OPÇÃO INVÁLIDA] O número {opcao} não existe no menu.")
            print("Por favor, digite um número entre 0 e 12.")
            pausar()


if __name__ == '__main__':
    main()
