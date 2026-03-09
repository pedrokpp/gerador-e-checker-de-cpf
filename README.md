# Gerador e Validador de CPF e CNPJ

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma biblioteca Python moderna para validar e gerar CPFs e CNPJs brasileiros de acordo com os algoritmos oficiais.

## Características

- ✅ **Validação correta**: Usa algoritmos módulo 11 oficiais
- ✅ **Geração eficiente**: Gera documentos válidos de forma determinística  
- ✅ **CPF com regiões**: Valida e gera CPFs por estado/região
- ✅ **CNPJ com filiais**: Gera matrizes (0001) ou filiais aleatórias
- ✅ **Formatação flexível**: Aceita entrada formatada ou não
- ✅ **Type hints completos**: Totalmente tipado para melhor IDE support
- ✅ **98% de cobertura**: 209 testes unitários e de integração
- ✅ **Clean Architecture**: Código organizado com princípios SOLID

## Instalação

```bash
pip install cpf
```

## Uso Rápido

### CPF

```python
import cpf

# Validação
cpf.validate("494.351.429-40")  # True
cpf.validate("49435142940")      # True (aceita sem formatação)
cpf.validate("111.111.111-11")  # False (dígitos iguais)

# Validação com informação de região
result = cpf.validate("494.351.429-40", show_region=True)
# {'valid': True, 'region': 'Paraná – Santa Catarina'}

# Geração
cpfs = cpf.generate(count=5)
# ['222.272.431-78', '157.258.802-50', ...]

# Geração por região (número, nome ou sigla)
cpfs = cpf.generate(count=3, region=8)        # São Paulo
cpfs = cpf.generate(count=3, region="SP")     # por sigla
cpfs = cpf.generate(count=3, region="rio de janeiro")  # por nome

# Sem formatação
cpfs = cpf.generate(count=2, formatted=False)
# ['22227243178', '15725880250']
```

### CNPJ

```python
import cnpj

# Validação
cnpj.validate("11.222.333/0001-81")  # True
cnpj.validate("11222333000181")       # True (aceita sem formatação)
cnpj.validate("11.111.111/1111-11")  # False (dígitos iguais)

# Geração de matrizes (filial 0001)
cnpjs = cnpj.generate(count=5, matriz_only=True)
# ['11.222.333/0001-81', '45.678.901/0001-23', ...]

# Geração com filiais aleatórias
cnpjs = cnpj.generate(count=5, matriz_only=False)
# ['11.222.333/0245-67', '45.678.901/1234-56', ...]

# Sem formatação
cnpjs = cnpj.generate(count=2, formatted=False)
# ['11222333000181', '45678901000123']
```

## Regiões do CPF

O 9º dígito do CPF indica a região de emissão:

| Código | Estados |
|--------|---------|
| **0** | RS |
| **1** | DF, GO, MS, MT, TO |
| **2** | AC, AM, AP, PA, RO, RR |
| **3** | CE, MA, PI |
| **4** | AL, PB, PE, RN |
| **5** | BA, SE |
| **6** | MG |
| **7** | ES, RJ |
| **8** | SP |
| **9** | PR, SC |

## Desenvolvimento

### Instalando dependências

```bash
git clone https://github.com/pedrokpp/gerador-e-checker-de-cpf
cd gerador-e-checker-de-cpf
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate no Windows
pip install -e ".[dev]"
```

### Rodando testes

```bash
pytest tests/ -v
pytest tests/ --cov=src/cpf --cov=src/cnpj  # Com coverage
```

### Build

```bash
python -m build
```

## Exemplos CLI

O projeto inclui scripts de exemplo interativos:

```bash
python examples/cli_modern.py  # CPF (API v3.0)
python examples/cli_cnpj.py    # CNPJ (API v3.1)
python examples/cli_legacy.py  # CPF (API v2.x compatível)
```

Ver [examples/README.md](examples/README.md) para mais detalhes.

## Estrutura do Projeto

```
src/
├── cpf/                  # Módulo CPF
│   ├── domain/          # Entidades (CPF, Region)
│   ├── application/     # Casos de uso
│   ├── infrastructure/  # Validador e gerador
│   └── presentation/    # API pública
└── cnpj/                 # Módulo CNPJ
    ├── domain/          # Entidades (CNPJ)
    ├── application/     # Casos de uso
    ├── infrastructure/  # Validador e gerador
    └── presentation/    # API pública
```

## API Legada

A biblioteca mantém compatibilidade com versão 2.x para CPF:

```python
import cpf

# Funções legadas (backward compatible)
cpf.checar("494.351.429-40")  # equivalente a validate()
cpf.gerar(quantidade=5)        # equivalente a generate()
```

## Atenção

Estes scripts validam CPFs e CNPJs de acordo com os **padrões técnicos** brasileiros (algoritmo módulo 11). A validação **não garante** que o documento está cadastrado na Receita Federal, apenas que é um número válido segundo as regras de formação.

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Reportando Bugs

Abra uma [issue](https://github.com/pedrokpp/gerador-e-checker-de-cpf/issues) com:
- Descrição do problema
- Exemplo de código que reproduz o bug
- Comportamento esperado vs comportamento atual
- Versão do Python e da biblioteca

## Licença

MIT License - veja [LICENSE.txt](LICENSE.txt) para detalhes.

## Autor

**pedrokp** - [pedrkp@proton.me](mailto:pedrkp@proton.me)

## Links

- 📦 [PyPI](https://pypi.org/project/cpf/)
- 🐙 [GitHub](https://github.com/pedrokpp/gerador-e-checker-de-cpf)
- 🐛 [Issues](https://github.com/pedrokpp/gerador-e-checker-de-cpf/issues)
- 📋 [CHANGELOG](CHANGELOG.md)
