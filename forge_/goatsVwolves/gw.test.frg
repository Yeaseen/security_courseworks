#lang forge/bsl

open "common.frg"

// Uncomment exactly ONE of these at a time:
open "gw.wheat"    -- hidden solution
//open "gw.frg"   -- your code

test suite for GWValidStates {

    // Example valid state
    example validState is GWValidStates for {
        GWState = `S0 -- a trace with one state for simplicity
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far
        gwshore =   `S0 -> `G0 ->  Far +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near +
                    `S0 -> `W2 -> Near 

        gwboat = `S0  -> `Near0 

    }

    // Example invalid state: less than 3 wolves on near side at start
    example invalidState1 is not GWValidStates for {
        GWState = `S0 
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far

        gwshore =   `S0 -> `G0 -> Near +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near 

        gwboat = `S0 -> `Near0 
    }

}

test suite for GWinitState {
    example validGWinitState is GWinitState[GWState] for {
    GWState = `S0
    Goat = `G0 + `G1 + `G2
    Wolf = `W0 + `W1 + `W2
    GWAnimal = Goat + Wolf
    Far = `Far0
    Near = `Near0
    Position = Near + Far
    gwshore =   `S0 -> `G0 -> Near +
                `S0 -> `G1 -> Near +
                `S0 -> `G2 -> Near +
                `S0 -> `W0 -> Near +
                `S0 -> `W1 -> Near +
                `S0 -> `W2 -> Near
    gwboat = `S0  -> `Near0
    }
}

test suite for GWfinalState {
    example validGWfinalState is GWfinalState[GWState] for {
    GWState = `S0
    Goat = `G0 + `G1 + `G2
    Wolf = `W0 + `W1 + `W2
    GWAnimal = Goat + Wolf
    Far = `Far0
    Near = `Near0
    Position = Near + Far
    gwshore =   `S0 -> `G0 -> Far +
                `S0 -> `G1 -> Far +
                `S0 -> `G2 -> Far +
                `S0 -> `W0 -> Far +
                `S0 -> `W1 -> Far +
                `S0 -> `W2 -> Far
    gwboat = `S0  -> `Far0
    }
}
test suite for GWcanTransition {

    example validTransition is {some pre, post: GWState | GWcanTransition[pre, post]} for {
        GWState = `S0 + `S1
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far

        gwnext = `S0 -> `S1

        gwshore =   `S0 -> `G0 ->  Near +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near +
                    `S0 -> `W2 -> Near +

                    `S1 -> `G0 -> Far +
                    `S1 -> `G1 -> Far +
                    `S1 -> `G2 -> Near +
                    `S1 -> `W0 -> Near +
                    `S1 -> `W1 -> Near +
                    `S1 -> `W2 -> Near 

        gwboat = `S0  -> `Near0 +
                 `S1  -> `Far0 

    }

    example invalidTransition1 is not {some pre, post: GWState | GWcanTransition[pre, post]} for {
        GWState = `S0 + `S1 
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far
        gwnext = `S0 -> `S1

        gwshore =   `S0 -> `G0 ->  Near +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near +
                    `S0 -> `W2 -> Near +

                    `S1 -> `G0 -> Far +
                    `S1 -> `G1 -> Far +
                    `S1 -> `G2 -> Far +
                    `S1 -> `W0 -> Near +
                    `S1 -> `W1 -> Near +
                    `S1 -> `W2 -> Near 

        gwboat = `S0  -> `Near0 +
                 `S1  -> `Far0 
    }

    example invalidTransition2 is not {some pre, post: GWState | GWcanTransition[pre, post]} for {
        GWState = `S0 + `S1 
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far

        gwnext = `S0 -> `S1

        gwshore =   `S0 -> `G0 ->  Near +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near +
                    `S0 -> `W2 -> Near +

                    `S1 -> `G0 -> Near +
                    `S1 -> `G1 -> Near +
                    `S1 -> `G2 -> Near +
                    `S1 -> `W0 -> Near +
                    `S1 -> `W1 -> Near +
                    `S1 -> `W2 -> Near 

        gwboat = `S0  -> `Near0 +
                `S1  -> `Far0 
    }

}

test suite for TransitionStates {
}

test suite for GWNeverEating {
    example neverEating is GWNeverEating for {
        GWState = `S0 
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far

        gwshore =   `S0 -> `G0 ->  Near +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near +
                    `S0 -> `W2 -> Near 

        gwboat = `S0  -> `Near0 

    }

    example someEating is not GWNeverEating for {
        GWState = `S0 
        Goat = `G0 + `G1 + `G2
        Wolf = `W0 + `W1 + `W2
        GWAnimal = Goat + Wolf
        Far = `Far0
        Near = `Near0
        Position = Near + Far

        gwshore =   `S0 -> `G0 ->  Far +
                    `S0 -> `G1 -> Near +
                    `S0 -> `G2 -> Near +
                    `S0 -> `W0 -> Near +
                    `S0 -> `W1 -> Near +
                    `S0 -> `W2 -> Near 

        gwboat = `S0  -> `Near0 
    }

}