import blog_craw
import threading
import time

def single_thread_craw():
    print("single thread begin")
    for url in blog_craw.urls:
        blog_craw.craw(url)
    print("single thread end")
    
def multi_thread_craw():
    print("multi thread begin")
    threads = []
    for url in blog_craw.urls:
        t = threading.Thread(target=blog_craw.craw,args=(url,))
        threads.append(t)
    
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
        
    print("multi thread end")
    
if __name__ == "__main__":
    start = time.time()
    single_thread_craw()
    end = time.time()
    print("single thread time :",end - start,"seconds")
    
    start = time.time()
    multi_thread_craw()
    end = time.time()
    print("multi thread time :",end - start,"seconds")
    