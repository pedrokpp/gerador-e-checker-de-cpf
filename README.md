# Gerador e Validador de CPF

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Uma biblioteca Python moderna para validar e gerar CPFs (Cadastro de Pessoas Físicas) brasileiros de acordo com o algoritmo oficial.

## Características

- ✅ **Validação correta**: Usa o algoritmo módulo 11 oficial
- ✅ **Geração eficiente**: Gera CPFs válidos de forma determinística  
- ✅ **Suporte a regiões**: Valida e gera CPFs por estado/região
- ✅ **Formatação flexível**: Aceita CPFs formatados ou não
- ✅ **Type hints completos**: Totalmente tipado para melhor IDE support
- ✅ **Testado**: 97% de code coverage com testes unitários e de integração
- ✅ **Clean Architecture**: Código organizado com princípios SOLID
- ✅ **Backward compatible**: Mantém compatibilidade com versão 2.x

## Instalação

```bash
pip install cpf
```

## Uso Rápido

### API Moderna (v3.0+)

```python
import cpf

# Validação simples
cpf.validate("494.351.429-40")  # True
cpf.validate("49435142940")      # True (aceita sem formatação)
cpf.validate("111.111.111-11")  # False (dígitos iguais)

# Validação com informação de região
result = cpf.validate("494.351.429-40", show_region=True)
# {'valid': True, 'region': 'Paraná – Santa Catarina'}

# Geração de CPFs
cpfs = cpf.generate(count=5)
# ['222.272.431-78', '157.258.802-50', ...]

# Gerar CPFs de uma região específica (por número)
cpfs = cpf.generate(count=3, region=8)  # São Paulo
# ['874.152.887-82', '447.887.248-50', ...]

# Gerar CPFs de uma região específica (por nome/sigla)
cpfs = cpf.generate(count=3, region="SP")
cpfs = cpf.generate(count=3, region="São Paulo")
cpfs = cpf.generate(count=3, region="rio de janeiro")

# Gerar CPFs sem formatação
cpfs = cpf.generate(count=2, formatted=False)
# ['22227243178', '15725880250']
```

### API Legada (v2.x - Compatibilidade)

A biblioteca mantém 100% de compatibilidade com a versão 2.x:

```python
import cpf

# checar() - equivalente a validate()
cpf.checar("494.351.429-40")  # True
cpf.checar("494.351.429-40", regiao=True)  # True + imprime região

# gerar() - equivalente a generate()  
cpfs = cpf.gerar(quantidade=5)
cpfs = cpf.gerar(quantidade=5, regiao=8)  # São Paulo
```

## Regiões do CPF

O 9º dígito do CPF indica a região de emissão:

| Código | Região | Estados |
|--------|--------|---------|
| **0** | Rio Grande do Sul | RS |
| **1** | Centro-Oeste | DF, GO, MS, MT, TO |
| **2** | Norte | AC, AM, AP, PA, RO, RR |
| **3** | Nordeste (Norte) | CE, MA, PI |
| **4** | Nordeste (Leste) | AL, PB, PE, RN |
| **5** | Nordeste (Sul) | BA, SE |
| **6** | Sudeste | MG |
| **7** | Sudeste | ES, RJ |
| **8** | Sudeste | SP |
| **9** | Sul | PR, SC |

## Exemplos Avançados

### Validação

```python
import cpf

# Valida CPFs que falhavam incorretamente na v2.x (Issue #2 - RESOLVIDO)
cpf.validate("494.351.429-40")  # ✅ True
cpf.validate("654.926.122-80")  # ✅ True  
cpf.validate("132.923.016-70")  # ✅ True
cpf.validate("918.758.814-50")  # ✅ True

# Aceita formatação variada
cpf.validate("494.351.429-40")  # Com pontos e hífen
cpf.validate("49435142940")      # Sem formatação
cpf.validate("494 351 429 40")  # Com espaços (é normalizado)

# Rejeita CPFs inválidos
cpf.validate("000.000.000-00")  # False - todos dígitos iguais
cpf.validate("123.456.789-00")  # False - dígitos verificadores errados
```

### Geração

```python
import cpf

# Gerar CPF de estado específico usando sigla
sp_cpf = cpf.generate(region="SP")[0]
print(sp_cpf)  # Ex: "874.152.887-82"

# Gerar vários CPFs do Rio de Janeiro
rj_cpfs = cpf.generate(count=10, region="RJ")

# Gerar CPFs sem formatação para banco de dados
unformatted = cpf.generate(count=5, formatted=False)
print(unformatted)  # ['87415288782', '44788724850', ...]

# Gerar CPFs com regiões aleatórias (padrão)
random_cpfs = cpf.generate(count=100)
```

## Novidades na Versão 3.0

### 🐛 Correções

- **[Issue #2]** Corrigido algoritmo de validação que rejeitava CPFs válidos incorretamente
  - CPFs como `494.351.429-40` agora são validados corretamente
  - Implementado algoritmo módulo 11 oficial
  
- **[Issue #1]** Migração para `pyproject.toml` (PEP 517/518)
  - Suporte moderno para instalação via pip
  - Compatível com pip 23.1+

### ✨ Novos Recursos

- **Região por nome**: Gere CPFs usando nome ou sigla do estado
  ```python
  cpf.generate(region="SP")
  cpf.generate(region="São Paulo")
  ```

- **Formatação configurável**: Escolha se quer CPFs formatados ou não
  ```python
  cpf.generate(formatted=False)  # Retorna XXXXXXXXXXX
  cpf.generate(formatted=True)   # Retorna XXX.XXX.XXX-XX
  ```

- **Nova API moderna**: Funções `validate()` e `generate()` mais pythônicas
- **Type hints completos**: Melhor suporte para IDEs e type checkers
- **97% de test coverage**: Testes unitários e de integração extensivos

### 🏗️ Melhorias Técnicas

- **Clean Architecture**: Código organizado em camadas (Domain, Application, Infrastructure, Presentation)
- **Princípios SOLID**: Código mais manutenível e extensível
- **Geração eficiente**: Novo algoritmo determinístico (sem loops infinitos)
- **Python 3.8+**: Suporte para Python 3.8, 3.9, 3.10, 3.11 e 3.12
- **Cross-platform**: Funciona em Windows, Linux e macOS

## Desenvolvimento

### Instalando dependências de desenvolvimento

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
pytest tests/ --cov=src/cpf  # Com coverage
```

### Build

```bash
pip install build
python -m build
```

## Exemplos CLI

O projeto inclui scripts de exemplo interativos:

### Interface Moderna (v3.0 API)
```bash
python examples/cli_modern.py
```
- Validação com informação de região
- Geração com região por nome/sigla ("SP", "Rio de Janeiro")
- Formatação configurável
- Validação em lote

### Interface Legada (v2.x API)
```bash
python examples/cli_legacy.py
```
- Demonstra backward compatibility
- Usa funções `checar()` e `gerar()`

Ver [examples/README.md](examples/README.md) para mais detalhes e exemplos de código.

## Estrutura do Projeto

```
src/cpf/
├── domain/          # Entidades e regras de negócio
│   ├── entities.py  # CPF value object
│   └── region.py    # Enum de regiões
├── application/     # Casos de uso
│   ├── validate_cpf.py
│   └── generate_cpf.py
├── infrastructure/  # Implementações concretas
│   ├── cpf_validator.py  # Validador módulo 11
│   └── cpf_generator.py  # Gerador determinístico
└── presentation/    # API pública
    └── api.py       # validate(), generate(), checar(), gerar()

examples/           # Scripts CLI de exemplo
├── cli_modern.py  # Interface moderna (v3.0 API)
├── cli_legacy.py  # Interface legada (v2.x API)
└── README.md      # Documentação dos exemplos
```

## Atenção

Este script valida CPFs de acordo com os **padrões técnicos** brasileiros (algoritmo módulo 11). A validação **não garante** que o CPF está cadastrado na Receita Federal, apenas que é um número válido segundo as regras de formação.

## Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

### Reportando Bugs

Se encontrar um bug, por favor abra uma [issue](https://github.com/pedrokpp/gerador-e-checker-de-cpf/issues) com:
- Descrição do problema
- Exemplo de código que reproduz o bug
- Comportamento esperado vs comportamento atual
- Versão do Python e da biblioteca

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.txt](LICENSE.txt) para detalhes.

## Autor

**pedrokp** - [pedrokp@protonmail.com](mailto:pedrokp@protonmail.com)

## Links

- 📦 [PyPI](https://pypi.org/project/cpf/)
- 🐙 [GitHub](https://github.com/pedrokpp/gerador-e-checker-de-cpf)
- 🐛 [Issues](https://github.com/pedrokpp/gerador-e-checker-de-cpf/issues)
