method MergeSort(a1:array<int>) returns (a2:array<int>)
  requires a1.Length > 0
  ensures a2 != null
  ensures forall k:: forall l:: 0 <= k < l < a2.Length ==> a2[k] <= a2[l]
{
  a2 := ms(a1, 0, a1.Length-1);
  return;
}
 

method ms(a1:array<int>, l:int, u:int) returns (a:array<int>)
requires 0 <= l < a1.Length
requires 0 <= u < a1.Length
decreases (u - l)

ensures a1.Length == a.Length
ensures forall i1:: forall i2::
          l <= i1 < i2 <= u ==> a[i1] <= a[i2]
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
    return;
  }
}

method merge(a1: array<int>, l: int, m: int, u: int) returns (a: array<int>)
  requires 0 <= l <= m <= u < a1.Length
  requires forall i1, i2 :: l <= i1 < i2 <= m ==> a1[i1] <= a1[i2]
  requires forall i1, i2 :: m <= i1 < i2 <= u ==> a1[i1] <= a1[i2]
  ensures a1.Length == a.Length
  ensures forall i1, i2 :: l <= i1 < i2 <= u ==> a[i1] <= a[i2]
{
  a := new int[a1.Length];
  assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];
  var buf := new int[u-l+1];
  var i: int := l;
  var j: int := m + 1;
  var k: int := 0;

  
  while (k < u-l+1)
  decreases u-l+1-k
  invariant 0 <= k <= u-l+1
  {
    if(i>m && j>u){
      break;
    }
    else if (i > m) { 
      buf[k] := a[j];
      j := j + 1;
    }
    else if (j > u) {
      buf[k] := a[i];
      i := i + 1;
    }
    else if (a[i] <= a[j]) {
      buf[k] := a[i];
      i := i + 1;
    }
    else {
      buf[k] := a[j];
      j := j + 1;
    }
    k := k + 1;
  }
  k := 0;
  while (k < u-l+1)
  decreases u-l+1-k
  {
    a[l + k] := buf[k];
    k := k + 1;
  }
}
