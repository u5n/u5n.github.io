/*
a dynamic arraylist API
use macro to try to make template on different TYPE
*/
#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<limits.h>
#define D(s,...) printf(s"\n", __VA_ARGS__);
#define Di(i) D("%d", (i))
#define Ds(i) D("%s", (i))
#define min(a,b) (((a)<(b))?(a):(b))
#define max(a,b) (((a)>(b))?(a):(b))

typedef struct vector{
    uint sz;
    uint cap;
    void* c;
} vector;

#define vector_ctor(v, TYPE) \
    vector* v=NULL;\
    v = malloc(sizeof(vector));\
    v->sz = 0;\
    v->cap = 5;\
    v->c = malloc(sizeof(TYPE)*(v->cap));

#define vector_push_back(v, TYPE, e)  \
    if(v->sz == v->cap){\
        v->cap = (v->cap)*2;\
        void* new_c = malloc(sizeof(TYPE)*(v->cap));\
        memcpy(new_c, v->c, sizeof(TYPE)*(v->sz));\
        free(v->c);\
        v->c = new_c;\
    }\
    ((TYPE*)(v->c))[v->sz]=(e);\
    v->sz += 1;\

#define vector_at(v, TYPE, i) ( ( (TYPE*)(v->c) )[i] )
// change vector v to c array with name dest
#define vector_to1darray(v, TYPE, dest) \
    TYPE dest[v->sz];\
    memcpy(dest, v->c, sizeof(dest));\

// change vector v to 2d c array with name dest
#define vector_to2darray(v, TYPE, dest) \
    uint maxCol##dest = INT_MAX;\
    for(int i=0;i<v->sz;i++){\
        maxCol##dest=min(maxCol##dest, vector_at(v,vector*,i)->sz);\
    }\
    TYPE dest[v->sz][maxCol##dest];\
    for(int i=0;i<v->sz;i++){\
        vector* row = vector_at(v,vector*,i);\
        for(int j=0;j<row->sz;j++){\
            dest[i][j] = vector_at(row,TYPE,j);\
        }\
    }\