predicate sorted (a: array<int>)
	requires a != null
	reads a
{
	sorted'(a, a.Length)
}

predicate sorted' (a: array<int>, i: int)
	requires a != null
	requires 0 <= i <= a.Length
	reads a
{
	forall k :: 0 < k < i ==> a[k-1] <= a[k]
}

method FindMin (a: array<int>, i: int) returns (m: int)
	requires a != null
	requires 0 <= i < a.Length
	ensures i <= m < a.Length
	ensures forall k :: i <= k < a.Length ==> a[k] >= a[m]
{
	var j := i;
	m := i;
	while(j < a.Length)
		invariant i <= j <= a.Length
		invariant i <= m < a.Length
		invariant forall k :: i <= k < j ==> a[k] >= a[m]
		decreases a.Length - j
	{
		if(a[j] < a[m]) { m := j; }
		j := j + 1;
	}
}

method InsertionSort (a: array<int>)
	requires a != null
	modifies a
	ensures sorted(a)
{
	var c := 0;
	while(c < a.Length)
		invariant 0 <= c <= a.Length
		invariant forall k, l :: 0 <= k < c <= l < a.Length ==> a[k] <= a[l]
		invariant sorted'(a, c)
	{
		var m := FindMin(a, c);
		a[m], a[c] := a[c], a[m];
		//assert forall k :: c <= k < a.Length ==> a[k] >= a[c];
		c := c + 1;
	}
}