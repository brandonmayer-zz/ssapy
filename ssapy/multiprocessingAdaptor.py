import multiprocessing

class Consumer(multiprocessing.Process):
    #can call functors that return an answer or that 
    #manipulate memory but return void
    def __init__(self,task_queue, result_queue = None):
        multiprocessing.Process.__init__(self)
        self.task_queue   = task_queue
        self.result_queue = result_queue
        
    def run(self):
        while True:
            next_task = self.task_queue.get()
            if next_task is None:
                print '{0}: Exiting'.format(self.name)
                self.task_queue.task_done()
                break
            print'{0} - running task: '.format(self.name, next_task.__str__())
            
            if self.result_queue != None:
                self.result_queue.put(next_task())
            else:
                next_task()
            self.task_queue.task_done()
            
        return
    