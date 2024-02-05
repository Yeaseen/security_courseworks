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
ensures forall i :: 0 <= i < l || (i > u && i < a1.Length) ==> a[i] == a1[i]
ensures forall i1, i2:: l <= i1 < i2 <= u ==> a[i1] <= a[i2]
{
  a := new int[a1.Length];
  //assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];

  var k := 0;
  while (k < a1.Length)
    invariant 0 <= k <= a1.Length // Loop invariant for index bound.
    invariant forall j :: 0 <= j < k ==> a[j] == a1[j] // Elements up to 'k' are copied correctly.
    decreases a1.Length - k // Decreases clause for termination.
  {
    a[k] := a1[k];
    k := k + 1;
  }
  assert forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];
  if (l >= u)
  {
    return a;
  }
  else
  {
    var m:int := (l + u) / 2;

    a := ms(a, l, m);
    assert forall i1, i2 :: l <= i1 < i2 <= m ==> a[i1] <= a[i2];
    assert forall i :: (i > u && i < a1.Length) ==> a[i] == a1[i];
    a := ms(a, m+1, u);
    
    assert forall i :: 0 <= i < l ==> a[i] == a1[i];
    assert forall i1, i2 :: l <= i1 < i2 <= m ==> a[i1] <= a[i2];
    assert forall i1, i2 :: m+1 <= i1 < i2 <= u ==> a[i1] <= a[i2];
     
    
    a := merge(a, l, m, u);
    assert forall i1, i2 :: l <= i1 < i2 <= u ==> a[i1] <= a[i2];
    return a;
  }
}

method merge(a1: array<int>, l: int, m: int, u: int) returns (a: array<int>)
  requires 0 <= l <= m < u < a1.Length
  requires forall i1, i2 :: l <= i1 < i2 <= m ==> a1[i1] <= a1[i2]
  requires forall i1, i2 :: m+1 <= i1 < i2 <= u ==> a1[i1] <= a1[i2]
  
  ensures a1.Length == a.Length
  ensures forall i :: 0 <= i < l || (i > u && i < a1.Length) ==> a[i] == a1[i]
  ensures forall i1, i2 :: l <= i1 < i2 <= u ==> a[i1] <= a[i2]
{
   a := new int[a1.Length];
  //assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];

  var p := 0;
  while (p < a1.Length)
    invariant 0 <= p <= a1.Length // Loop invariant for index bound.
    invariant forall j :: 0 <= j < p ==> a[j] == a1[j] // Elements up to 'k' are copied correctly.
    decreases a1.Length - p // Decreases clause for termination.
  {
    a[p] := a1[p];
    p := p + 1;
  }
  assert forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];

  var buf := new int[u-l+1];
  var i: int := l;
  var j: int := m + 1;
  var k: int := 0;

   

  while (k < u-l+1)
  decreases u-l+1-k
  invariant l <= m < u
  invariant 0 <= k <= u-l+1
  invariant 0 <= l <= m < u < a.Length
  invariant forall i1, i2 :: l <= i1 < i2 <= m ==> a[i1] <= a[i2]
  invariant forall i1, i2 :: m+1 <= i1 < i2 <= u ==> a[i1] <= a[i2]
  invariant forall i :: 0 <= i < l || (i > u && i < a1.Length) ==> a[i] == a1[i]
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
  //assert 0<=k<=u-l+1;
  //assert forall i1, i2 :: 0 <= i1 < i2 < u-l+1 ==> buf[i1] <= buf[i2];

  k := 0;
  while (k < u-l+1)
  decreases u-l+1-k
  invariant l <= m < u
  invariant 0 <= k <= u-l+1
  invariant forall i :: 0 <= i < l || (i > u && i < a1.Length) ==> a[i] == a1[i]
  {
    a[l + k] := buf[k];
    k := k + 1;
  }
  
  //assert forall i1, i2 :: l <= i1 < i2 <= u ==> a[i1] <= a[i2];
}