//
//  main.cpp
//  Dual_Pri
//
//  Created by GuXiaozhe on 9/3/16.
//  Copyright © 2016 GuXiaozhe. All rights reserved.
//

#include <iostream>
#include <fstream>
#include <string.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

long long int gcdf(int a, int b)
{
    if (b==0) return a;
    return gcdf(b, a % b);
}

long long int findLeastCommonMultiple(int *a, int size) {
    
    long long  int lcm = a[0] * (a[1]/gcdf(a[0], a[1]));
    
    for (int i=2;i<size;i++) {
        lcm = lcm * (a[i]/gcdf(lcm, a[i]));
    }
    
    return lcm;
    
}

using namespace std;

int main(int argc, char* argv[]){
    
    int n=3;
    
    
    int *C=new int[n+1];
    int *T=new int[n+1];
    double *P1=new double[n+1];
    double *P2=new double[n+1];
    double *O=new double[n+1];
    
    T[0]=1;
    
    //WCET, Period, InitialPriority, PromotedPriority, Offset
    
//    C[1]=2;  T[1]=8;  P1[1]=4; P2[1]=1;  O[1]=5;
//    C[2]=9;  T[2]=36; P1[2]=5; P2[2]=2;   O[2]=23;
//    C[3]=31;  T[3]=62; P1[3]=6; P2[3]=3;  O[3]=20;

    C[1]=6;  T[1]=20;  P1[1]=4; P2[1]=1;  O[1]=14;
    C[2]=10;  T[2]=73; P1[2]=5; P2[2]=2;  O[2]=57;
    C[3]=47;  T[3]=84; P1[3]=6; P2[3]=3;  O[3]=40;

    
    unsigned long long int LCM=findLeastCommonMultiple(T, n+1);
//    LCM = 500;
    
    int *sche_dp=new int[LCM];
    int *sche_edf=new int[LCM];
    for(int i=0; i<LCM;i++) {
        sche_dp[i]=-1;
        sche_edf[i]=-1;
    }
    
    double *RQC_dp=new double[n+1];
    double *RQC_edf=new double[n+1];
    double *Release=new double[n+1];
    for(int i=1; i<=n;i++){
        RQC_dp[i]=0;
        RQC_edf[i]=0;
        Release[i]=0;
    }
    int *curr_pri=new int[2*n];
    long long int t=0;
    
    int fail=0;
    char ss[50]="";
    
    while(t<LCM){
        
        //new jobs released at time t and priority promotion at time t
        for(int i=1; i<=n;i++){
            if(t%T[i]==0){
                for(int j=1; j<=n; j++){
                    //				if (RQC_dp[j] != RQC_edf[j]){
                    //					cout<<"!!!Task "<<j<<" has DP remainder "<<RQC_dp[j]<<" and EDF remainder "<<RQC_edf[j]<<" at "<<t<<endl;
                    //				}
                }
                if(RQC_dp[i]>0){ cout<<"!!!Task dp "<<i<<" with "<<RQC_dp[i]<<" misses its deadline at "<<t<<endl;
                    char num[5]="";
                    strcat(ss, "!!! Task ");
                    sprintf(num,"%d",i);
                    strcat(ss, num);
                    strcat(ss, "misses its deadline at time  ");
                    sprintf(num,"%lld",t);
                    strcat(ss, num);
                    
                    fail=1;
                    break;
                }
//                if(RQC_edf[i]>0){ cout<<"!!!Task edf "<<i<<" with "<<RQC_edf[i]<<" misses its deadline at "<<t<<endl;
//                    char num[5]="";
//                    strcat(ss, "!!! Task ");
//                    sprintf(num,"%d",i);
//                    strcat(ss, num);
//                    strcat(ss, "edf misses its deadline at time  ");
//                    sprintf(num,"%lld",t);
//                    strcat(ss, num);
//                    
//                    fail=1;
//                    break;
//                }
                RQC_dp[i]=C[i];
                RQC_edf[i]=C[i];
                Release[i]=t;
                curr_pri[i]=P1[i];
             //   cout<<" Task "<<i<<"  released at time "<<t<<"  V  "<<floor((t/(double)T[i]));
                cout<<"Task "<<i<<"  released at time "<<t<<"  V  "<<floor((t/(double)T[i])) <<endl;
            }
            if(t==floor((t/(double)T[i]))*T[i]+O[i]){
                curr_pri[i]=P2[i];
                cout<<" Task "<<i<<"  is promoted to "<<P2[i]<<" at time "<<t<<"  V  "<<floor((t/(double)T[i]))<<endl;
            }
        }
        
        if(fail) return 0;
        
        //4*n implies very low priority
        int priority=4*n;
        double deadline=2*LCM;
        
        int index_dp=-1;
        int index_edf=-1;
        
        //find highest priority ready task for DP scheduling
        for(int i=1;i<=n;i++){
            if(RQC_dp[i]>0 && curr_pri[i]<priority){
                priority=curr_pri[i];
                index_dp=i;
            }
        }
        
        //find highest priority ready task for EDF scheduling
        for(int i=1;i<=n;i++){
            if(RQC_edf[i]>0 && Release[i]+T[i]<deadline){
                deadline = Release[i]+T[i];
                index_edf=i;
            }
        }
        if(index_dp!=-1){
            RQC_dp[index_dp]--;
            if (RQC_dp[index_dp]==0)
                cout<<"task "<<index_dp<<" is executing in ["<<t<<","<<t+1<<") END_OF_TASK"<<endl;
            else
                cout<<"task "<<index_dp<<" is executing in ["<<t<<","<<t+1<<")"<<endl;
            sche_dp[t]=index_dp;
        }
//        if(index_edf!=-1){
//            RQC_edf[index_edf]--;
//            if (RQC_edf[index_edf]==0)
//                cout<<"                             task "<<index_edf<<" is executing in ["<<t<<","<<t+1<<") END_OF_TASK"<<endl;
//            else
//                cout<<"                             task "<<index_edf<<" is executing in ["<<t<<","<<t+1<<")"<<endl;
//            sche_edf[t]=index_edf;
//        }
        
        t++;
    } //end of while
    return 0;
}