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

ensures a1.Length == a.Length // input and output lengths must be same
ensures forall i :: 0 <= i <= l-1 ==> a[i] == a1[i] // [0..l-1] shoudn't change 
ensures forall i :: u+1 <= i < a.Length ==> a[i] == a1[i] //[u+1..a.Length-1] shouldn't change
ensures forall i1:: forall i2:: l <= i1 < i2 <= u ==> a[i1] <= a[i2] // output array [l..] sorted 
{
  a := new int[a1.Length];
  assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];
  if (l >= u)
  {
    return;
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
  requires 0 <= l <= m < u < a1.Length
  requires forall i1, i2 :: l <= i1 < i2 <= m ==> a1[i1] <= a1[i2] //input array [l..m] should be sorted
  requires forall i1, i2 :: m+1 <= i1 < i2 <= u ==> a1[i1] <= a1[i2] ////input array [m+1..u] should be sorted
  
  
  ensures a1.Length == a.Length // input and output lengths must be same 
  ensures forall i1, i2 :: l <= i1 < i2 <= u ==> a[i1] <= a[i2] //output array[l..u] sorted
  ensures forall i :: 0 <= i <= l-1 ==> a[i] == a1[i] //[u+1..a.Length-1] shouldn't change
  ensures forall i :: u+1 <= i < a.Length ==> a[i] == a1[i] // output array [l..] sorted
{
  a := new int[a1.Length];
  assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];
  var buf := new int[u-l+1];
  var i: int := l;
  var j: int := m + 1;
  var k: int := 0;

  
  while(k < u-l+1)
  decreases u-l+1-k
  invariant 0 <= l <= m < u < a1.Length
  invariant 0 <= k <= u-l+1
  invariant l <= i <= m+1
  invariant m+1 <= j <= u+1
  invariant k == (i - l) + (j - (m + 1)) // k = #of items picked from [l...m] + #of items picked from [m+1...u]
  
  invariant ( i>m && j<=u ) ==> forall i1, i2 :: (l<= i1 <i && j <= i2 <=u) ==> a[i1] <= a[i2] //it should be supported by precondition + my first if case
  invariant ( j>u && i<=m ) ==> forall i1, i2 :: (i<= i1 <=m && m+1 <= i2 <j) ==> a[i2] <= a[i1] // same as above
  
  invariant forall i :: 0 <= i <= l-1 ==> a[i] == a1[i] //precondition
  invariant forall i :: u+1 <= i < a.Length ==> a[i] == a1[i] //precondition
  
  invariant forall i1, i2 :: l <= i1 < i2 <= m ==> a[i1] <= a[i2] //precondition
  invariant forall i1, i2 :: m+1 <= i1 < i2 <= u ==> a[i1] <= a[i2] //precondition
  invariant (k>0 && i<=m) ==> forall k1:: 0 <= k1 <k ==> a[i] >= buf[k1]
  invariant (k>0 && j<=u) ==> forall k1:: 0 <= k1 < k ==> a[j] >= buf[k1] 
  invariant forall i1, i2:: 0 <= i1 < i2 < k ==> buf[i1] <= buf[i2] //after putting the asserts, i think for some good k buf will remain sorted
  {
    
    //if(i>m && j>u){
      //assert k > 0 ==> buf[k-1] <= buf[k];
      //break;
    //}
    if (i > m ) { 
      buf[k] := a[j];
      assert buf[k] == a[j];
      //assert k > 0 ==> buf[k-1] <= buf[k];
      j := j + 1;
      
      assert m+1 <= j <= u+1;
      
    }
    else if (j > u ) {
      buf[k] := a[i];
      assert buf[k] == a[i];
      i := i + 1;
      assert forall i1, i2 :: 0 <= i1 < i2 < k ==> buf[i1] <= buf[i2];
      assert m+1 <= j <= u+1;
      //assert k > 0 ==> buf[k-1] <= buf[k];
    }
    else if ( a[i] <= a[j]) {
      buf[k] := a[i];
      assert a[i] <= a[j];
      assert buf[k] <= a[i];
      i := i + 1;
      assert m+1 <= j <= u+1;
      assert forall i1, i2 :: 0 <= i1 < i2 < k ==> buf[i1] <= buf[i2];
    }
    else if( a[i] > a[j]) {
      buf[k] := a[j];
      assert a[i] > a[j];
      assert buf[k] == a[j];
      //assert k > 0 ==> buf[k-1] <= buf[k];
      j := j + 1;
      assert m+1 <= j <= u+1;
      assert forall i1, i2 :: 0 <= i1 < i2 < k ==> buf[i1] <= buf[i2];
    }
    
    k := k + 1;
    assert m+1 <= j <= u+1;
    assert forall i1, i2 :: 0 <= i1 < i2 < k-1 ==> buf[i1] <= buf[i2];
    
  }


  k := 0;
  while (k < u-l+1)
  decreases u-l+1-k
  invariant 0 <= l <= m < u <a.Length
  invariant 0 <= k <= u-l+1
  invariant forall i :: 0 <= i <= l-1 ==> a[i] == a1[i] //precondition
  invariant forall i :: u+1 <= i < a.Length ==> a[i] == a1[i] //precondiiton
  
  invariant 1 <= k <= u-l+1 ==> buf[k-1] == a[k+l-1] // for some good k this holds true
  invariant forall i :: 0 <= i < k ==> a[l + i] == buf[i] 
  invariant forall i1, i2:: l <= i1 < i2 < k+l ==> a[i1] <= a[i2]
  invariant forall i1, i2 :: 0 <= i1 < i2 <= u-l ==> buf[i1] <= buf[i2] //i think k needs to be restricted in some way
  
  {
    a[l + k] := buf[k];
    k := k + 1;
  }
}
