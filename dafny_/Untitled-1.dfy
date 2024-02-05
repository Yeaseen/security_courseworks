method MergeSort(a1:array<int>) returns (a2:array<int>)
  requires a1.Length > 0
  ensures a2 != null
  //ensures forall k:: forall l:: 0 <= k < l < a2.Length ==> a2[k] <= a2[l]
{
  a2 := ms(a1, 0, a1.Length-1);
  return;
}
 

method ms(a1:array<int>, l:int, u:int) returns (a:array<int>)
requires 0 <= l < a1.Length
requires 0 <= u < a1.Length
decreases (u - l)

ensures a1.Length == a.Length
//ensures forall i1:: forall i2::
          //l <= i1 < i2 <= u ==> a[i1] <= a[i2]
{
  a := new int[a1.Length];
  assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];
  if (l >= u)
  {
    return a;
  }
  else
  {
    var m:int := (l + u) / 2;
    a := ms(a, l, m);
    a := ms(a, m+1, u);
    a := merge(a, l, m, u);
    return a;
  }
}

method merge(L:array?<int>, lo:int, mid:int, hi:int) returns (a: array<int>)
requires L!=null;
requires lo <= mid <= hi;
requires 0 <= lo < L.Length;
requires 0 <= mid < L.Length;
requires 0 <= hi < L.Length;

ensures L.Length == a.Length
//ensures forall i1, i2 :: lo <= i1 < i2 <= hi ==> a[i1] <= a[i2]
//modifies L;
{
    a := new int[L.Length];
    var L1:array<int>, L2:array<int> := new int[mid - lo + 1], new int[hi - mid];
    var i, j, k := 0, 0, 0;
    while(j<L1.Length && lo+j<L.Length)
    decreases L1.Length-j;
    invariant 0<=j<=L1.Length;
    invariant 0<=lo+j<=L.Length;{
        L1[j] := L[lo+j];
        j := j +1;
    }
    while(k<L2.Length && mid+k+1<L.Length)
    decreases L2.Length-k;
    invariant 0<=k<=L2.Length;
    invariant 0<=mid+k<=L.Length;
    {
        L2[k] := L[mid+k+1];
        k := k +1;
    }
    j, k := 0, 0;
    while (i < hi - lo + 1 && j <= L1.Length && k <= L2.Length && lo+i < L.Length)
    decreases hi - lo - i;
    invariant 0 <= i <= hi - lo + 1;
    {
        if(j >= L1.Length && k >= L2.Length){
            break;
        }
        else if(j >= L1.Length){
            a[lo+i] := L2[k];
            k := k+1;
        }else if(k >= L2.Length){
            a[lo+i] := L1[j];
            j := j+1;
        }else{
            if(L1[j] <= L2[k]){
                a[lo+i] := L1[j];
                j := j +1;
            }else if(L1[j] > L2[k]){
                a[lo+i] := L2[k];
                k := k +1;
            }
        }
        i := i+1;
    }
}
