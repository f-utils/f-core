# Idea

> abordagem unificada e construtivista para funções do dia a dia do Python

* Ferramentas:
1. **abordagem funcional**: foco em funções ao invés de objetos
2. **polimorfismo paramétrico**: mesma função para diferentes tipos de variáveis.
    * `add`: se aplica tanto para números, quanto para strings, tuples, listas, dicts, sets, etc.

# Estratégia 1

* construção de polimorfismo paramétrico **sem** abordagem funcional

```python
def add(x, y):
    if type(x) is str and type(y) is str:
        return add_str(x, y)
    elif type(x) is list and type(y) is list:
        return add_list(x, y)
    elif type(x) is str and type(y) is list:
        return add_str_list(x, y)
    ...
    else:
        raise TypeError(f'tipos {x} ou {y} não são aceitos para a função add.')
```

* Problemas:
    1. precisa-se ter todos os tipos a serem consumidos por uma função definidos antes da definição da função.
    2. caso algum tipo seja esquecido, o usuário obtém um erro genérico [ausência de "type safety"]
    3. caso seja necessário adicionar um novo tipo, o tipo precisa ser definido antes da  função e a função precisa ser refatorada.

> Estado atual do `futils`.

# Estratégia 2

* Construção de polimorfismo paramétrico com abordagem funcional.
* Abordagem funcional:
    1. funções possuem um tipo
    2. funções podem ser armazenadas em variáveis
    3. pode-se passar funções como argumento ou retornar funções dentro de outras funções
* Trabalha-se com o `spectrum` de uma função, o qual descreve seu "estado".
    1. nome da função: `name: str`
    2. lista de tipos: `domain: list` (tipos aceitáveis da função)
    3. corpo: `body: dict`
        * `tipo_x: função_de_retorno_do_tipo_x`, onde `tipo_x` é um tipo aceitável
    4. retorno padrão: `std: function` 

```python
spec=(name, domain, body, std)
```

* Tem-se os seguintes "métodos" principais:
    1. `func`: inicializa uma função com `domain` vazio: `init('nome', retorno_padrao)`
    2. `extend`: adiciona uma entrada no domínio e no corpo de uma função já inicializada. `extend(nome, tipo_x, retorno_tipo_x)`
    3. `update`: modifica corpo ou retorno padrão de uma função.


> É para onde o `futils` vai.
> [ximenesyuri/safe](https://github.com/ximenesyuri/safe)
