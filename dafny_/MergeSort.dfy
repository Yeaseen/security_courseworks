method MergeSort(a1:array<int>) returns (a:array<int>)
  requires a1.Length > 0;
  ensures a != null;
  ensures forall k:: forall l:: 0 <= k < l < a.Length ==> a[k] <= a[l];
{
  a := ms(a1, 0, a1.Length-1);
  return;
}
 
method ms(a1:array<int>, l:int, u:int) returns (a:array<int>)
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

method merge(a1:array<int>, l:int, m:int, u:int) returns (a:array<int>)
{
  a := new int[a1.Length];
  assume forall k:: 0 <= k < a1.Length ==> a[k] == a1[k];
  var buf := new int[u-l+1];
  var i:int := l;
  var j:int := m + 1;
  var k:int := 0;

  while (k < u-l+1)
  {
    if (i > m)
    {
      buf[k] := a[j];
      j := j + 1;
    }
    else if (j > u)
    {
      buf[k] := a[i];
      i := i + 1;
    }
    else if (a[i] <= a[j])
    {
      buf[k] := a[i];
      i := i + 1;
    }
    else
    {
      buf[k] := a[j];
      j := j + 1;
    }
    k := k + 1;
  }

  k := 0;
  while (k < u-l+1)
  {
    a[l + k] := buf[k];
    k := k + 1;
  }
}

