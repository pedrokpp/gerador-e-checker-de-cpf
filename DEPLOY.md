# Instruções de Deploy - CPF/CNPJ v3.1.0

## Pré-requisitos

- Python 3.8+
- Conta no PyPI (https://pypi.org)
- Token de API do PyPI configurado

## Verificações Antes do Deploy

### 1. Executar todos os testes

```bash
# Ativar ambiente virtual
source .venv/bin/activate  # Linux/Mac
# ou .venv\Scripts\activate  # Windows

# Rodar testes (CPF e CNPJ)
pytest tests/ -v --cov=src/cpf --cov=src/cnpj

# Verificar que todos os 209 testes passaram (112 CPF + 97 CNPJ)
# Coverage deve estar em ~98%
```

### 2. Verificar que as issues foram resolvidas

```bash
# Testar CPFs da issue #2
python -c "
import sys
sys.path.insert(0, 'src')
from cpf import validate
cpfs = ['49435142940', '65492612280', '13292301670', '91875881450']
for c in cpfs:
    assert validate(c), f'CPF {c} should be valid'
print('✅ Issue #2 resolvida!')
"
```

### 2.5. Verificar funcionalidades CNPJ

```bash
# Testar CNPJs válidos conhecidos
python -c "
import sys
sys.path.insert(0, 'src')
import cnpj

# Validar CNPJs conhecidos
assert cnpj.validate('11.222.333/0001-81'), 'CNPJ válido deve passar'
assert cnpj.validate('11222333000181'), 'CNPJ válido sem formatação deve passar'
assert not cnpj.validate('11.111.111/1111-11'), 'CNPJ inválido deve falhar'

# Gerar CNPJs
cnpjs = cnpj.generate(count=5, matriz_only=True)
assert len(cnpjs) == 5, 'Deve gerar 5 CNPJs'
for c in cnpjs:
    assert cnpj.validate(c), f'CNPJ {c} deve ser válido'

print('✅ Funcionalidades CNPJ verificadas!')
"
```

### 3. Build do pacote

```bash
# Limpar builds anteriores
rm -rf dist/*.whl dist/cpf-3.1.0.tar.gz

# Fazer build
python -m build

# Verificar arquivos gerados
ls -lh dist/
# Deve conter:
# - cpf-3.1.0-py3-none-any.whl
# - cpf-3.1.0.tar.gz
```

### 4. Testar instalação local

```bash
# Criar ambiente virtual de teste
python -m venv /tmp/test_cpf
source /tmp/test_cpf/bin/activate

# Instalar wheel
pip install dist/cpf-3.1.0-py3-none-any.whl

# Testar funcionalidades CPF e CNPJ
python -c "
import cpf
import cnpj

# Testar CPF (existente)
assert cpf.validate('49435142940')
cpfs = cpf.generate(count=3, region='SP')
assert len(cpfs) == 3

# Testar CNPJ (novo!)
assert cnpj.validate('11.222.333/0001-81')
cnpjs = cnpj.generate(count=3, matriz_only=True)
assert len(cnpjs) == 3

# Backward compatibility CPF
assert cpf.checar('49435142940')
cpfs_legacy = cpf.gerar(2, 8)
assert len(cpfs_legacy) == 2

print('✅ CPF e CNPJ testados com sucesso!')
"

# Sair do ambiente de teste
deactivate
```

## Deploy para PyPI

### Opção 1: Upload Manual (Recomendado para primeira vez)

1. **Instalar twine** (se ainda não tiver):
```bash
pip install twine
```

2. **Upload para TestPyPI** (opcional, mas recomendado):
```bash
# Upload para test.pypi.org primeiro
twine upload --repository testpypi dist/*

# Testar instalação do TestPyPI
pip install --index-url https://test.pypi.org/simple/ cpf==3.1.0
```

3. **Upload para PyPI produção**:
```bash
# Upload para pypi.org
twine upload dist/*

# Você será solicitado a fornecer:
# Username: __token__
# Password: pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (seu token de API)
```

4. **Verificar no PyPI**:
   - Acesse https://pypi.org/project/cpf/
   - Verifique se a versão 3.1.0 aparece
   - Verifique se o README.md está renderizado corretamente (com exemplos de CNPJ)

### Opção 2: Usando Token Salvo

1. **Configurar ~/.pypirc** (uma única vez):
```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

[testpypi]
username = __token__
password = pypi-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

2. **Upload**:
```bash
twine upload dist/*
```

## Após o Deploy

### 1. Criar Git Tag

```bash
git tag -a v3.1.0 -m "Release v3.1.0 - Adiciona suporte a CNPJ"
git push origin v3.1.0
```

### 2. Criar GitHub Release

1. Ir para https://github.com/pedrokpp/gerador-e-checker-de-cpf/releases/new
2. Selecionar a tag `v3.1.0`
3. Título: `v3.1.0 - Suporte a CNPJ`
4. Descrição: Copiar do CHANGELOG.md
5. Anexar os arquivos:
   - `dist/cpf-3.1.0-py3-none-any.whl`
   - `dist/cpf-3.1.0.tar.gz`
6. Publicar release

### 3. Testar Instalação Pública

```bash
# Criar novo ambiente virtual
python -m venv /tmp/test_public
source /tmp/test_public/bin/activate

# Aguardar alguns minutos após o upload, então:
pip install cpf

# Verificar versão
python -c "import cpf; print('Versão instalada:', cpf.__version__)"

# Testar funcionalidades CPF e CNPJ
python -c "
import cpf
import cnpj

# CPF
assert cpf.validate('49435142940')
cpfs = cpf.generate(count=3, region='SP')

# CNPJ
assert cnpj.validate('11.222.333/0001-81')
cnpjs = cnpj.generate(count=3)

print(f'✅ CPF e CNPJ funcionando!')
print(f'CPFs: {cpfs}')
print(f'CNPJs: {cnpjs}')
"
```

### 4. Fechar Issues

Ir para as issues no GitHub e comentar:

**Issue #1:**
> Resolvido na versão 3.0.0!
> 
> O projeto foi migrado para `pyproject.toml` usando `hatchling` como build backend (PEP 517/518).
> Agora é compatível com pip 23.1+ e não gera mais avisos de deprecação.
> 
> Para atualizar: `pip install --upgrade cpf`

**Issue #2:**
> Resolvido na versão 3.0.0!
> 
> O algoritmo de validação foi completamente reescrito usando o método módulo 11 oficial.
> Todos os CPFs mencionados agora são validados corretamente:
> - ✅ 494.351.429-40
> - ✅ 654.926.122-80
> - ✅ 132.923.016-70
> - ✅ 918.758.814-50
> 
> A biblioteca agora tem 97% de test coverage com 112 testes automatizados.
> Para atualizar: `pip install --upgrade cpf`

## Rollback (Se Necessário)

Se algo der errado:

```bash
# PyPI não permite deletar versões, mas você pode "yank" (marcar como não recomendada)
# Isso ainda permite que quem já instalou continue usando
# Entre em contato com PyPI support se necessário
```

## Checklist Final

Antes de fazer deploy, confirme:

- [ ] Todos os 209 testes passando (112 CPF + 97 CNPJ)
- [ ] Coverage >= 98%
- [ ] README.md atualizado com exemplos CNPJ
- [ ] CHANGELOG.md atualizado com v3.1.0
- [ ] Versão correta no pyproject.toml (3.1.0)
- [ ] Build local funcionando
- [ ] Teste de instalação local passou (CPF + CNPJ)
- [ ] CPFs da issue #2 validando corretamente
- [ ] CNPJs validando e gerando corretamente
- [ ] Backward compatibility CPF funcionando
- [ ] Código commitado no Git
- [ ] Branch main atualizada

## Dúvidas?

Consulte a documentação oficial:
- PyPI: https://packaging.python.org/tutorials/packaging-projects/
- twine: https://twine.readthedocs.io/
- pyproject.toml: https://packaging.python.org/specifications/declaring-project-metadata/
