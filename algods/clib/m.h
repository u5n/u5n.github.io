/* 2021.5.15
support c++14
g++ -O2 -std=gnu++17 -Wall -Wno-sign-compare mycpp.cpp -o mycpp -fsanitize=address 
*/
#pragma GCC optimize ("O3")
#include <bits/stdc++.h>
using namespace std;
// meta
    // alias a class method
    #define FUNCTIONAMEQ(highLevelF, lowLevelF) \
    template<typename... Args> \
    inline auto highLevelF(Args&&... args) -> decltype(lowLevelF(forward<Args>(args)...)) \
    {return lowLevelF(forward<Args>(args)...);}
// abbr
    using int64 = long long;
    using vi = vector<int>;
    using vvi = vector<vi>;
    using pii = pair<int, int>;
    #define fi first
    #define se second
    #define all(x) begin(x),end(x)
    #define rall(x) rbegin(x),rend(x) //c++14

//len->size
    #if __cplusplus >= 201703L
        #define len(x) size(x)
    #else
        #define len(x) (x.size())
    #endif
//range->rep
    #define GET_MACRO(_0,_1,_2,_3,_N,...) _N
    #define rep(...)  GET_MACRO(__VA_ARGS__,X,rep3,rep2,rep1)(__VA_ARGS__)
    #define rep3(i,a,b) for(int i=(a),_5=(b);i<_5;++i)
    #define rep2(i,b) rep3(i,0,b)
    #define rep1(b) rep2(_,b)
    /*
        need _5, otherwise, for(int i=-2;i<v.size();i++) equals to
        for(int i = -2; static_cast<unsigned long>(i) < v.size(); i++) 
    */

/* algorithm boost*/
    #if __cplusplus <= 201703L
        #define gcd __gcd
        #define lcm(x,y) (x/gcd(x,y)*y)
    #endif
    //pow->powmod(a,b,mod) # Fast Power Algo
        inline int64 powmod(int64 a,int64 b,int64 mod) 
        {
            a%=mod;
            int64 res=1;
            while(b){
                if(b&1) 
                    res=res*a%mod;
                a=a*a%mod;
                b>>=1;
            }
            return res;
        }	     
    // matrix powmod
        #define vvt vector<vector<T>>
        template<class T>
        vvt mat_mulmod(vvt& matL, vvt& matR, int64 mod){
            auto m=len(matL),n=len(matR),p=len(matR[0]);
            vvt ret(m, vector<T>(p, 0));
            rep(i,m) rep(j,p) {
                T val = 0;
                rep(k,n) {
                    val = (val+matL[i][k]*matR[k][j])%mod;
                }
                ret[i][j] = val;
            }
            return ret;
        }
        template<class T>
        vvt mat_powmod(vvt& mat, int64 b, int64 mod){
            auto n = len(mat);
            vvt ret(n, vector<T>(n, 0));
            rep(i,n) ret[i][i] = 1;
            while(b){
                if(b%2) 
                    ret = mat_mulmod(ret, mat, mod);
                mat = mat_mulmod(mat, mat, mod);
                b>>=1;
            }
            return ret;
        }
/* opreator */
    /* 1d math vector operator
        vector v , const c
        v+v ; v+c ; v*c ; v*v ; and *= ,+= 
    */
        template<class T>
        vector<T> operator+(const vector<T>& l,const vector<T>& r){
            vector<T> res(l);
            rep(i,len(r)) res[i]+=r[i];
            return res;
        }
        template<class T,class R>
        vector<T> operator+(const vector<T>& l,const R& r){
            vector<T> res(l);
            rep(i,len(res)) res[i]+=r;
            return res;
        }
        template<class T>
        vector<T> operator*(const vector<T>& l,const vector<T>& r){
            vector<T> res(l);
            rep(i,len(r)) res[i]*=r[i];
            return res;
        }
        template<class T,class R>
        vector<T> operator*(const vector<T>& l,const R& r){
            vector<T> res(l);
            rep(i,len(res)) res[i]*=r;
            return res;
        }

        template<class T>
        void operator+=(vector<T>& res,const vector<T>& r)
        {rep(i,len(r)) res[i]+=r[i];}
        template<class T,class R>
        void operator+=(vector<T>& res,const R& r)
        {rep(i,len(res)) res[i]+=r;}
        template<class T>
        void operator*=(vector<T>& res,const vector<T>& r)
        {rep(i,len(r)) res[i]*=r[i];}
        template<class T,class R>
        void operator*=(vector<T>& res,const R& r)
        {rep(i,len(res)) res[i]*=r;}
    
    /* string operator 
        += int ,* int
    */
        string operator*(const string& s, int rhs) {
            if(rhs==1){return s;}
            else{
                string s2(s);
                rep(rhs-1) s2+=(s);
                return s2;
            }
        }
        void operator+=(string&l, int r){
            if(r<=9){l.push_back(r+48);return;}
            else{
                int digits=pow(10,int(log10(r)));
                while(digits){
                    int quotient=r/digits;
                    l.push_back(quotient+48);
                    r-=quotient*digits;
                    digits/=10;
                }
            }
        }

//pre set
    #define type(...) (type_map[typeid(__VA_ARGS__)])
    unordered_map<type_index, string> type_map;
    int __mystery = []() {
        /* io accelerater */
        ios::sync_with_stdio(0);cin.tie(0);
        /* type */
        type_map[typeid(bool)]="bool";
        type_map[typeid(int)]="int";
        type_map[typeid(float)]="float";
        type_map[typeid(long)]="long";
        type_map[typeid(long long)]="longlong";
        type_map[typeid(unsigned int)]="uint";
        type_map[typeid(unsigned long)]="ulong"; // size_t 
        type_map[typeid(double)]="double";
        type_map[typeid(pair<int,int>)]="pair<int,int>";
        type_map[typeid(string)]="string";
        type_map[typeid(vector<int>)]="vector<int>";
        type_map[typeid(initializer_list<int>)]="vector<int>";
        type_map[typeid(set<int>)]="set<int>";
        type_map[typeid(vector<string>)]="vector<string>";
        type_map[typeid(unordered_map<int,int>)]="unordered_map<int,int>";
        return 42;
    }();

/* debug online judge */
    #ifndef ONLINE_JUDGE
    // common use D,D1(:firstN),D1(start,end),D2([:row[,:col]]),Dmap
    // arbitary size c arr e.g.
    //     N is not const 
    //     int a[N] use Da(a,N)
    //     int a[N][M] use Da(a,N,M)

    // cpp like for_each(begin(s),end(s),[](int&n){}), adding used here only keep code logic clean
        #define for_iter(i, s) for(auto i=begin(s);i!=end(s);i++)
        #define for_iter_n(i, s, n) for(auto i=begin(s),_6=next(begin(s),n);i!=_6;++i)
    // print element with separator
        template<class T>
        inline void D0(const T& x, string sep=", "){
            if(type(x)=="string") cout<<'"'<<x<<'"'<<sep;
            else if(type(x)=="char") cout<<'\''<<x<<'\''<<sep;
            else cout<<x<<sep;
        }
    //print single element, arbitary args
        #define D(...) {cout<<#__VA_ARGS__<<'\t';Dout(__VA_ARGS__);cout<<'\n';};
            inline void Dout(){cout<<'\n';}
            template<class T>
            inline void Dout(const T& h){D0(h,"");}
            template<class T,class... U>
            inline void Dout(const T& h,const U&... t){D0(h);Dout(t...);}
    //1d container supporting iterator
        #define D1(...)  {cout<<#__VA_ARGS__<<"\t{";GET_MACRO(__VA_ARGS__,X,Dvec2,Dvec1,Ds)(__VA_ARGS__);cout<<"}\n";}
            #define Ds(...) for(const auto &__e : __VA_ARGS__ ) D0(__e); // use ... for initializer_list<>
            #define Dvec1(x,fir) {for_iter_n(_7,x,fir) D0(*_7);}
            #define Dvec2(x,fir,sec) {for(auto _9=begin(x),_6=next(_9,sec),_7=next(_9,fir);_7!=_6;_7++) D0(*_7);}
    //2d container supporting iterator
        #define D2(...)  {cout<<#__VA_ARGS__<<"\n{\n";GET_MACRO(__VA_ARGS__,X,Da2,Dv2,Ds2)(__VA_ARGS__);cout<<"}\n";}
            #define Ds2(x) for(auto const& e:x) {cout<<"    {";Ds(e); cout<<"},\n";}
            #define Dv2(x,fir) for_iter_n(_8,x,fir) {cout<<"    {";Ds(*_8); cout<<"},\n";}
            #define Da2(x,fir,sec) rep(__i,fir) {cout<<"    {";Darr1(x[__i],sec);cout<<"},\n";}
    // 1d or 2d arr using "For loop"
        #define Da(...)  {cout<<#__VA_ARGS__<<"\t{";GET_MACRO(__VA_ARGS__,X,Darr2,Darr1,Dmap)(__VA_ARGS__);cout<<"}\n";}
            #define Darr1(x,s)  {rep(__j,s) D0(x[__j]);}
            #define Darr2(x,s,e)  {rep(__j,s,e) D0(x[__j]);}
    // map and vector<pair<int,int>>
        #define Dmap(mp) for(auto const& p:mp){D0(p.fi,": ");D0(p.se);}
    #endif