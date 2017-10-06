"""
    Facilita a execucao de tarefas em threads

    Criado por: lsfranco@uoldiveo.com
    Em: 2017-10-05

    Ex.:
        manager = TaskingManager(tasks, consumer)
        manager.process_tasks()
"""
import Queue
import threading

class Job(threading.Thread):
    """ k """
    def __init__(self, thread_id, name, task_queue, task_consumer):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.task_queue = task_queue
        self.task_consumer = task_consumer

    def run(self):
        self.task_consumer(self.task_queue)

class TaskingManager(object):
    """
        Gerencia a lista as threads para execucao das tarefas

        Params:
        - tasks: lista de tarefas
        - consumer: metodo que saiba excutar as tarefas individualmente
        - threads: numero de threads simutaneas. Padrao: 5
        - retries: quantidade de retentativas. Padrao: 3
        - retry_condition: valor esperado para retentativa. Padrao: None
        - get_task_name: metodo para nomear as tasks no retorno.
                    Se nao for informado a task em si sera o nome.
    """
    def __init__(
            self, tasks, consumer, threads=5,
            retries=3, retry_condition=None,
            get_task_name=None):
        self.queue_lock = threading.Lock()
        self.tasks = tasks
        self.work_queue = Queue.Queue(len(tasks))
        self.consumer = consumer
        self.get_task_name = get_task_name
        self.thread_size = threads
        self.retries = retries
        self.retry_condition = retry_condition
        self.exit_flag = 0
        self.job_result = []

    def process_data(self, task_queue):
        """ Processa e controla o consumo da fila """
        while not self.exit_flag:
            self.queue_lock.acquire()
            if not self.work_queue.empty():
                data = task_queue.get()
                self.queue_lock.release()
                result = None
                if self.get_task_name is not None:
                    job_name = self.get_task_name(data)
                else:
                    job_name = data
                for item in range(self.retries):
                    try:
                        result = self.consumer(data)
                    except Exception as error:
                        self.job_result.append((job_name, {'error': str(error.message)}))
                        raise
                    if result != self.retry_condition:
                        break
                self.job_result.append((job_name, result))
            else:
                self.queue_lock.release()

    def process_tasks(self):
        """ Inicia o processamento das tasks
            Retorna uma lista com os resultados
        """
        thread_list = ["thread-%s" % x for x in range(0, self.thread_size)]
        threads = []
        thread_id = 1

        # Create new threads
        for t_name in thread_list:
            thread = Job(thread_id, t_name, self.work_queue, self.process_data)
            thread.start()
            threads.append(thread)
            thread_id += 1

        # Fill the queue
        self.queue_lock.acquire()
        for word in self.tasks:
            self.work_queue.put(word)
        self.queue_lock.release()

        # Wait for queue to empty
        while not self.work_queue.empty():
            pass

        # Notify threads it's time to exit
        self.exit_flag = 1

        # Wait for all threads to complete
        for item in threads:
            item.join()

        return self.job_result
