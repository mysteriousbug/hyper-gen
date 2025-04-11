import streamlit as st

# Configure page
st.set_page_config(page_title="CodeT5: Live Translation", layout="wide")
st.title("Code Translator")

# Language options
LANGUAGES = {
    "Python": "python",
    "Java": "java",
    "C++": "cpp",
    "JavaScript": "javascript"
}

# Your Java code
JAVA_CODE = """import java.util.concurrent.*;
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

# Main app layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Code")
    source_lang = st.selectbox("From:", list(LANGUAGES.keys()))
    
    source_code = st.text_area(
        "Enter your code:", 
        height=300,
        placeholder=f"Enter {source_lang} code here...",
        key="source"
    )
    
    uploaded_file = st.file_uploader("Or upload file:", type=list(LANGUAGES.values()))
    
    if uploaded_file:
        source_code = uploaded_file.getvalue().decode("utf-8")

with col2:
    st.subheader("Output Code")
    target_lang = st.selectbox("To:", list(LANGUAGES.keys()))
    
    if st.button("Show Java Example"):
        st.session_state.show_java = True
    
    if target_lang == "Python":
        st.warning("Note: This is a static example. For actual translation, you'll need to implement or connect to a translation service.")
        
        if st.button("Download Java Example"):
            st.download_button(
                label="Click to confirm download",
                data=JAVA_CODE,
                file_name="MultiThreadingExample.java",
                mime="text/plain",
                key="java_download"
            )
        
        st.code(JAVA_CODE, language="java")
    else:
        st.info("Select Python as target language to see the Java example")

st.markdown("""
<style>
.stCodeBlock {
    max-height: 500px;
    overflow-y: auto;
}
</style>
""", unsafe_allow_html=True)
