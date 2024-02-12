method mergesort(L:array<int>)
requires L != null
modifies L
{
    sort(L, 0, L.Length-1);

   
    
}

method merge(L:array<int>, lo:int, mid:int, hi:int)
requires L!=null;
requires lo <= mid <= hi;
requires 0 <= lo <= L.Length;
requires 0 <= mid <= L.Length;
requires 0 <= hi <= L.Length;
modifies L;

{
    var L1:array<int>, L2:array<int> := new int[mid - lo + 1], new int[hi - mid];
    var i, j, k := 0, 0, 0;
    
    while( j<L1.Length && lo+j<L.Length )
    decreases L1.Length-j
    invariant 0<=j<=L1.Length
    invariant 0<=lo+j<=L.Length
    {
        L1[j] := L[lo+j];
        j := j +1;
    }
    while( k<L2.Length && mid+k+1<L.Length )
    decreases L2.Length-k
    invariant 0<=k<=L2.Length
    invariant 0<=mid+k<=L.Length
    {
        L2[k] := L[mid+k+1];
        k := k +1;
    }
    
    j, k := 0, 0;
    while (i < hi - lo + 1 && j <= L1.Length && k <= L2.Length && lo+i < L.Length)
    decreases hi - lo - i
    invariant 0 <= i <= hi - lo + 1
    {
        if(j >= L1.Length && k >= L2.Length){
            break;
        }
        else if(j >= L1.Length){
            L[lo+i] := L2[k];
            k := k+1;
        }else if(k >= L2.Length){
            L[lo+i] := L1[j];
            j := j+1;
        }else{
            if(L1[j] <= L2[k]){
                L[lo+i] := L1[j];
                j := j +1;
            }else if(L1[j] > L2[k]){
                L[lo+i] := L2[k];
                k := k +1;
            }
        }
        i := i+1;
    }
    
    
}

method sort(L:array<int>, lo:int, hi:int) 
decreases hi - lo
requires L != null
requires lo >= 0 && hi <= L.Length;
modifies L

{
    if (lo < hi){
        var mid : int := lo + (hi - lo)/2;
        sort(L, lo, mid);
        sort(L, mid+1, hi);
        merge(L, lo, mid, hi);        
    }

    
}