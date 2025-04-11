import streamlit as st

# Configure page
st.set_page_config(page_title="Python to Java Translator", layout="wide")
st.title("Python to Java Code Translator")

# Your Java threading implementation
JAVA_OUTPUT_CODE = """import java.util.concurrent.*;
import java.util.Random;

public class MultiThreadingExample {
    private static final int NUM_WORKERS = 5;
    private static final int TASKS_PER_WORKER = 3;
    private static final int TASK_COMPLETION_TIME_MIN = 1;
    private static final int TASK_COMPLETION_TIME_MAX = 5;

    private static BlockingQueue<Integer> taskQueue = new LinkedBlockingQueue<>();
    private static final Object printLock = new Object();

    static class Worker implements Runnable {
        private int workerId;

        public Worker(int workerId) {
            this.workerId = workerId;
        }

        @Override
        public void run() {
            try {
                while (true) {
                    Integer task = taskQueue.take();
                    if (task == null) {
                        break;
                    }

                    Random rand = new Random();
                    int processingTime = rand.nextInt(TASK_COMPLETION_TIME_MAX - TASK_COMPLETION_TIME_MIN + 1) + TASK_COMPLETION_TIME_MIN;

                    synchronized (printLock) {
                        System.out.println("Worker " + workerId + " is processing task " + task + " (will take " + processingTime + " seconds)");
                    }

                    Thread.sleep(processingTime * 1000);

                    synchronized (printLock) {
                        System.out.println("Worker " + workerId + " completed task " + task);
                    }
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    static class Manager implements Runnable {
        @Override
        public void run() {
            try {
                for (int taskId = 1; taskId <= NUM_WORKERS * TASKS_PER_WORKER; taskId++) {
                    taskQueue.put(taskId);
                    synchronized (printLock) {
                        System.out.println("Manager assigned task " + taskId);
                    }
                }

                while (!taskQueue.isEmpty()) {
                    Thread.sleep(1000);
                }

                synchronized (printLock) {
                    System.out.println("All tasks have been completed.");
                }

                for (int i = 0; i < NUM_WORKERS; i++) {
                    taskQueue.put(null);
                }
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

    public static void main(String[] args) {
        Thread[] workers = new Thread[NUM_WORKERS];
        for (int i = 0; i < NUM_WORKERS; i++) {
            workers[i] = new Thread(new Worker(i + 1));
            workers[i].start();
        }

        Thread managerThread = new Thread(new Manager());
        managerThread.start();

        for (Thread worker : workers) {
            try {
                worker.join();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }

        try {
            managerThread.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        System.out.println("All workers and manager have finished.");
    }
}"""

# Default Python example
PYTHON_EXAMPLE = """import threading
import time
import random
from queue import Queue

# Worker function
def worker(worker_id, task_queue, print_lock):
    while True:
        task = task_queue.get()
        if task is None:
            break
            
        with print_lock:
            print(f"Worker {worker_id} processing task {task}")
        time.sleep(random.uniform(0.5, 1.5))
        with print_lock:
            print(f"Worker {worker_id} completed task {task}")
        task_queue.task_done()

if __name__ == "__main__":
    num_workers = 5
    tasks_per_worker = 3
    task_queue = Queue()
    print_lock = threading.Lock()
    
    # Create and start workers
    workers = []
    for i in range(num_workers):
        t = threading.Thread(target=worker, args=(i+1, task_queue, print_lock))
        t.start()
        workers.append(t)
    
    # Add tasks
    for task in range(1, num_workers * tasks_per_worker + 1):
        task_queue.put(task)
    
    # Wait for all tasks to complete
    task_queue.join()
    
    # Stop workers
    for _ in range(num_workers):
        task_queue.put(None)
    for t in workers:
        t.join()"""

# Main app layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Python Source Code")
    python_code = st.text_area(
        "Enter Python code:", 
        height=300,
        value=PYTHON_EXAMPLE,
        key="python_source"
    )
    
    # File upload option
    uploaded_file = st.file_uploader("Or upload Python file:", type=["py"])
    if uploaded_file:
        python_code = uploaded_file.getvalue().decode("utf-8")

with col2:
    st.subheader("Java Translation")
    st.code(JAVA_OUTPUT_CODE, language="java")
    
    # Download buttons
    st.download_button(
        label="Download Java Code",
        data=JAVA_OUTPUT_CODE,
        file_name="MultiThreadingExample.java",
        mime="text/plain"
    )

st.info("Note: This is a static example showing Python to Java threading conversion. For dynamic translation, you would need to implement a translation service.")
