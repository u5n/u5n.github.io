---
layout: post
title:  "竞争条件-linux"
date:   2017-10-14
categories: posts
---

# <sub>未经整理,思维的输出
## Meaning
输出结果受 不可控的事件的执行 序列/时间 的影响
## 收集方向
1. ~~搜索引擎~~

2. ~~leetcode~~

3. java多线程设计模式(放弃)

4. ~~<linux高级程序设计>~~

5. github项目
## Method
    function () {

    }
    pthread_create
    pthread_exit
    pthread_join
    pthread_cancel
    pthread_self

    pthread_key_t key
    pthread_setspecific(key,&i)
    pthread_getspecific(key)
    //私有变量
## Example
    ...

    <pthread1.c>
    <pthreadcond.c>
    <pthreadrw.c>
在我做的server上确实可能存在race condition问题,解决方案是简单的互斥锁
## Question
      Two thread updating a variable (initial value of 0) without a lock,
      each thread uses a loop of 50 to increment a global variable.
      What is the minimum and maximum possible value you can get?
      4 steps:Mem->cache1;Load Cache2;cal cache1+cache2->cache3;cache3->mem1;
      

## How to Avoid
### 手动sleep,手动bool(不安全)
### 互斥锁:解决资源的互斥访问
    pthread_mutex_t lockthing;//占用一个共享资源(厕所)
    pthread_mutex_init()
    pthread_lock();
    pthread_unlock();
    pthread_mutex_destroy();
### 条件变量配合互斥锁
    pthread_cond_t conditionthing;
    pthread_cond_init
    pthread_cond_wait//阻塞,参考golang <-chan
    pthread_cond_timedwait//阻塞,参考golang时间信号
    pthread_cond_siginal/broadcast
    pthread_cond_broadcast
    pthread_cond_destroy
### 读写锁
#### (多读少写时提高效率,读取时不互斥(逻辑上))
    pthread_rwlock_t rwlockthing;
    pthread_rwlock_init
    pthread_rwlock_rdlock;//block read lock
    pthread_rwlock_tryrdlock;//read lock
    pthread_rwlock_wrlock;//block write lock
    pthread_rwlock_trywrlock;//write lock
    pthread_rwlock_unlock//read release in this thread;write all release
    pthread_rwlock_destroy
##
    两个进程不同时在critical region
    程序不针对CPU设计
    不在critical region的不阻塞其他进程
## Others
自旋锁(占用cpu)

    // 线程A
          while (true) {
              while (turn != 0) {}         // 锁被占，循环忙等。
             critical_rigion();
                turn = 1;                      // 释放锁
                noncritical_rigion();
            }
            // 线程B
            while (true) {
                while (turn != 1) {}         // 锁被占，循环忙等
                critical_rigion();
                turn = 0;                    // 释放锁
                noncritical_rigion();
            }
    
pthread_mutex_lock的实现

    mutex_lock:
        TSL REGISTER,MUTEX    |将互斥量复制到寄存器，并且将互斥量重置为1
        CMP REGISTER,#0         |互斥量是0吗？
        JZE ok                          |如果互斥量为0，解锁，返回
        CALL thread_yield          |互斥量忙，调度另一线程
        JMP mutex_lock            |稍后再试
    ok: RET                            |返回调用这，进入临界区
    
原子操作:如果这个操作所处的层(layer)的更高层不能发现其内部实现与结构，那么这个操作是一个原子(atomic)操作