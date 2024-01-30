#lang forge
open "elevator.frg" --- import elevator procedures

--------------------------------------------------------------------------------
-- Q. Download and run the elevator simulation:
--    <https://fmv.jku.at/elsim/>
--    Find a way to make the simple controller move while the door is open.
--    Explain how to reproduce this safety violation (for example, with short
--    click-by-click instructions).
-- A. In the simple controller mode, the moment the elevator door just opens at Floor #n, clicking   
--    for any floor below Floor #n will make the elevator go down while the door is open.  
--    However, this safety violation doesn't happen if clicking for 
--    any floor above Floor #n while the elevator is in Fllor #n, is done.
--    How to reproduce: Run the elevator -> click 'go' button -> click Floor #3 ->
--                      click Floor #2 the moment the elevator door opens at Floor #3 
-- 

--------------------------------------------------------------------------------
-- Q. What is liveness and in what way is it important to an elevator?
-- A. Liveness properties guarantee that a favorable outcome will ultimately occur. 
-- For instance, in a mutual exclusion algorithm, the liveness property guarantees 
-- that attempts to enter and leave the critical section will be successful after some time. 
-- This suggests that the system is free from deadlock and starvation.
-- 
-- In case of an elevator system, liveness ensures that the elevator does not get 
-- stuck indefinitely at a particular floor or in between floors, eventually avoiding deadlocks. 
-- Another liveness property ensures that every request is eventually serviced. That means if a call 
-- button is pressed on any floor, the elevator will eventually arrive at that floor to serve the request.
-- Yet another liveness property ensures that the elevator does not move while the door is open.

--------------------------------------------------------------------------------
-- Q. Write your own names and documentation for the 5 mystery procedures in
--    elevator.frg. The documentation can be as short as 1 sentence per
--    procedure, but it **must** bring across how each procedure is unique.
--    You may find it helpful to experiment with the (optional) properties
--    at the bottom of this file. You may explain with examples.

-- A. [procedure1]
--  Name of procedure1: ManageBasicElevatorOperations
--  This ensures that the elevator stays put when there are no pending requests and 
--  performs pickups on the current floor as required. The method smartly avoids ascending 
--  if there are outstanding requests on the floors below and similarly avoids descending 
--  when there are no requests on the lower floors.

-- procedure2
--  Name of procedure2: EndToEndVerticalCycle
--  This procedure represents a unique operational model emphasizing relentless movement and systematic coverage 
--  of all floors. Distinct from conventional elevator logic that responds reactively to requests, this procedure 
--  mandates continuous movement between the building's extremes - the top and bottom floors - without ever remaining stationary.
--  This relentless vertical traversal ensures that the elevator visits every floor in a cyclic manner, offering a 
--  predictable pattern that could be particularly efficient in buildings with evenly distributed and constant traffic.

-- procedure3
--  Name of procedure3: EfficientDirectionalScheduling
--  The procedure enforces that the elevator will not stay still if there are pending requests, ensuring 
--  continuous operation until all requests are addressed. The elevator always picks up passengers from the 
--  current floor if there are requests there, maximizing immediate service responsiveness.
--  It's unique because This strategy minimizes unnecessary travel, as the elevator systematically clears 
--  requests in one direction before reversing, leading to time and energy efficiency, especially in scenarios 
--  with clustered requests over certain floors.

-- procedure4
--  Name of procedure4: FocusedRequestNavigation
--  This procedure centralizes the concept of a nextRequest to guide the elevator's actions.
--  The elevator remains stationary only if there are no requests, prioritizing movement otherwise. 
--  It consistently services the current floor if there is a request, ensuring immediate responsiveness. 
--  The distinctive aspect of this procedure lies in its handling of the nextRequest: the elevator moves 
--  exclusively upwards if the nextRequest is above, and conversely, only downwards if it's below, until the request is fulfilled. 
--  Additionally, it incorporates a mechanism to handle transitions from a state of no requests to receiving new ones, 
--  ensuring that the nextRequest is always relevant and up-to-date.

-- procedure5
--  Name of procedure5: DynamicRequestResponseStrategy
--  To put procedure5 in forge/temporal language, we can say { procedure4 implies procedure5 }
--  So, In addition to doing what procedure4 does, the procedure5 does a strategic decision-making mechanism when choosing a new nextRequest: 
--  if the elevator is already moving upwards and a new request is made, it prioritizes requests on the higher floors; 
--  conversely, if moving downwards, it favors lower floor requests.
--  This adaptive strategy is particularly effective in scenarios where passenger requests are not uniformly distributed across floors, 
--  allowing the elevator to serve the most logical and immediate requests based on its current trajectory.


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

-- I added a new sfety property predicate and test case for this
// Safety property: Don't move when the door is open

pred elevatorNotMoveWhenDoorOpened[e: Elevator] {
  e.door = Open  => e.floor = e.floor'
}

test expect {
  -- test basic properties here
  test2: {traces implies elevatorNotMoveWhenDoorOpened[Elevator]} for exactly 1 Elevator is theorem
}


// property: forward progress is always possible
pred forwardProgress[e: Elevator] {
  always eventually enabled[e]
}

-- I added a test for forwardProgress predicate
test expect {
  -- test basic properties here
  test3: {traces implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
}


// Liveness property: every request for every elevator is eventually served
pred everyonePickedUp[e: Elevator] {
  always { 
    all f: Floor | f in e.requests => eventually {f not in e.requests}
  }
}

-- added a test case for testing everyonePickedUp predicate
test expect {
  -- testing Liveness property: everyonePickedUp
  test4: {traces and always everyonePickedUp[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
}

// property: the elevator only moves up/down if there are
// requests above/below it (no pointless trips)
pred noPointlessTrips[e: Elevator] {
  always {moveDown[e] => some (e.floor.^below & e.requests)}
  always {moveUp[e] => some (e.floor.^above & e.requests)}
}

-- added a test case for testing noPointlessTrips predicate
test expect {
  -- testing Liveness property: noPointlessTrips
  test5: {traces and always noPointlessTrips[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
}

// property: a request may exist above and below the elevator
pred canRequestAboveAndBelow[e: Elevator] {
  eventually {
    some (e.requests & e.floor.^below)
    some (e.requests & e.floor.^above)
  }
}

-- added a test case for testing canRequestAboveAndBelow predicate
test expect {
  -- testing Liveness property: canRequestAboveAndBelow
  test6: {traces and always canRequestAboveAndBelow[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
}

// I added a propoerty:: a request may exist Top and Bottom of the elevator
pred canRequestTopAndBottom[e: Elevator] {
  eventually {
    some (e.requests & Top)
    some (e.requests & Bottom)
  }
}

-- added a test case for testing canRequestTopAndBottom predicate
test expect {
  -- testing property: canRequestTopAndBottom
  test7: {traces and always canRequestTopAndBottom[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
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


-- Here is the predicate that catches relationship between procedure4 and procedure5
pred EfficientProcedureRelationship[e: Elevator] {
  -- Check if procedure4 is true then procedure5 should also be true
  (procedure4[e] implies procedure5[e])
  
  -- Check if procedure5 leads to forwardProgress
  (procedure5[e] implies forwardProgress[e])
}

test expect {
  fp6: {traces and always EfficientProcedureRelationship[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
}

-- The following one combines strategies from both procedure3 and procedure2
-- This new predicate could be structured to prioritize the movement logic of 
-- procedure3 (which is more responsive to the location of requests) 
-- while ensuring the continuous operation from procedure2 is respected

pred HybridElevatorOperation[e: Elevator] {
  -- Incorporate request-based movement from procedure3
  procedure3[e]

  -- Apply continuous movement logic from procedure2 when no specific requests dictate movement
  no e.requests implies procedure2[e]

  -- Optional: Add any additional specific conditions or optimizations that combine elements from both procedures
  -- Example condition: Ensure the elevator moves in the direction of the majority of requests if idle
}


test expect {
  fp7: {traces and always HybridElevatorOperation[Elevator] implies forwardProgress[Elevator]} for exactly 1 Elevator is theorem
}
