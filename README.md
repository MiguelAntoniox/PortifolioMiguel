# PortifolioMiguel

Sistema web em Flask com visual minimalista futurista para exibir automaticamente os projetos públicos do GitHub.

## Destaques

- Integração em tempo real com o perfil `MiguelAntoniox`
- Layout com estética preta e roxa
- Cards de projetos com linguagem, stars, forks e links
- Fallback local caso a API do GitHub fique indisponível

## Como executar

1. Instale as dependências:

	`pip install -r requirements.txt`

2. Inicie a aplicação:

	`python app.py`

3. Abra no navegador:

	`http://127.0.0.1:5000`

## Configuração opcional

Você pode trocar o usuário do GitHub definindo a variável de ambiente `GITHUB_USERNAME`.
