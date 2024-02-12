#lang forge/bsl

sig Process {
  id : one Int,
  successor : one Process,  --- successor is a table mapping one Process to another Process
  highestId : pfunc State -> Int
  -- func is a total function
}

sig State {}

one sig Election {
  initial : one State,          --- the start state (though we need constraints to make it so)
  next : pfunc State -> State   --- sequence of states, modeled as a function
}

// run {
//   }
//   for exactly 3 Process, 4 State
//   for { next is linear } -- linear 
// comment out old runs,
//  otherwise you need to click enter to skip their Sterling windows

pred wellformed {
  -- every process can reach every other via
  --  successor
  -- HINT: reachable[a, b, f]
  --  can get to a from b using f each step
  all p0, p1 : Process {
    reachable[p1, p0, successor]
  }

  -- every process has ID >= 0
  all p : Process | p.id >= 0

  -- every process has highestID >= ID
  all p : Process {
   all s : State {
     p.highestId[s] >= p.id
  }}

  -- every process has unique ID
  -- lone ... given an int, there's at most
  --  one process with that int as the id
  all num : Int {
    lone p : Process {
      p.id = num
    } }

}

// run { wellformed }
//   for exactly 3 Process, 4 State
//   for { next is linear }

pred init[t : State] {
  -- for all Process, highestId = id
  all p : Process | p.id = p.highestId[t]
}

pred winningAfter[t : State, p : Process] {
  -- what property holds just before
  --  a process gets its ID back?
  some p0 : Process {
    p0.successor = p
    p0.highestId[t] = p.id
  }
}

pred step[t1, t2 : State] {
  -- t1 happens before t2, how can they differ?
  -- every process updates their highest
  --  (if it was lower than the incoming)
  all p0 : Process {
    let p1 = p0.successor |
    let id0 = p0.highestId[t1] |
    let id1 = p1.highestId[t1] |
    (id0 >= id1) => {
      p1.highestId[t2] = id0
    } else {
      p1.highestId[t2] = id1
    }
  }
}

pred traces {
  wellformed

  -- Election.initial is a valid init state
  init[Election.initial]

  -- nothing comes before the init state
  no prev : State {
    Election.next[prev] = Election.initial
  }

  -- when t has a next state, then the two are related by step
  all t : State {
    (some Election.next[t]) => step[t, Election.next[t]]
  }
}

-- Q. why do we need show?
--    we already have traces!
-- A. traces doesn't require a winning state
pred show {
  traces
  some p: Process, t: State {
    winningAfter[t,p]
  }
}

run {show} for exactly 3 Process, 5 State
 for { next is linear }


