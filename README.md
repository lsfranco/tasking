Tasking
===

Facilita a execução de tarefas paralelas
---

Este módulo tem como objetivo facilitar a execução de tarefas paralelas com uso de threads. Recebe uma lista de tarefas e um método que saiba como executa-las, com isso lança threads que consumirão as tarefas e ao fim retorna uma lista com os valores de retorno do método.

Modo de uso
---

O uso mais simples do módulo é passando uma lista de tarefas e um método consumidor de tarefas:

```python
from tasking import TaskingManager

tasks = ['um', 'dois', 'tres']
consumer = lambda value: "retorno %s" % value

manager = TaskingManager(tasks, consumer)
manager.process_tasks()
```

O método `process_tasks()` retornará uma lista de **tuplas** contendo a task em si e o retorno do método `consumer()`

Retorno:

```python
[('um', 'retorno um'), ('dois', 'retorno dois'), ('tres', 'retorno tres')]
```

A classe `TaskingManager()` pode receber os seguintes parametros:

```python
TaskingManager(
    tasks,                  #lista de tarefas
    consumer,               #método consumidor
    threads=5,              #numero de threads simutaneas
    retries=3,              #quantidade de retentativas
    retry_condition=None,   #valor esperado para retentativa
    get_task_name=None      #metodo para nomear as tasks no retorno
)
```

Usando *retries* e *retry_condition*
---

Os parametros *`retries`* e *`retry_condition`* dão a possibilidade da thread tentar executar mais de uma vez o método `consumer()`.

A thread repetirá o método `consumer()` até receber um valor diferente do especificado em  *`retry_condition`* ou igualar a quantidade de *`retries`*

```python
from tasking import TaskingManager

tasks = ['um', 'dois', 'tres']

def consumer(value):
    if value in ['dois']:
        print "tentando", value
        return False
    return "retorno %s" % value

manager = TaskingManager(tasks, consumer, retries=3, retry_condition=False)
manager.process_tasks()
```

Usando *get_task_name*
---

Por padrão o método `process_tasks()` retorna uma lista de tuplas contendo a task em si e o retorno do método `consumer()`, porém é possível alterar o primeiro valor da tupla com o parametro *`get_task_name`*. Este paramentro recebe um método que deve retornar uma `string`.

```python
from tasking import TaskingManager

tasks = ['um', 'dois', 'tres']
consumer = lambda value: "retorno %s" % value
names = lambda value: "task-%s" % value

manager = TaskingManager(tasks, consumer, get_task_name=names)
manager.process_tasks()
```

Retorno:

```python
[('task-um', 'retorno um'), ('task-dois', 'retorno dois'), ('task-tres', 'retorno tres')]
```

O arquivo `example.py` usa todos os parametros disponíveis na classe `TaskingManager()` em um exemplo com o modulo **`requests`**

Dependencias
---

* python 2.7
