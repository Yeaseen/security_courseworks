#include "POUS.h"
void LOGGER_init__(LOGGER *data__, BOOL retain) {
  __INIT_VAR(data__->EN,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->ENO,__BOOL_LITERAL(TRUE),retain)
  __INIT_VAR(data__->TRIG,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->MSG,__STRING_LITERAL(0,""),retain)
  __INIT_VAR(data__->LEVEL,LOGLEVEL__INFO,retain)
  __INIT_VAR(data__->TRIG0,__BOOL_LITERAL(FALSE),retain)
}

// Code part
void LOGGER_body__(LOGGER *data__) {
  // Control execution
  if (!__GET_VAR(data__->EN)) {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(FALSE));
    return;
  }
  else {
    __SET_VAR(data__->,ENO,,__BOOL_LITERAL(TRUE));
  }
  // Initialise TEMP variables

  if ((__GET_VAR(data__->TRIG,) && !(__GET_VAR(data__->TRIG0,)))) {
    #define GetFbVar(var,...) __GET_VAR(data__->var,__VA_ARGS__)
    #define SetFbVar(var,val,...) __SET_VAR(data__->,var,__VA_ARGS__,val)

   LogMessage(GetFbVar(LEVEL),(char*)GetFbVar(MSG, .body),GetFbVar(MSG, .len));
  
    #undef GetFbVar
    #undef SetFbVar
;
  };
  __SET_VAR(data__->,TRIG0,,__GET_VAR(data__->TRIG,));

  goto __end;

__end:
  return;
} // LOGGER_body__() 





void PROGRAM0_init__(PROGRAM0 *data__, BOOL retain) {
  __INIT_VAR(data__->STARTBUTTON,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->ROLLERENGINE,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->NOZZLE,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->BOTTLESENSOR,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->WATERLEVELSENSOR,__BOOL_LITERAL(FALSE),retain)
  __INIT_VAR(data__->PLANTSTATE,0,retain)
}

// Code part
void PROGRAM0_body__(PROGRAM0 *data__) {
  // Initialise TEMP variables

  if ((__GET_VAR(data__->PLANTSTATE,) == 0)) {
    __SET_VAR(data__->,ROLLERENGINE,,__BOOL_LITERAL(FALSE));
    __SET_VAR(data__->,NOZZLE,,__BOOL_LITERAL(FALSE));
    if (__GET_VAR(data__->STARTBUTTON,)) {
      __SET_VAR(data__->,PLANTSTATE,,1);
    };
  };
  if ((__GET_VAR(data__->PLANTSTATE,) == 1)) {
    if ((__GET_VAR(data__->BOTTLESENSOR,) && !(__GET_VAR(data__->WATERLEVELSENSOR,)))) {
      __SET_VAR(data__->,NOZZLE,,__BOOL_LITERAL(TRUE));
    } else {
      __SET_VAR(data__->,NOZZLE,,__BOOL_LITERAL(FALSE));
    };
    if (__GET_VAR(data__->WATERLEVELSENSOR,)) {
      __SET_VAR(data__->,PLANTSTATE,,2);
    };
  };
  if ((__GET_VAR(data__->PLANTSTATE,) == 2)) {
    __SET_VAR(data__->,NOZZLE,,__BOOL_LITERAL(FALSE));
    __SET_VAR(data__->,ROLLERENGINE,,__BOOL_LITERAL(TRUE));
    if (!(__GET_VAR(data__->BOTTLESENSOR,))) {
      __SET_VAR(data__->,PLANTSTATE,,1);
    };
  };
  if (!(__GET_VAR(data__->STARTBUTTON,))) {
    __SET_VAR(data__->,PLANTSTATE,,0);
  };

  goto __end;

__end:
  return;
} // PROGRAM0_body__() 





