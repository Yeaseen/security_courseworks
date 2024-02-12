#lang forge  -- removed bsl and used Relational Forge so that I can use relational oeprators

open "common.frg"

//option verbose 2  --commented out this for getting only the last two lines of output per test case from the test file

abstract sig GWAnimal {}
sig Goat extends GWAnimal {}
sig Wolf extends GWAnimal {}

sig GWState {
    gwnext: lone GWState, --'lone' is also signleton like 'one', but final state doesn't have next state; hence 'lone' 
    gwshore: pfunc GWAnimal -> Position, -- where is every animal?
    gwboat: one Position -- where is the boat?
}

pred GWValidStates {
    // All states must assign a position to every animal and to the boat.
    all s: GWState, a: GWAnimal | {
        one s.gwshore[a]  -- a singleton instance of gwshore in each state to each animal
    }
    all s: GWState {
        one s.gwboat  -- 'one' is for each state's signleton gwboat instance
    }
}

// each of the predicates below should ASSUME valid states
//  they should NOT ENFORCE valid states
// (the `run` command below will enforce it!)

pred GWinitState[s: GWState] {
    // All animals and the boat must start on the near side
    all a: GWAnimal | s.gwshore[a] = Near
    s.gwboat = Near
    // Added one valid and one invalid test cases in the test file

}

pred GWfinalState[s: GWState] {
    // All animals and the boat must end on the far side
    all a: GWAnimal | s.gwshore[a] = Far
    s.gwboat = Far
    // Added one valid and one invalid test cases in the test file
}


pred GWcanTransition[pre: GWState, post: GWState] {
    //the boat must move
    pre.gwboat != post.gwboat

    let movedAnimals = {a: GWAnimal | pre.gwshore[a] != post.gwshore[a]} | {
        // - the boat can carry 1-2 animals (not zero!)
        #movedAnimals > 0 && #movedAnimals <= 2
        // - every other animal stays in the same place
        // used Relational Forge here. It's mentioned in the Documentation of Forge
        all a: GWAnimal | not (a in movedAnimals) => pre.gwshore[a] = post.gwshore[a]
    }
}

pred GWTransitionStates {
    some init, final: GWState {
        GWinitState[init]
        GWfinalState[final]

        // - must be no state before the init state
        no s: GWState | s.gwnext = init
        
        // - must be no state after the final state
        no final.gwnext

        // Every state except the initial state must be reachable from the initial
        all s: GWState | s != init => reachable[s, init, gwnext]

        // - all state transitions must be valid
        all pre: GWState | pre.gwnext != none => GWcanTransition[pre, pre.gwnext]
    }
    // Wrote an invalid test case that should not be in this predicates
    // For a valid one, it will be a mess to write all the valid states and transitions
}


pred GWNeverEating {
    // Never have goats outnumbered by wolves on either side.
    all s: GWState | {
        all p: Position | 
            #({a: Goat | s.gwshore[a] = p}) >= #({a: Wolf | s.gwshore[a] = p})
    }
}

run {
    GWValidStates
    GWTransitionStates
    GWNeverEating
} for exactly 12 GWState,
  exactly 6 GWAnimal,
  exactly 3 Goat,
  exactly 3 Wolf,
  5 Int
  for {gwnext is linear}


// What happens if you change "exactly 12 State" to "11 State"?
// Why do you think that happens?

--Answer to the Question:
// In my opinion, the solver will never find a solution. 
// Sterling will show "UNSAT0" message due to not finding a sloution. (Which it showed, though) 
// Because, theoretically, the total number of states has to be 'EVEN' if the Boat wants to find itself on the other side of the starting Side.
// Possible cases for boat transition: Near -> Far -> Near -> Far
// Near -> Far -> Near -> Far -> Near -> Far
// So, with odd number, if starting state of the Boat is 'Near', the end state of the Boat will also be 'Near'.
// But, the end state of the Boat must be 'Far'. It's possible iff the number of states is "EVEN"
