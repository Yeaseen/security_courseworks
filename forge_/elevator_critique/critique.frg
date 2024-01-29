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
--  It ensures the elevator remains stationary if there are no requests and engages in pickup at the current 
--  floor if needed. The procedure intelligently decides against moving upwards if there are pending requests on 
--  lower floors and refrains from moving downwards in the absence of lower floor requests.
-- 

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
--  To put procedure5 in forge/temporal language, we can say { procedure4 in procedure5 }
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


