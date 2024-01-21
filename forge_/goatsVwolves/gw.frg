#lang forge

open "common.frg"
option verbose 2

abstract sig GWAnimal {}
sig Goat extends GWAnimal {}
sig Wolf extends GWAnimal {}

sig GWState {
    gwnext: lone GWState,
    gwshore: pfunc GWAnimal -> Position, -- where is every animal?
    gwboat: one Position -- where is the boat?
}

pred GWValidStates {
    // All states must assign a position to every animal and to the boat.
    all s: GWState, a: GWAnimal | {
        // TODO fill in
        one s.gwshore[a]
    }
    all s: GWState {
        // TODO fill in
        one s.gwboat
    }
}

// each of the predicates below should ASSUME valid states
//  they should NOT ENFORCE valid states
// (the `run` command below will enforce it!)

pred GWinitState[s: GWState] {
    // All animals and the boat must start on the near side
    // TODO fill in

    all a: GWAnimal | s.gwshore[a] = Near
    s.gwboat = Near

}

pred GWfinalState[s: GWState] {
    // All animals and the boat must end on the far side
    // TODO fill in

    all a: GWAnimal | s.gwshore[a] = Far
    s.gwboat = Far
}


pred GWcanTransition[pre: GWState, post: GWState] {
    //the boat must move
    pre.gwboat != post.gwboat

    // - the boat can carry 1-2 animals (not zero!)
    // - every other animal stays in the same place
    let movedAnimals = {a: GWAnimal | pre.gwshore[a] != post.gwshore[a]} | {
        #movedAnimals > 0 && #movedAnimals <= 2
        //all a: GWAnimal - movedAnimals | pre.gwshore[a] = post.gwshore[a]

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

        //some pre, post: GWState | GWcanTransition[pre, post]


    }
}


pred GWNeverEating {
    // Never have goats outnumbered by wolves on either side.
    // TODO fill in
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

