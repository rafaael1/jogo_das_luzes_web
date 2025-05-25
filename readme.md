# Jogo das Luzes - Web Version

O objetivo do Jogo das Luzes é ACENDER todas as luzes do tabuleiro com o menor número de jogadas possíveis. Esta é uma versão web do clássico jogo (lights out).

- **Luz APAGADA:** ${\normalsize{\textbf{\color{red}VERMELHO}}}$
- **Luz ACESA:** ${\normalsize{\textbf{\color{yellow}AMARELO}}}$ (com fundo escuro para visualização)

## Como Jogar

O jogo é disputado em um tabuleiro de 5 x 5 luzes. Inicialmente, todas as luzes começam apagadas (vermelhas).

1.  **Selecionar uma Luz:** Clique em qualquer luz no tabuleiro.
2.  **Efeito do Clique:** Clicar em uma luz alterna o estado dela (de acesa para apagada, ou de apagada para acesa) E também alterna o estado das luzes adjacentes diretas (Norte, Sul, Leste e Oeste).
3.  **Objetivo:** Deixar todas as luzes do tabuleiro acesas (amarelas).
4.  **Contador de Jogadas:** O número de jogadas é contado. Tente vencer com o mínimo de cliques!

## Interface do Jogo

O jogo agora é jogado inteiramente no seu navegador web e possui duas telas principais:

*   **Página do Jogo (`/`):**
    *   Mostra o tabuleiro 5x5 interativo.
    *   Exibe o contador de jogadas atual.
    *   Contém um botão "Reset Game" para reiniciar o tabuleiro para o estado inicial.
    *   Inclui um link "View Rankings" para acessar a página de pontuações.

*   **Página de Rankings (`/ranking`):**
    *   Mostra uma tabela com as melhores pontuações (top 10).
    *   Cada entrada no ranking exibe o nome do jogador, o número de jogadas e a data em que a pontuação foi alcançada.
    *   Permite voltar para a página do jogo.

## Executando a Aplicação Localmente

Para rodar o Jogo das Luzes no seu computador:

1.  **Pré-requisitos:**
    *   Python 3.x instalado.
    *   Flask instalado. Se não tiver, instale com o comando:
        ```bash
        pip install Flask
        ```

2.  **Navegue até o diretório raiz do projeto** (o diretório que contém a pasta `web_app` e este `readme.md`).

3.  **Execute o servidor Flask:**
    Abra um terminal ou prompt de comando no diretório raiz e execute:
    ```bash
    python -m web_app.app
    ```
    Este comando inicia o servidor de desenvolvimento do Flask.

4.  **Acesse o Jogo:**
    Abra seu navegador web e vá para o seguinte endereço:
    [http://localhost:8080](http://localhost:8080) ou [http://0.0.0.0:8080](http://0.0.0.0:8080)

## Sistema de Ranking

Ao vencer o jogo (deixar todas as luzes acesas), você será solicitado a inserir seu nome. Sua pontuação (nome e número de jogadas) será salva e exibida na página de rankings se estiver entre as melhores.

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Authors

- [@rafaael1](https://github.com/rafaael1) (versão original em console - [Jogo das Luzes](https://github.com/rafaael1/jogo_das_luzes) )

Adaptado para versão web como parte de um projeto.

## Contributing

Contributions are always welcome! Se tiver sugestões ou melhorias, sinta-se à vontade para contribuir.
