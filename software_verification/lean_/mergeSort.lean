-- TODO remove the `partial`s and convince Lean that mergeSort terminates

def merge [Ord A] (xs : List A) (ys : List A) : List A :=
  match xs, ys with
  | [], _ => ys
  | _, [] => xs
  | x'::xs', y'::ys' =>
    match Ord.compare x' y' with
    | .lt | .eq => x' :: merge xs' (y' :: ys')
    | .gt => y' :: merge (x'::xs') ys'
--termination_by merge xs ys => xs.length + ys.length -- decreasing length
termination_by merge xs ys => (xs, ys)   -- decreasing

def splitList (lst : List A) : (List A × List A) :=
  match lst with
  | [] => ([], [])  --if list is empty returns a pair of empty lists
  | x :: xs =>    -- else case
    let (a, b) := splitList xs
    (x :: b, a)  --alternation for even splitting

theorem splitList_shorter_le (lst : List α) :
    (splitList lst).fst.length ≤ lst.length ∧ (splitList lst).snd.length ≤ lst.length := by
  induction lst with
  | nil => simp [splitList]
  | cons x xs ih =>
    simp [splitList]
    cases ih
    constructor
    case left => apply Nat.succ_le_succ; assumption
    case right => apply Nat.le_succ_of_le; assumption

theorem splitList_shorter (lst : List α) (_ : lst.length ≥ 2) :
    (splitList lst).fst.length < lst.length ∧
      (splitList lst).snd.length < lst.length := by
  match lst with
  | x :: y :: xs =>
    simp_arith [splitList]
    apply splitList_shorter_le

theorem splitList_shorter_fst (lst : List α) (h : lst.length ≥ 2) :
    (splitList lst).fst.length < lst.length :=
  splitList_shorter lst h |>.left

theorem splitList_shorter_snd (lst : List α) (h : lst.length ≥ 2) :
    (splitList lst).snd.length < lst.length :=
  splitList_shorter lst h |>.right

def mergeSort [Ord A] (xs : List A) : List A :=
  if h : xs.length < 2 then
    match xs with
    | [] => []
    | [x] => [x]
  else
    let halves := splitList xs
    have : xs.length ≥ 2 := by
      apply Nat.ge_of_not_lt
      assumption
    have : halves.fst.length < xs.length := by
      apply splitList_shorter_fst
      assumption
    have : halves.snd.length < xs.length := by
      apply splitList_shorter_snd
      assumption
    merge (mergeSort halves.fst) (mergeSort halves.snd)
termination_by mergeSort xs => xs.length


def sorted (xs : List Nat) : Prop :=
  match xs with
  | [] => True
  | _ :: [] => True
  | x :: y :: xs => x <= y /\ sorted (y :: xs)


#eval mergeSort ["yeaseen", "arafat", "mr", "md"]
#eval mergeSort [44/11, -4, -0, 2*4]


--theorem mergeSort_sorts (xs : List Nat) :
--  sorted (mergeSort xs) := by
--  sorry
