# dados/

Esta pasta existe para seguir o padrão da disciplina, mas o projeto **não
usa um arquivo de dados estático** — os dados são baixados em tempo real
do dataset público [mledoze/countries](https://github.com/mledoze/countries),
hospedado no GitHub, na primeira execução do app.

Após a primeira execução, os dados ficam salvos em cache local em
`src/paises_cache.json` (não versionado no Git, veja `.gitignore`), para
evitar downloads repetidos.

Fonte dos dados: https://raw.githubusercontent.com/mledoze/countries/master/dist/countries.json