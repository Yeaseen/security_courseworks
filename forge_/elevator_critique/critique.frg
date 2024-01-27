#lang forge
open "elevator.frg" --- import elevator procedures

--------------------------------------------------------------------------------
-- Q. Download and run the elevator simulation:
--    <https://fmv.jku.at/elsim/>
--    Find a way to make the simple controller move while the door is open.
--    Explain how to reproduce this safety violation (for example, with short
--    click-by-click instructions).
-- A. TODO fill in here
--  (add more lines if you need)
-- 
-- 

--------------------------------------------------------------------------------
-- Q. What is liveness and in what way is it important to an elevator?
-- A. TODO fill in here
--  (add more lines if you need)
-- 
-- 

--------------------------------------------------------------------------------
-- Q. Write your own names and documentation for the 5 mystery procedures in
--    elevator.frg. The documentation can be as short as 1 sentence per
--    procedure, but it **must** bring across how each procedure is unique.
--    You may find it helpful to experiment with the (optional) properties
--    at the bottom of this file. You may explain with examples.

-- A. [procedure1]
--  TODO give a descriptive name and documentation
--  (add more lines if you need)
-- 
-- 
-- 
-- 

-- procedure2
--  TODO give a descriptive name and documentation
--  (add more lines if you need)
-- 
-- 
-- 
-- 

-- procedure3
--  TODO give a descriptive name and documentation
--  (add more lines if you need)
-- 
-- 
-- 
-- 

-- procedure4
--  TODO give a descriptive name and documentation
--  (add more lines if you need)
-- 
-- 
-- 
-- 

-- procedure5
--  TODO give a descriptive name and documentation
--  (add more lines if you need)
-- 
-- 
-- 
-- 


--------------------------------------------------------------------------------
-- OPTIONAL: model properties and verification
--  You may find it helpful to write tests below. Use the preds we provide or
--  write your own. Same goes for the test expect blocks; you can extend the
--  ones we provide or write your own. This part of the file will not be
--  graded. It is scratch space for learning how the elevator procedures work.

// Safety property: move only when door is closed
pred elevatorOnlyMoveWhenDoorClosed[e: Elevator] {
  e.floor != e.floor' => e.door = Closed
}

test expect {
  -- test basic properties here
  test1: {traces implies elevatorOnlyMoveWhenDoorClosed[Elevator]} for exactly 1 Elevator is theorem
}

// property: forward progress is always possible
pred forwardProgress[e: Elevator] {
  always eventually enabled[e]
}

// Liveness property: every request for every elevator is eventually served
pred everyonePickedUp[e: Elevator] {
  always { 
    all f: Floor | f in e.requests => eventually {f not in e.requests}
  }
}

// property: the elevator only moves up/down if there are
// requests above/below it (no pointless trips)
pred noPointlessTrips[e: Elevator] {
  always {moveDown[e] => some (e.floor.^below & e.requests)}
  always {moveUp[e] => some (e.floor.^above & e.requests)}
}

// property: a request may exist above and below the elevator
pred canRequestAboveAndBelow[e: Elevator] {
  eventually {
    some (e.requests & e.floor.^below)
    some (e.requests & e.floor.^above)
  }
}

test expect {
  -- procedure1
  fp1: {traces and always procedure1[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem

}

test expect {
  -- procedure2
  fp2: {traces and always procedure2[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem

}

test expect {
  -- procedure3
  fp3: {traces and always procedure3[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem

}

test expect {
  -- procedure4
  fp4: {traces and always procedure4[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem

}

test expect {
  -- procedure5
  fp5: {traces and always procedure5[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem

}


