#lang forge/bsl

open "common.frg"

abstract sig GWAnimal {}
sig Goat extends GWAnimal {}
sig Wolf extends GWAnimal {}

sig GWState {
    gwnext: lone GWState,
    gwshore: func GWAnimal -> Position, -- where is every animal?
    gwboat: one Position -- where is the boat?
}

pred GWValidStates {
    // All states must assign a position to every animal and to the boat.
    all s: GWState, a: GWAnimal | {
        // TODO fill in
    }
    all s: GWState {
        // TODO fill in
    }
}

// each of the predicates below should ASSUME valid states
//  they should NOT ENFORCE valid states
// (the `run` command below will enforce it!)

pred GWinitState[s: GWState] {
    // All animals and the boat must start on the near side
    // TODO fill in
}

pred GWfinalState[s: GWState] {
    // All animals and the boat must end on the far side
    // TODO fill in
}

pred GWcanTransition[pre: GWState, post: GWState] {
    // - the boat must move
    // - the boat can carry 1-2 animals (not zero!)
    // - every other animal stays in the same place
    // TODO fill in
}

pred GWTransitionStates {
    some init, final: GWState {
        GWinitState[init]
        GWfinalState[final]

        // - must be no state before the init state
        // TODO fill in
        // - must be no state after the final state
        // TODO fill in
        // - every state must be reachable from the initial
        // TODO fill in
        // - all state transitions must be valid
        // TODO fill in
    }
}

pred GWNeverEating {
    // Never have goats outnumbered by wolves on either side.
    // TODO fill in
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

